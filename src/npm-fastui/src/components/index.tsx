import { useContext, FC } from 'react'

import type { FastProps, Display, Text, ServerLoad, PageTitle, FireEvent } from '../models'

import { ErrorContext } from '../hooks/error'
import { useCustomRender } from '../hooks/config'
import { unreachable } from '../tools'

import { TextComp } from './text'
import { ParagraphComp } from './paragraph'
import { PageTitleComp } from './PageTitle'
import { DivComp } from './div'
import { HeadingComp } from './heading'
import { MarkdownComp } from './Markdown'
import { CodeComp } from './Code'
import { FormComp } from './form'
import {
  FormFieldInputComp,
  FormFieldBooleanComp,
  FormFieldSelectComp,
  FormFieldSelectSearchComp,
  FormFieldFileComp,
} from './FormField'
import { ButtonComp } from './button'
import { LinkComp, LinkRender } from './link'
import { LinkListComp } from './LinkList'
import { NavbarComp } from './navbar'
import { ModalComp } from './modal'
import { TableComp } from './table'
import { PaginationComp } from './pagination'
import { DetailsComp } from './details'
import { DisplayComp } from './display'
import { JsonComp } from './Json'
import { FooterComp } from './footer'
import { ServerLoadComp } from './ServerLoad'
import { ImageComp } from './image'
import { IframeComp } from './Iframe'
import { VideoComp } from './video'
import { FireEventComp } from './FireEvent'
import { CustomComp } from './Custom'

// TODO some better way to export components
export {
  TextComp,
  ParagraphComp,
  PageTitleComp,
  DivComp,
  HeadingComp,
  MarkdownComp,
  CodeComp,
  FormComp,
  FormFieldInputComp,
  FormFieldBooleanComp,
  FormFieldSelectComp,
  FormFieldSelectSearchComp,
  FormFieldFileComp,
  ButtonComp,
  LinkComp,
  LinkListComp,
  NavbarComp,
  ModalComp,
  TableComp,
  PaginationComp,
  DetailsComp,
  DisplayComp,
  JsonComp,
  FooterComp,
  ServerLoadComp,
  ImageComp,
  IframeComp,
  VideoComp,
  FireEventComp,
  CustomComp,
  LinkRender,
}

export type FastClassNameProps = Exclude<FastProps, Text | Display | ServerLoad | PageTitle | FireEvent>

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
      case 'Footer':
        return <FooterComp {...props} />
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
      case 'JSON':
        return <JsonComp {...props} />
      case 'ServerLoad':
        return <ServerLoadComp {...props} />
      case 'Image':
        return <ImageComp {...props} />
      case 'Iframe':
        return <IframeComp {...props} />
      case 'Video':
        return <VideoComp {...props} />
      case 'FireEvent':
        return <FireEventComp {...props} />
      case 'Custom':
        return <CustomComp {...props} />
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
