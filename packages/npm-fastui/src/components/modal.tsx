import { FC, useEffect } from 'react'

import type { FastProps } from './index'
import type { ContextType } from '../hooks/eventContext'

import { ClassName } from '../hooks/className'
import { PageEvent, usePageEventListen } from '../events'

export interface ModalProps {
  type: 'Modal'
  title: string
  body: FastProps[]
  footer?: FastProps[]
  openTrigger?: PageEvent
  openContext?: ContextType
  className?: ClassName
}

export const ModalComp: FC<ModalProps> = (props) => {
  const { title, openTrigger, openContext } = props

  const { eventContext, clear } = usePageEventListen(openTrigger, openContext)
  const open = !!eventContext

  useEffect(() => {
    if (open) {
      setTimeout(() => {
        alert(`${title}\n\nNote: modals are not implemented by pure FastUI, implement a component for 'ModalProps'.`)
        clear()
      })
    }
  }, [open, title, clear])

  return <></>
}
