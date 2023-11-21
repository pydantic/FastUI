import { ClassNameGenerator, CustomRender } from 'fastui'

import type { FormFieldProps, ClassName } from 'fastui'

export const customRender: CustomRender = (props) => {
  const { type } = props
  if (type === 'DisplayPrimitive') {
    const { value } = props
    if (typeof value === 'boolean') {
      return () => <>{value ? '👍' : '👎'}</>
    }
  }
}

export const classNameGenerator: ClassNameGenerator = (props, subElement) => {
  const { type } = props
  switch (type) {
    case 'Page':
      return 'container py-4'
    case 'Row':
      return 'row'
    case 'Col':
      return 'col'
    case 'Button':
      return 'btn btn-primary'
    case 'Table':
      return 'table table-striped'
    case 'Form':
    case 'ModelForm':
      return formClassName(subElement)
    case 'FormFieldInput':
    case 'FormFieldCheckbox':
    case 'FormFieldSelect':
    case 'FormFieldFile':
      return formFieldClassName(props, subElement)
  }
}

function formFieldClassName(props: FormFieldProps, subElement?: string): ClassName {
  switch (subElement) {
    case 'input':
      return props.error ? 'is-invalid form-control' : 'form-control'
    case 'select':
      return 'form-select'
    case 'label':
      return { 'form-label': true, 'fw-bold': props.required }
    case 'error':
      return 'invalid-feedback'
    default:
      return 'mb-3'
  }
}

function formClassName(subElement?: string): ClassName {
  switch (subElement) {
    case 'form-container':
      return 'd-flex justify-content-center'
  }
}
