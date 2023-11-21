import { FC } from 'react'

import { ClassName, useClassName } from '../hooks/className'
import { useFireEvent, Event } from '../hooks/event'

export interface ButtonProps {
  type: 'Button'
  text: string
  onClick?: Event
  htmlType?: 'button' | 'submit' | 'reset'
  className?: ClassName
}

export const ButtonComp: FC<ButtonProps> = (props) => {
  const { text, onClick, htmlType } = props

  const { fireEvent } = useFireEvent()

  return (
    <button className={useClassName(props)} type={htmlType} onClick={() => fireEvent(onClick)}>
      {text}
    </button>
  )
}
