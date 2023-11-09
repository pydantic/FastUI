import { FC } from 'react'
import { ClassName, useClassNameGenerator } from '../hooks/className'
import { useFireEvent, PageEvent, GoToEvent } from '../hooks/event'

export interface ButtonProps {
  type: 'Button'
  text: string
  onClick?: PageEvent | GoToEvent
  className?: ClassName
}

export const ButtonComp: FC<ButtonProps> = (props) => {
  const { className, text, onClick } = props

  const { fireEvent } = useFireEvent()

  return (
    <button className={useClassNameGenerator(className, props)} onClick={() => fireEvent(onClick)}>
      {text}
    </button>
  )
}
