import { FC } from 'react'

import type { Paragraph } from '../models'

import { useClassName } from '../hooks/className'

export const ParagraphComp: FC<Paragraph> = (props) => {
  const { text } = props

  return <p className={useClassName(props)}>{text}</p>
}
