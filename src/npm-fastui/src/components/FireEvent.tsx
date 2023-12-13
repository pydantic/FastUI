import { FC, useEffect, useRef } from 'react'

import { AnyEvent, useFireEvent } from '../events'
import { ClassName } from '../hooks/className'

export interface FireEventProps {
  type: 'FireEvent'
  event: AnyEvent
  message?: string
  className?: ClassName
}

export const FireEventComp: FC<FireEventProps> = ({ event, message }) => {
  const { fireEvent } = useFireEvent()
  const fireEventRef = useRef(fireEvent)

  useEffect(() => {
    fireEventRef.current = fireEvent
  }, [fireEvent])

  useEffect(() => {
    fireEventRef.current(event)
  }, [event, fireEventRef])

  return <>{message}</>
}
