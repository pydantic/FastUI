import { FC, FormEvent, useState } from 'react'

import { ClassName, useClassNameGenerator } from '../hooks/className'
import { useFireEvent, PageEvent, GoToEvent } from '../hooks/event'
import { request } from '../tools'

import { FastProps, RenderChildren } from './index'

import { ButtonComp } from './button'
import { FormFieldProps } from './FormField'

interface BaseFormProps {
  formFields: FormFieldProps[]
  submitUrl: string
  footer?: boolean | FastProps[]
  className?: ClassName
}

export interface FormProps extends BaseFormProps {
  type: 'Form'
}

export interface ModelFormProps extends BaseFormProps {
  type: 'ModelForm'
}

interface FormResponse {
  type: 'FormResponse'
  event: PageEvent | GoToEvent
}

export const FormComp: FC<FormProps | ModelFormProps> = (props) => {
  const { className, formFields, submitUrl, footer } = props

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

  const fieldProps: FormFieldProps[] = formFields.map((formField) =>
    Object.assign({}, formField, { error: fieldErrors[formField.name], locked }),
  )

  return (
    <form className={useClassNameGenerator(className, props)} onSubmit={onSubmit}>
      <RenderChildren children={fieldProps} />
      {error ? <div>Error: {error}</div> : null}
      <Footer footer={footer} />
    </form>
  )
}

const Footer: FC<{ footer?: boolean | FastProps[] }> = ({ footer }) => {
  if (footer === false) {
    return null
  } else if (footer === true || typeof footer === 'undefined') {
    return <ButtonComp type="Button" text="Submit" htmlType="submit" />
  } else {
    return <RenderChildren children={footer} />
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
