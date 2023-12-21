import { FC } from 'react'

import type { Video } from '../models'

export const VideoComp: FC<Video> = (props) => {
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
