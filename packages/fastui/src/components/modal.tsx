import { FC, useEffect } from 'react'

import { ClassName } from '../hooks/className'
import { PageEvent, useEventListenerToggle } from '../hooks/events'

import { FastProps } from './index'

export interface ModalProps {
  type: 'Modal'
  title: string
  body: FastProps[]
  footer?: FastProps[]
  openTrigger?: PageEvent
  open?: boolean
  className?: ClassName
}

export const ModalComp: FC<ModalProps> = (props) => {
  const { title, openTrigger } = props

  const [open, toggle] = useEventListenerToggle(openTrigger, props.open)

  useEffect(() => {
    if (open) {
      setTimeout(() => {
        alert(`${title}\n\nNote: modals are not implemented by pure FastUI, implement a component for 'ModalProps'.`)
        toggle()
      })
    }
  }, [open, title, toggle])

  return <></>
}
