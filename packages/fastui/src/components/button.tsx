import { FC } from 'react'

import { ClassName, useClassNameGenerator } from '../hooks/className'
import { useFireEvent, PageEvent, GoToEvent } from '../hooks/event'

export interface ButtonProps {
  type: 'Button'
  text: string
  onClick?: PageEvent | GoToEvent
  htmlType?: 'button' | 'submit' | 'reset'
  className?: ClassName
}

export const ButtonComp: FC<ButtonProps> = (props) => {
  const { className, text, onClick, htmlType } = props

  const { fireEvent } = useFireEvent()

  return (
    <button className={useClassNameGenerator(className, props)} type={htmlType} onClick={() => fireEvent(onClick)}>
      {text}
    </button>
  )
}
