import { useContext, FC } from 'react'

import { ErrorContext } from '../hooks/error'
import { useCustomRender } from '../hooks/config'
import { unreachable } from '../tools'

import { TextProps, TextComp } from './text'
import { ParagraphProps, ParagraphComp } from './paragraph'
import { PageTitleProps, PageTitleComp } from './PageTitle'
import { AllDivProps, DivComp, DivProps } from './div'
import { HeadingComp, HeadingProps } from './heading'
import { MarkdownComp, MarkdownProps } from './Markdown'
import { CodeComp, CodeProps } from './Code'
import { FormComp, FormProps, ModelFormProps } from './form'
import {
  FormFieldProps,
  FormFieldInputComp,
  FormFieldBooleanComp,
  FormFieldSelectComp,
  FormFieldSelectSearchComp,
  FormFieldFileComp,
} from './FormField'
import { ButtonComp, ButtonProps } from './button'
import { LinkComp, LinkProps, LinkRender } from './link'
import { LinkListProps, LinkListComp } from './LinkList'
import { NavbarProps, NavbarComp } from './navbar'
import { ModalComp, ModalProps } from './modal'
import { TableComp, TableProps } from './table'
import { PaginationProps, PaginationComp } from './pagination'
import { DetailsProps, DetailsComp } from './details'
import {
  AllDisplayProps,
  DisplayArray,
  DisplayComp,
  DisplayObject,
  DisplayPrimitive,
  DisplayPrimitiveProps,
} from './display'
import { JsonComp, JsonProps } from './Json'
import { ServerLoadComp, ServerLoadProps } from './ServerLoad'
import { IframeComp, IframeProps } from './Iframe'

export type {
  TextProps,
  ParagraphProps,
  PageTitleProps,
  AllDivProps,
  DivProps,
  HeadingProps,
  MarkdownProps,
  CodeProps,
  FormProps,
  ModelFormProps,
  FormFieldProps,
  ButtonProps,
  ModalProps,
  TableProps,
  PaginationProps,
  DetailsProps,
  LinkProps,
  LinkListProps,
  NavbarProps,
  AllDisplayProps,
  DisplayPrimitiveProps,
  JsonProps,
  ServerLoadProps,
  IframeProps,
}

// TODO some better way to export components
export { LinkComp, LinkRender }

export type FastProps =
  | TextProps
  | ParagraphProps
  | PageTitleProps
  | AllDivProps
  | DivProps
  | HeadingProps
  | MarkdownProps
  | CodeProps
  | FormProps
  | ModelFormProps
  | FormFieldProps
  | ButtonProps
  | ModalProps
  | TableProps
  | PaginationProps
  | DetailsProps
  | LinkProps
  | LinkListProps
  | NavbarProps
  | AllDisplayProps
  | JsonProps
  | ServerLoadProps
  | IframeProps

export type FastClassNameProps = Exclude<FastProps, TextProps | AllDisplayProps | ServerLoadProps | PageTitleProps>

export const AnyCompList: FC<{ propsList: FastProps[] }> = ({ propsList }) => (
  <>
    {propsList.map((child, i) => (
      <AnyComp key={i} {...child} />
    ))}
  </>
)

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
      case 'Paragraph':
        return <ParagraphComp {...props} />
      case 'PageTitle':
        return <PageTitleComp {...props} />
      case 'Div':
      case 'Page':
        return <DivComp {...props} />
      case 'Heading':
        return <HeadingComp {...props} />
      case 'Markdown':
        return <MarkdownComp {...props} />
      case 'Code':
        return <CodeComp {...props} />
      case 'Button':
        return <ButtonComp {...props} />
      case 'Link':
        return <LinkComp {...props} />
      case 'LinkList':
        return <LinkListComp {...props} />
      case 'Navbar':
        return <NavbarComp {...props} />
      case 'Form':
      case 'ModelForm':
        return <FormComp {...props} />
      case 'FormFieldInput':
        return <FormFieldInputComp {...props} />
      case 'FormFieldBoolean':
        return <FormFieldBooleanComp {...props} />
      case 'FormFieldFile':
        return <FormFieldFileComp {...props} />
      case 'FormFieldSelect':
        return <FormFieldSelectComp {...props} />
      case 'FormFieldSelectSearch':
        return <FormFieldSelectSearchComp {...props} />
      case 'Modal':
        return <ModalComp {...props} />
      case 'Table':
        return <TableComp {...props} />
      case 'Pagination':
        return <PaginationComp {...props} />
      case 'Details':
        return <DetailsComp {...props} />
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
      case 'ServerLoad':
        return <ServerLoadComp {...props} />
      case 'Iframe':
        return <IframeComp {...props} />
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
