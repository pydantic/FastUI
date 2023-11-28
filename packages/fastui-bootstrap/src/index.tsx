import { pathMatch } from 'fastui'

import type { components, ClassNameGenerator, CustomRender, ClassName } from 'fastui'

import { Modal } from './modal'
import { Navbar } from './navbar'
import { Pagination } from './pagination'

export const customRender: CustomRender = (props) => {
  const { type } = props
  switch (type) {
    case 'DisplayPrimitive':
      return displayPrimitiveRender(props)
    case 'Navbar':
      return () => <Navbar {...props} />
    case 'Modal':
      return () => <Modal {...props} />
    case 'Pagination':
      return () => <Pagination {...props} />
  }
}

function displayPrimitiveRender(props: components.DisplayPrimitiveProps) {
  const { value } = props
  if (typeof value === 'boolean') {
    return () => <>{value ? '👍' : '👎'}</>
  }
}

export const classNameGenerator: ClassNameGenerator = ({ props, fullPath, subElement }) => {
  const { type } = props
  switch (type) {
    case 'Page':
      return 'container py-4'
    case 'Button':
      return 'btn btn-primary'
    case 'Table':
      return 'table table-striped table-bordered'
    case 'Form':
    case 'ModelForm':
      return formClassName(subElement)
    case 'FormFieldInput':
    case 'FormFieldCheckbox':
    case 'FormFieldSelect':
    case 'FormFieldSelectSearch':
    case 'FormFieldFile':
      return formFieldClassName(props, subElement)
    case 'Navbar':
      return navbarClassName(subElement)
    case 'Link':
      return linkClassName(props, fullPath)
    case 'LinkList':
      return linkListClassName(props, subElement)
  }
}

function formFieldClassName(props: components.FormFieldProps, subElement?: string): ClassName {
  switch (subElement) {
    case 'input':
      return props.error ? 'is-invalid form-control' : 'form-control'
    case 'select':
      return 'form-select'
    case 'select-react':
      return ''
    case 'label':
      return { 'form-label': true, 'fw-bold': props.required }
    case 'error':
      return 'invalid-feedback'
    case 'description':
      return 'form-text'
    default:
      return 'mb-3'
  }
}

function formClassName(subElement?: string): ClassName {
  switch (subElement) {
    case 'form-container':
      return 'row justify-content-center'
    default:
      return 'col-md-4'
  }
}

function navbarClassName(subElement?: string): ClassName {
  switch (subElement) {
    case 'contents':
      return 'container'
    case 'title':
      return 'navbar-brand'
    default:
      return 'navbar navbar-expand-lg bg-body-tertiary'
  }
}

function linkClassName(props: components.LinkProps, fullPath: string): ClassName {
  return {
    active: pathMatch(props.active, fullPath),
    'nav-link': props.mode === 'navbar' || props.mode === 'tabs',
  }
}

function linkListClassName(props: components.LinkListProps, subElement?: string): ClassName {
  if (subElement === 'link-list-item' && props.mode) {
    return 'nav-item'
  }
  switch (props.mode) {
    case 'tabs':
      return 'nav nav-underline'
    case 'vertical':
      return 'nav flex-column'
    default:
      return ''
  }
}
