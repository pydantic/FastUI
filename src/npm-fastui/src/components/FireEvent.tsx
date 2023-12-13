import { FC, useEffect, useRef } from 'react'

import { AnyEvent, useFireEvent } from '../events'
import { ClassName } from '../hooks/className'

export interface FireEventProps {
  type: 'FireEvent'
  event: AnyEvent
  message?: string
  // className is not used, but it's here to satisfy ClassName hooks type checks
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
