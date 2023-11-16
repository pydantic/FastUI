import { FC, FormEvent, useState } from 'react'

import { ClassName, useClassNameGenerator } from '../hooks/className'
import { useFireEvent, PageEvent, GoToEvent } from '../hooks/event'
import { useCustomRender } from '../hooks/customRender'
import { request } from '../tools'

import { FormFieldProps, FormFieldComp } from './FormField'

export interface FormProps {
  type: 'Form'
  formFields: FormFieldProps[]
  submitUrl: string
  className?: ClassName
}

interface FormResponse {
  type: 'FormResponse'
  event: PageEvent | GoToEvent
}

export interface ModelFormProps extends Omit<FormProps, 'type'> {
  type: 'ModelForm'
}

export const FormComp: FC<FormProps | ModelFormProps> = (props) => {
  const { className, formFields, submitUrl } = props

  // mostly equivalent to `<input disabled`
  const [locked, setLocked] = useState(false)
  const [fieldErrors, setFieldErrors] = useState<Record<string, string>>({})
  const [error, setError] = useState<string | null>(null)
  const { fireEvent } = useFireEvent()

  const onSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    setLocked(true)
    setError(null)
    setFieldErrors({})
    const formData = new FormData(e.currentTarget)

    const [status, data] = await request({ url: submitUrl, formData, expectedStatus: [200, 422] })
    if (status === 200) {
      if (data.type !== 'FormResponse') {
        throw new Error(`Expected FormResponse, got ${JSON.stringify(data)}`)
      }
      const { event } = data as FormResponse
      fireEvent(event)
    } else {
      // status === 422
      const errorResponse = data as ErrorResponse
      const formErrors = errorResponse.detail.form
      if (formErrors) {
        setFieldErrors(Object.fromEntries(formErrors.map((e) => [locToName(e.loc), e.msg])))
      } else {
        console.warn('Non-field error submitting form:', data)
        setError('Error submitting form')
      }
    }
    setLocked(false)
  }

  return (
    <form className={useClassNameGenerator(className, props)} onSubmit={onSubmit}>
      {formFields.map((formField, i) => (
        <RenderField key={i} {...formField} error={fieldErrors[formField.name]} locked={locked} />
      ))}
      {error ? <div>Error: {error}</div> : null}
      <button type="submit">Submit</button>
    </form>
  )
}

const RenderField: FC<FormFieldProps> = (props) => {
  const CustomRenderComp = useCustomRender(props)
  if (CustomRenderComp) {
    return <CustomRenderComp />
  } else {
    return <FormFieldComp {...props} />
  }
}

type Loc = (string | number)[]
interface Error {
  type: string
  loc: Loc
  msg: string
}

interface ErrorResponse {
  detail: { form?: Error[] }
}

/**
 * Should match `loc_to_name` in python so errors can be connected to the correct field
 */
function locToName(loc: Loc): string {
  if (loc.some((v) => typeof v === 'string' && v.includes('.'))) {
    return JSON.stringify(loc)
  } else if (typeof loc[0] === 'string' && loc[0].startsWith('[')) {
    return JSON.stringify(loc)
  } else {
    return loc.join('.')
  }
}
