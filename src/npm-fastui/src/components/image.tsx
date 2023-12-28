import { FC } from 'react'

import type { Image } from '../models'

import { useClassName } from '../hooks/className'
import { useFireEvent } from '../events'

export const ImageComp: FC<Image> = (props) => {
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
