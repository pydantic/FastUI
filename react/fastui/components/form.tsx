import { FC, FormEvent } from 'react'

import { ClassName, useClassNameGenerator } from '../hooks/className'
import { useFireEvent, PageEvent, GoToEvent } from '../hooks/event'
import { useCustomRender } from '../hooks/customRender'
import { request } from '../tools'

import { FormFieldProps, FormFieldComp } from './FormField'

export interface FormProps {
  type: 'Form'
  formFields: FormFieldProps[]
  submitUrl?: string
  successEvent?: PageEvent | GoToEvent
  className?: ClassName
}

export interface ModelFormProps extends Omit<FormProps, 'type'> {
  type: 'ModelForm'
}

export const FormComp: FC<FormProps | ModelFormProps> = (props) => {
  const { className, formFields, successEvent, submitUrl } = props

  const { fireEvent } = useFireEvent()

  const onSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    const formData = new FormData(e.currentTarget)
    console.log(Object.fromEntries(formData.entries()))
    if (submitUrl) {
      const [status, data] = await request({ url: submitUrl, formData, expectedStatus: [200, 422] })
      console.log({ status, data })
      // TODO substitute into event
    }
    fireEvent(successEvent)
  }

  return (
    <form className={useClassNameGenerator(className, props)} onSubmit={onSubmit}>
      {formFields.map((formField, i) => (
        <RenderField key={i} {...formField} />
      ))}
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
