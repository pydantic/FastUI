import { FC, MouseEventHandler, ReactNode } from 'react'
import ReactMarkdown, { Components } from 'react-markdown'
import remarkGfm from 'remark-gfm'

import type { Markdown, Code, AnyEvent } from '../models'

import { useClassName } from '../hooks/className'
import { useFireEvent } from '../events'
import { useCustomRender } from '../hooks/config'

import { CodeComp } from './Code'

const MarkdownComp: FC<Markdown> = (props) => {
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
    <ReactMarkdown
      className={useClassName(props, { dft: 'fastui-markdown' })}
      remarkPlugins={[remarkGfm]}
      components={components}
    >
      {text}
    </ReactMarkdown>
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
  const codeProps: Code = {
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
