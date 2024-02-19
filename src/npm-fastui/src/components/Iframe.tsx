import { FC } from 'react'

import type { Iframe } from '../models'

export const IframeComp: FC<Iframe> = (props) => {
  const { src, width, height, title, sandbox, srcdoc } = props
  return <iframe src={src} width={width} height={height} title={title} sandbox={sandbox} srcDoc={srcdoc} />
}
