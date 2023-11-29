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

export const classNameGenerator: ClassNameGenerator = ({ props, fullPath, subElement }): ClassName => {
  const { type } = props
  switch (type) {
    case 'Page':
      return 'container mt-80'
    case 'Button':
      return 'btn btn-primary'
    case 'Table':
      switch (subElement) {
        case 'no-data-message':
          return 'text-center mt-2'
        default:
          return 'table table-striped table-bordered'
      }
    case 'Details':
      switch (subElement) {
        case 'dt':
          return 'col-sm-3 col-md-2 text-sm-end'
        case 'dd':
          return 'col-sm-9 col-md-10'
        default:
          return 'row'
      }
    case 'Form':
    case 'ModelForm':
      if (props.displayMode === 'inline') {
        switch (subElement) {
          case 'form-container':
            return ''
          default:
            return 'row row-cols-lg-4 align-items-center justify-content-end'
        }
      } else {
        switch (subElement) {
          case 'form-container':
            return 'row justify-content-center'
          default:
            return 'col-md-4'
        }
      }
    case 'FormFieldInput':
    case 'FormFieldCheckbox':
    case 'FormFieldSelect':
    case 'FormFieldSelectSearch':
    case 'FormFieldFile':
      switch (subElement) {
        case 'input':
          return props.error ? 'is-invalid form-control' : 'form-control'
        case 'select':
          return 'form-select'
        case 'select-react':
          return ''
        case 'label':
          if (props.displayMode === 'inline') {
            return 'visually-hidden'
          } else {
            return { 'form-label': true, 'fw-bold': props.required }
          }
        case 'error':
          return 'invalid-feedback'
        case 'description':
          return 'form-text'
        default:
          return 'mb-3'
      }
    case 'Navbar':
      switch (subElement) {
        case 'contents':
          return 'container'
        case 'title':
          return 'navbar-brand'
        default:
          return 'border-bottom fixed-top bg-body'
      }
    case 'Link':
      return {
        active: pathMatch(props.active, fullPath),
        'nav-link': props.mode === 'navbar' || props.mode === 'tabs',
      }
    case 'LinkList':
      if (subElement === 'link-list-item' && props.mode) {
        return 'nav-item'
      } else {
        switch (props.mode) {
          case 'tabs':
            return 'nav nav-underline'
          case 'vertical':
            return 'nav flex-column'
          default:
            return ''
        }
      }
  }
}
