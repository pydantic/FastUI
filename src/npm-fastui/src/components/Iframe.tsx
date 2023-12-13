import { FC } from 'react'

import { ClassName } from '../hooks/className'

export interface IframeProps {
  type: 'Iframe'
  /**
   * @format uri
   * @maxLength 2083
   * @minLength 1
   */
  src: string
  /** @TJS-type ["string", "integer"] */
  width?: string | number
  /** @TJS-type ["string", "integer"] */
  height?: string | number
  title?: string
  className?: ClassName
}

export const IframeComp: FC<IframeProps> = (props) => {
  const { src, width, height, title } = props
  return <iframe src={src} width={width} height={height} title={title} />
}
