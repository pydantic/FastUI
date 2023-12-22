import { FC, useEffect, useRef } from 'react'

import type { FireEvent } from '../models'

import { useFireEvent } from '../events'

export const FireEventComp: FC<FireEvent> = ({ event, message }) => {
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
