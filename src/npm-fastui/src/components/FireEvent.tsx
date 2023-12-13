import { FC, useEffect, useState } from 'react'

import { AnyEvent, useFireEvent } from '../events'
import { ClassName } from '../hooks/className'

export interface FireEventProps {
  type: 'FireEvent'
  event: AnyEvent
  message?: string
  className?: ClassName
}

export const FireEventComp: FC<FireEventProps> = ({ event, message }) => {
  const [effectEvent] = useState(event)

  const { fireEvent } = useFireEvent()

  useEffect(() => {
    fireEvent(effectEvent)
  }, [effectEvent, fireEvent])

  return <>{message}</>
}
