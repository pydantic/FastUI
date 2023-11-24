import * as codeStyles from 'react-syntax-highlighter/dist/esm/styles/prism'
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter'

import type { CodeProps } from './Code'

import { useClassName } from '../hooks/className'

export default function (props: CodeProps) {
  const { text, language, codeStyle } = props
  const codeLookup = codeStyle as keyof typeof codeStyles
  const style = (codeStyle && codeStyles[codeLookup]) || codeStyles.coldarkCold
  return (
    <SyntaxHighlighter
      className={useClassName(props)}
      PreTag="div"
      children={text}
      language={language}
      style={style}
    />
  )
}
