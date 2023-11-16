import { useContext, FC } from 'react'

import { ErrorContext } from '../hooks/error'
import { useCustomRender } from '../hooks/customRender'
import { unreachable } from '../tools'

import { AllDivProps, DivComp } from './div'
import { TextProps, TextComp } from './text'
import { HeadingComp, HeadingProps } from './heading'
import { FormComp, FormProps, ModelFormProps } from './form'
import { FormFieldComp, FormFieldProps } from './FormField'
import { ButtonComp, ButtonProps } from './button'
import { LinkComp, LinkProps } from './link'
import { ModalComp, ModalProps } from './modal'
import { TableComp, TableProps } from './table'
import { AllDisplayProps, DisplayArray, DisplayComp, DisplayObject, DisplayPrimitive } from './display'
import { JsonComp, JsonProps } from './Json'

export type FastProps =
  | TextProps
  | AllDivProps
  | HeadingProps
  | FormProps
  | ModelFormProps
  | FormFieldProps
  | ButtonProps
  | ModalProps
  | TableProps
  | LinkProps
  | AllDisplayProps
  | JsonProps

export const AnyComp: FC<FastProps> = (props) => {
  const { DisplayError } = useContext(ErrorContext)

  const CustomRenderComp = useCustomRender(props)
  if (CustomRenderComp) {
    return <CustomRenderComp />
  }

  const { type } = props
  try {
    switch (type) {
      case 'Text':
        return <TextComp {...props} />
      case 'Div':
      case 'Page':
      case 'Row':
      case 'Col':
        return renderWithChildren(DivComp, props)
      case 'Heading':
        return <HeadingComp {...props} />
      case 'Button':
        return <ButtonComp {...props} />
      case 'Link':
        return renderWithChildren(LinkComp, props)
      case 'Form':
      case 'ModelForm':
        return <FormComp {...props} />
      case 'FormField':
        return <FormFieldComp {...props} />
      case 'Modal':
        return <ModalComp {...props} />
      case 'Table':
        return <TableComp {...props} />
      case 'Display':
        return <DisplayComp {...props} />
      case 'DisplayArray':
        return <DisplayArray {...props} />
      case 'DisplayObject':
        return <DisplayObject {...props} />
      case 'DisplayPrimitive':
        return <DisplayPrimitive {...props} />
      case 'JSON':
        return <JsonComp {...props} />
      default:
        unreachable('Unexpected component type', type, props)
        return <DisplayError title="Invalid Server Response" description={`Unknown component type: "${type}"`} />
    }
  } catch (e) {
    // TODO maybe we shouldn't catch this error (by default)?
    const description = (e as any).message
    return <DisplayError title="Render Error" description={description} />
  }
}

interface WithChildren {
  children: FastProps[]
}

function renderWithChildren<T extends WithChildren>(Component: FC<T>, props: T) {
  const { children, ...rest } = props
  // TODO  is there a way to make this type safe?
  return <Component {...(rest as any)}>{children}</Component>
}

export const RenderChildren: FC<{ children: FastProps[] }> = ({ children }) => (
  <>
    {children.map((child, i) => (
      <AnyComp key={i} {...child} />
    ))}
  </>
)
