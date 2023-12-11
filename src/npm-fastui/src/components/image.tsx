import { FC } from 'react'

import { ClassName, useClassName } from '../hooks/className'
import { useFireEvent, AnyEvent } from '../events'

export interface ImageProps {
  type: 'Image'
  src: string
  alt?: string
  /** @TJS-type ["string", "integer"] */
  width?: number | string
  /** @TJS-type ["string", "integer"] */
  height?: number | string
  referrerPolicy?:
    | 'no-referrer'
    | 'no-referrer-when-downgrade'
    | 'origin'
    | 'origin-when-cross-origin'
    | 'same-origin'
    | 'strict-origin'
    | 'strict-origin-when-cross-origin'
    | 'unsafe-url'
  loading?: 'eager' | 'lazy'
  onClick?: AnyEvent
  className?: ClassName
}

export const ImageComp: FC<ImageProps> = (props) => {
  const { src, alt, width, height, referrerPolicy, loading, onClick } = props

  const { fireEvent } = useFireEvent()

  return (
    <img
      className={useClassName(props)}
      src={src}
      alt={alt}
      width={width}
      height={height}
      referrerPolicy={referrerPolicy}
      loading={loading}
      onClick={() => fireEvent(onClick)}
    />
  )
}
