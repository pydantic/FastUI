import { FC, useEffect } from 'react'

import type { FireEvent } from '../models'

import { useFireEvent } from '../events'

export const FireEventComp: FC<FireEvent> = ({ event, message }) => {
  const { fireEvent } = useFireEvent()

  useEffect(() => {
    // debounce the event so changes to fireEvent (from location changes) don't trigger the event many times
    const clear = setTimeout(() => fireEvent(event), 50)
    return () => clearTimeout(clear)
  }, [fireEvent, event])

  return <>{message}</>
}
