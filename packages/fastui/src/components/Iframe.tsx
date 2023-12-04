import { FC } from 'react'

import { ClassName } from '../hooks/className'

export interface IframeProps {
  type: 'Iframe'
  src: string
  width?: string | number
  height?: string | number
  title?: string
  className?: ClassName
}

export const IframeComp: FC<IframeProps> = (props) => {
  const { src, width, height, title } = props
  return <iframe src={src} width={width} height={height} title={title} />
}
