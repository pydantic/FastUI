import { FC } from 'react'

import type { Button } from '../models'

import { useClassName } from '../hooks/className'
import { useFireEvent } from '../events'

export const ButtonComp: FC<Button> = (props) => {
  const { text, onClick, htmlType } = props

  const { fireEvent } = useFireEvent()

  return (
    <button className={useClassName(props)} type={htmlType} onClick={() => fireEvent(onClick)}>
      {text}
    </button>
  )
}
