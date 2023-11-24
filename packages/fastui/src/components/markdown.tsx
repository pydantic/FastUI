import { FC, MouseEventHandler, ReactNode } from 'react'
import Markdown, { Components } from 'react-markdown'
import remarkGfm from 'remark-gfm'
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter'
import * as codeStyles from 'react-syntax-highlighter/dist/esm/styles/prism'

import { ClassName, useClassName } from '../hooks/className'
import { useFireEvent, AnyEvent } from '../hooks/events'

export interface MarkdownProps {
  type: 'Markdown'
  text: string
  codeStyle?: keyof typeof codeStyles
  className?: ClassName
}

export const MarkdownComp: FC<MarkdownProps> = (props) => {
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
    <Markdown className={useClassName(props)} remarkPlugins={[remarkGfm]} components={components}>
      {text}
    </Markdown>
  )
}

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

interface CodeProps {
  children: ReactNode
  className?: string
  codeStyle?: keyof typeof codeStyles
}

const MarkdownCode: FC<CodeProps> = ({ children, className, codeStyle }) => {
  const match = /language-(\w+)/.exec(className || '')
  if (match) {
    const style = (codeStyle && codeStyles[codeStyle]) || codeStyles.coldarkCold
    return (
      <SyntaxHighlighter
        PreTag="div"
        children={String(children).replace(/\n$/, '')}
        language={match[1]}
        style={style}
      />
    )
  } else {
    return <code className={className}>{children}</code>
  }
}
