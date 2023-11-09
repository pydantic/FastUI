import { useContext, FC } from 'react'
import { ErrorContext } from '../hooks/error'
import { CustomRenderContext } from '../hooks/customRender'
import { DivComp, AllDivProps } from './div'
import { TextProps, TextComp } from './text'
import { FormFieldComp, FormFieldProps } from './FormField'
import { ButtonComp, ButtonProps } from './button'
import { ModalComp, ModalProps } from './modal'

export type FastProps = TextProps | AllDivProps | FormFieldProps | ButtonProps | ModalProps

export const AnyComp: FC<FastProps> = (props) => {
  const { setError, DisplayError } = useContext(ErrorContext)
  const customRender = useContext(CustomRenderContext)
  const { type } = props

  if (customRender) {
    try {
      const CustomRenderComp = customRender(props)
      if (CustomRenderComp) {
        return <CustomRenderComp />
      }
    } catch (e) {
      // TODO maybe we shouldn't catch this error (by default)?
      const description = (e as any).message
      setError({ title: 'Custom Render Error', description })
    }
  }

  try {
    switch (type) {
      case 'Text':
        return TextComp(props)
      case 'Div':
      case 'Container':
      case 'Row':
      case 'Col':
        return DivComp(props)
      case 'Button':
        return ButtonComp(props)
      case 'FormField':
        return FormFieldComp(props)
      case 'Modal':
        return ModalComp(props)
      default:
        return <DisplayError title="Invalid Server Response" description={`Unknown component type: "${type}"`} />
    }
  } catch (e) {
    // TODO maybe we shouldn't catch this error (by default)?
    const description = (e as any).message
    return <DisplayError title="Render Error" description={description} />
  }
}

export const RenderChildren: FC<{ children: FastProps[] }> = ({ children }) => (
  <>
    {children.map((child, i) => (
      <AnyComp key={i} {...child} />
    ))}
  </>
)
