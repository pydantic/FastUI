import {FC} from 'react'

export interface Text {
  type: 'Text'
  text: string
}

export const TextRender: FC<Text> = ({text}) => (
  <>{text}</>
)
