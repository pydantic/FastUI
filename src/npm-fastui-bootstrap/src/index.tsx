import { pathMatch } from 'fastui'

import type { ClassNameGenerator, CustomRender, models } from 'fastui'

import { Modal } from './modal'
import { Navbar } from './navbar'
import { Pagination } from './pagination'
import { Footer } from './footer'
import { Toast } from './toast'

export const customRender: CustomRender = (props) => {
  const { type } = props
  switch (type) {
    case 'Navbar':
      return () => <Navbar {...props} />
    case 'Footer':
      return () => <Footer {...props} />
    case 'Modal':
      return () => <Modal {...props} />
    case 'Pagination':
      return () => <Pagination {...props} />
    case 'Toast':
      return () => <Toast {...props} />
  }
}

export const classNameGenerator: ClassNameGenerator = ({
  props,
  fullPath,
  subElement,
}): models.ClassName | undefined => {
  const { type } = props
  switch (type) {
    case 'Page':
      return 'container mt-80 mb-3 page'
    case 'Button':
      return {
        btn: true,
        'btn-primary': !props.namedStyle || props.namedStyle === 'primary',
        'btn-secondary': props.namedStyle === 'secondary',
        'btn-warning': props.namedStyle === 'warning',
      }
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
      } else if (props.displayMode === 'page') {
        switch (subElement) {
          case 'form-container':
            return 'row justify-content-center'
          default:
            return 'col-md-4'
        }
      } else {
        break
      }
    case 'FormFieldInput':
    case 'FormFieldTextarea':
    case 'FormFieldBoolean':
    case 'FormFieldSelect':
    case 'FormFieldSelectSearch':
    case 'FormFieldFile':
      switch (subElement) {
        case 'textarea':
        case 'input':
        case 'select-react':
          return {
            'form-control': !['FormFieldBoolean', 'FormFieldSelect'].includes(type),
            'is-invalid': props.error != null,
            'form-check-input': type === 'FormFieldBoolean',
          }
        case 'select':
          return 'form-select'
        case 'label':
          if (props.displayMode === 'inline') {
            return 'visually-hidden'
          } else {
            return { 'form-label': true, 'fw-bold': !!props.required, 'form-check-label': type === 'FormFieldBoolean' }
          }
        case 'error':
          return 'invalid-feedback'
        case 'description':
          return 'form-text'
        default:
          return {
            'mb-3': true,
            'form-check': type === 'FormFieldBoolean',
            'form-switch': type === 'FormFieldBoolean' && props.mode === 'switch',
          }
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
    case 'Footer':
      switch (subElement) {
        case 'link-list':
          return 'nav justify-content-center pb-1'
        case 'extra':
          return 'text-center text-muted pb-3'
        default:
          return 'border-top pt-1 mt-auto bg-body'
      }
    case 'Link':
      return {
        active: pathMatch(props.active, fullPath),
        'nav-link': props.mode === 'navbar' || props.mode === 'tabs' || props.mode === 'footer',
        'text-muted': props.mode === 'footer',
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
    case 'Code':
      return 'rounded'
    case 'Error':
      if (props.statusCode === 502) {
        return 'm-3 text-muted'
      } else {
        return 'error-alert alert alert-danger m-3'
      }
    case 'Spinner':
      if (subElement === 'text') {
        return 'd-flex justify-content-center mb-2'
      } else if (subElement === 'animation') {
        return 'd-flex justify-content-center'
      } else {
        return 'my-4'
      }
  }
}
