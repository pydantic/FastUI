import {useContext, ReactNode} from 'react'
import {ErrorContext} from '../errorContext'
import {DivComp, DivRender, DivTypes} from './div'
import {Text, TextRender} from './text'
import {FormFieldRender, FormField} from './FormField'

export type AnyComp = Text | DivComp | FormField
export type CompTypes = 'Text' | DivTypes | 'FormField'

export type CustomRender = (props: AnyComp) => ReactNode | null

export const AnyCompRender = (props: AnyComp, customRender?: CustomRender): ReactNode => {
  const {setError} = useContext(ErrorContext)
  const {type} = props

  if (customRender) {
    try {
      const node = customRender(props)
      if (node) {
        return node
      }
    } catch (e) {
      const description = (e as any).message
      setError({title: 'Custom Render Error', description})
    }
  }

  try {
    switch (type) {
      case 'Text':
        return TextRender(props)
      case 'Div':
      case 'Container':
      case 'Row':
      case 'Col':
        return DivRender(props)
      case 'FormField':
        return FormFieldRender(props)
      default:
        setError({title: 'Render Error', description: `Unknown component type: ${type}`})
    }
  } catch (e) {
    const description = (e as any).message
    setError({title: 'Render Error', description})
  }
}
