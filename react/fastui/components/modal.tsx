import { FC } from 'react'

import { ClassName, renderClassName, useClassNameGenerator } from '../hooks/className'
import { PageEvent, useEventListenerToggle } from '../hooks/event'

import { FastProps, RenderChildren } from './index'
import './modal.css'

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
  const { title, body, footer, openTrigger, className } = props

  const [open, toggle] = useEventListenerToggle(openTrigger, props.open)

  return (
    <div className={renderClassName({ 'fu-modal-overlay': true, open })}>
      <div className={useClassNameGenerator(className, props, 'fu-modal-content')}>
        <div className="fu-model-header">
          <h2>{title}</h2>
          <div className="fu-close" onClick={toggle}>
            &times;
          </div>
        </div>
        <div className="fu-modal-body">
          <RenderChildren children={body} />
        </div>
        {footer && (
          <div className="fu-modal-footer">
            <RenderChildren children={footer} />
          </div>
        )}
      </div>
    </div>
  )
}
