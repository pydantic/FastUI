import { FC, useEffect } from 'react'

import type { Modal } from '../models'

import { usePageEventListen } from '../events'

export const ModalComp: FC<Modal> = (props) => {
  const { title, openTrigger, openContext } = props

  const { fireId, clear } = usePageEventListen(openTrigger, openContext)

  useEffect(() => {
    if (fireId) {
      setTimeout(() => {
        alert(`${title}\n\nNote: modals are not implemented by pure FastUI, implement a component for 'ModalProps'.`)
        clear()
      })
    }
  }, [fireId, title, clear])

  return <></>
}
