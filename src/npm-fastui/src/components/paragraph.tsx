import { FC } from 'react'

import { ClassName, useClassName } from '../hooks/className'

export interface ParagraphProps {
  type: 'Paragraph'
  text: string
  className?: ClassName
}

export const ParagraphComp: FC<ParagraphProps> = (props) => {
  const { text } = props

  return <p className={useClassName(props)}>{text}</p>
}
