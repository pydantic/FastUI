import { FC, useEffect } from 'react'

import type { Toast } from '../models'

import { usePageEventListen } from '../events'

export const ToastComp: FC<Toast> = (props) => {
  const { title, openTrigger, openContext } = props

  const { fireId, clear } = usePageEventListen(openTrigger, openContext)

  useEffect(() => {
    if (fireId) {
      setTimeout(() => {
        alert(`${title}\n\nNote: modals are not implemented by pure FastUI, implement a component for 'ToastProps'.`)
        clear()
      })
    }
  }, [fireId, title, clear])

  return <></>
}
