import { FC, FormEvent, useState } from 'react'

import { ClassName, useClassName } from '../hooks/className'
import { useFireEvent, AnyEvent } from '../hooks/events'
import { useRequest } from '../tools'

import { FastProps, AnyCompList } from './index'

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
  event: AnyEvent
}

export const FormComp: FC<FormProps | ModelFormProps> = (props) => {
  const { formFields, submitUrl, footer } = props

  // mostly equivalent to `<input disabled`
  const [locked, setLocked] = useState(false)
  const [fieldErrors, setFieldErrors] = useState<Record<string, string>>({})
  const [error, setError] = useState<string | null>(null)
  const { fireEvent } = useFireEvent()
  const request = useRequest()

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
    <div className={useClassName(props, { el: 'form-container' })}>
      <form className={useClassName(props)} onSubmit={onSubmit}>
        <AnyCompList propsList={fieldProps} />
        {error ? <div>Error: {error}</div> : null}
        <Footer footer={footer} />
      </form>
    </div>
  )
}

const Footer: FC<{ footer?: boolean | FastProps[] }> = ({ footer }) => {
  if (footer === false) {
    return null
  } else if (footer === true || typeof footer === 'undefined') {
    return <ButtonComp type="Button" text="Submit" htmlType="submit" />
  } else {
    return <AnyCompList propsList={footer} />
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
