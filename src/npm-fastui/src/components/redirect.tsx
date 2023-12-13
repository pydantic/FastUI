import { FC, useEffect, useState } from 'react'

import { AnyEvent, useFireEvent } from '../events'
import { ClassName } from '../hooks/className'

export interface RedirectProps {
  type: 'Redirect'
  event: AnyEvent
  message?: string
  className?: ClassName
}

export const RedirectComp: FC<RedirectProps> = ({ event, message }) => {
  const [effectEvent] = useState(event)

  const { fireEvent } = useFireEvent()

  useEffect(() => {
    fireEvent(effectEvent)
  }, [effectEvent, fireEvent])

  return <>{message}</>
}
