import { FC, FormEvent, useContext, useState, useRef, useCallback } from 'react'

import { ClassName, useClassName } from '../hooks/className'
import { useFireEvent, AnyEvent } from '../events'
import { useRequest, RequestArgs } from '../tools'
import { LocationContext } from '../hooks/locationContext'

import { FastProps, AnyCompList } from './index'

import { ButtonComp } from './button'
import { FormFieldProps } from './FormField'

interface BaseFormProps {
  formFields: FormFieldProps[]
  initial?: Record<string, any>
  submitUrl: string
  footer?: boolean | FastProps[]
  method?: 'GET' | 'GOTO' | 'POST'
  displayMode?: 'default' | 'inline'
  submitOnChange?: boolean
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
  const formRef = useRef<HTMLFormElement>(null)
  const { formFields, initial, submitUrl, method, footer, displayMode, submitOnChange } = props

  // mostly equivalent to `<input disabled`
  const [locked, setLocked] = useState(false)
  const [fieldErrors, setFieldErrors] = useState<Record<string, string>>({})
  const [error, setError] = useState<string | null>(null)
  const { fireEvent } = useFireEvent()
  const request = useRequest()
  const { goto } = useContext(LocationContext)

  const submit = useCallback(
    async (formData: FormData) => {
      setLocked(true)
      setError(null)
      setFieldErrors({})

      if (method === 'GOTO') {
        // this seems to work in common cases, but typescript doesn't like it
        const query = new URLSearchParams(formData as any)
        for (const [k, v] of query.entries()) {
          if (v === '') {
            query.delete(k)
          }
        }
        const queryStr = query.toString()
        goto(queryStr === '' ? submitUrl : `${submitUrl}?${queryStr}`)
        setLocked(false)
        return
      }

      const requestArgs: RequestArgs = { url: submitUrl, expectedStatus: [200, 422] }
      if (method === 'GET') {
        // as above with URLSearchParams
        requestArgs.query = new URLSearchParams(formData as any)
      } else {
        requestArgs.formData = formData
      }

      const [status, data] = await request(requestArgs)
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
    },
    [goto, method, request, submitUrl, fireEvent],
  )

  const onSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    const formData = new FormData(e.currentTarget)
    await submit(formData)
  }

  const onChange = useCallback(() => {
    if (submitOnChange && formRef.current) {
      const formData = new FormData(formRef.current)
      submit(formData)
    }
  }, [submitOnChange, submit])

  const fieldProps: FormFieldProps[] = formFields.map((formField) => {
    const f = {
      ...formField,
      error: fieldErrors[formField.name],
      locked,
      displayMode,
      onChange,
    } as FormFieldProps
    const formInitial = initial && initial[formField.name]
    if (formInitial !== undefined) {
      ;(f as any).initial = formInitial
    }
    return f
  })

  return (
    <div className={useClassName(props, { el: 'form-container' })}>
      <form ref={formRef} className={useClassName(props)} onSubmit={onSubmit}>
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
