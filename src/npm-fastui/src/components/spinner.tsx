import { FC } from 'react'

import type { Spinner } from '../models'

import { useClassName } from '../hooks/className'

export const SpinnerComp: FC<Spinner> = (props) => {
  const { text } = props

  return (
    <div className={useClassName(props, { dft: 'fastui-spinner' })}>
      <div className={useClassName(props, { el: 'text' })}>{text}</div>
      <div className={useClassName(props, { el: 'animation' })}>
        <div className="fastui-spinner-animation">loading...</div>
      </div>
    </div>
  )
}
