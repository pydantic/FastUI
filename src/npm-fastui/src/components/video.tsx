import { FC } from 'react'

import { ClassName } from '../hooks/className'
export interface VideoProps {
  type: 'Video'
  sources: string[]
  autoplay?: boolean
  controls?: boolean
  loop?: boolean
  muted?: boolean
  poster?: string
  width?: string | number
  height?: string | number
  className?: ClassName
}

export const VideoComp: FC<VideoProps> = (props) => {
  const { sources, autoplay, controls, loop, muted, poster, width, height } = props
  return (
    <video
      autoPlay={autoplay}
      controls={controls}
      loop={loop}
      muted={muted}
      poster={poster}
      width={width}
      height={height}
    >
      {sources.map((src, i) => (
        <source key={i} src={src} />
      ))}
    </video>
  )
}
