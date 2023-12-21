import { FC, FormEvent, useContext, useState, useRef, useCallback, useEffect } from 'react'

import type { Form, ModelForm, FastProps } from '../models'

import { useClassName } from '../hooks/className'
import { useRequest, RequestArgs } from '../tools'
import { LocationContext } from '../hooks/locationContext'
import { usePageEventListen } from '../events'

import { AnyCompList } from './index'

import { ButtonComp } from './button'
import { FormFieldProps } from './FormField'

export const FormComp: FC<Form | ModelForm> = (props) => {
  const formRef = useRef<HTMLFormElement>(null)
  const { formFields, initial, submitUrl, method, footer, displayMode, submitOnChange, submitTrigger } = props

  // mostly equivalent to `<input disabled`
  const [locked, setLocked] = useState(false)
  const [fieldErrors, setFieldErrors] = useState<Record<string, string>>({})
  const [error, setError] = useState<string | null>(null)
  const [responseComponentProps, setResponseComponentProps] = useState<FastProps[] | null>(null)

  // if form fields change or the submit url changes, clear the response
  useEffect(() => {
    setResponseComponentProps(null)
  }, [formFields, submitUrl])

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
        setResponseComponentProps(data as FastProps[])
      } else {
        console.assert(status === 422)
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
    [goto, method, request, submitUrl],
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

  const { fireId } = usePageEventListen(submitTrigger)

  useEffect(() => {
    if (fireId && formRef.current) {
      const formData = new FormData(formRef.current)
      submit(formData)
    }
  }, [fireId, submit])

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

  const containerClassName = useClassName(props, { el: 'form-container' })
  const formClassName = useClassName(props)

  if (responseComponentProps) {
    return (
      <div className={containerClassName}>
        <AnyCompList propsList={responseComponentProps} />
      </div>
    )
  } else {
    return (
      <div className={containerClassName}>
        <form ref={formRef} className={formClassName} onSubmit={onSubmit}>
          <AnyCompList propsList={fieldProps} />
          {error ? <div>Error: {error}</div> : null}
          <Footer footer={footer} />
        </form>
      </div>
    )
  }
}

const Footer: FC<{ footer?: FastProps[] }> = ({ footer }) => {
  if (typeof footer === 'undefined') {
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
