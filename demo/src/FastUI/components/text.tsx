import { FC } from 'react'

export interface TextProps {
  type: 'Text'
  text: string
}

export const TextComp: FC<TextProps> = ({ text }) => <>{text}</>
