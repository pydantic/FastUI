import { FC, MouseEventHandler, ReactNode } from 'react'
import Markdown, { Components } from 'react-markdown'
import remarkGfm from 'remark-gfm'

import type { MarkdownProps } from './Markdown'

import { useClassName } from '../hooks/className'
import { useFireEvent, AnyEvent } from '../events'
import { useCustomRender } from '../hooks/config'

import { CodeProps, CodeComp } from './Code'

const MarkdownComp: FC<MarkdownProps> = (props) => {
  const { text, codeStyle } = props
  const components: Components = {
    a({ children, href }) {
      return <MarkdownA href={href}>{children}</MarkdownA>
    },
    code({ children, className }) {
      return (
        <MarkdownCode className={className} codeStyle={codeStyle}>
          {children}
        </MarkdownCode>
      )
    },
  }

  return (
    <Markdown
      className={useClassName(props, { dft: 'fastui-markdown' })}
      remarkPlugins={[remarkGfm]}
      components={components}
    >
      {text}
    </Markdown>
  )
}

export default MarkdownComp

const MarkdownA: FC<{ children: ReactNode; href?: string }> = ({ children, href }) => {
  const { fireEvent } = useFireEvent()

  let onClick: AnyEvent | undefined
  let preventDefault = true
  if (!href) {
    href = '#'
  } else if (href === '!back') {
    href = '#'
    onClick = { type: 'back' }
  } else if (href.startsWith('!')) {
    onClick = { type: 'page', name: href.slice(1) }
    href = '#'
  } else if (href.startsWith('#')) {
    preventDefault = href.length === 1
  } else {
    onClick = { type: 'go-to', url: href }
  }

  const clickHandler: MouseEventHandler<HTMLAnchorElement> = (e) => {
    if (preventDefault) {
      e.preventDefault()
      fireEvent(onClick)
    }
  }

  return (
    <a href={href} onClick={clickHandler}>
      {children}
    </a>
  )
}

interface MarkdownCodeProps {
  children: ReactNode
  className?: string
  codeStyle?: string
}

const MarkdownCode: FC<MarkdownCodeProps> = ({ children, className, codeStyle }) => {
  const match = /language-(\w+)/.exec(className || '')
  if (match) {
    return (
      <MarkdownCodeHighlight codeStyle={codeStyle} language={match[1]}>
        {children}
      </MarkdownCodeHighlight>
    )
  } else {
    return <code className={className}>{children}</code>
  }
}

interface MarkdownCodeHighlightProps {
  children: ReactNode
  language?: string
  codeStyle?: string
}

const MarkdownCodeHighlight: FC<MarkdownCodeHighlightProps> = ({ children, codeStyle, language }) => {
  const codeProps: CodeProps = {
    type: 'Code',
    text: String(children).replace(/\n$/, ''),
    language,
    codeStyle,
  }
  const CustomRenderComp = useCustomRender(codeProps)
  if (CustomRenderComp) {
    return <CustomRenderComp />
  } else {
    return <CodeComp {...codeProps} />
  }
}
