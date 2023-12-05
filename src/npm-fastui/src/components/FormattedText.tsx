import { FC } from 'react'

import { ClassName } from '../hooks/className'

export interface FormattedTextProps {
  type: 'FormattedText'
  text: string
  textFormat?: 'bold' | 'italic' | 'underline' | 'strikethrough'
  color?: string
  backgroundColor?: string
  className?: ClassName
}

export const FormattedTextComp: FC<FormattedTextProps> = (props) => {
  const { text, textFormat, color, backgroundColor } = props

  const style = {
    backgroundColor,
    color,
    fontWeight: textFormat === 'bold' ? 'bold' : 'normal',
    fontStyle: textFormat === 'italic' ? 'italic' : 'normal',
    textDecoration:
      textFormat === 'underline' ? 'underline' : textFormat === 'strikethrough' ? 'line-through' : 'none',
  }

  return <span style={style}>{text}</span>
}
