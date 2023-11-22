import { FC, lazy } from 'react'

import { ClassName, renderClassName, useClassName } from '../hooks/className'
import { PageEvent, useEventListenerToggle } from '../hooks/events'

import { FastProps, AnyCompList } from './index'

export interface ModalProps {
  type: 'Modal'
  title: string
  body: FastProps[]
  footer?: FastProps[]
  openTrigger?: PageEvent
  open?: boolean
  className?: ClassName
}

// @ts-expect-error typescript doesn't understand `./modal.css`
const DefaultCss = lazy(() => import('./modal.css'))

export const ModalComp: FC<ModalProps> = (props) => {
  const { title, body, footer, openTrigger } = props

  const [open, toggle] = useEventListenerToggle(openTrigger, props.open)

  return (
    <>
      <DefaultCss />
      <div className={renderClassName({ 'fu-modal-overlay': true, open })} tabIndex={-1}>
        <div className={useClassName(props, { dft: 'fu-modal-content' })}>
          <div className="fu-model-header">
            <h2>{title}</h2>
            <div className="fu-close" onClick={toggle}>
              &times;
            </div>
          </div>
          <div className="fu-modal-body">
            <AnyCompList propsList={body} />
          </div>
          {footer && (
            <div className="fu-modal-footer">
              <AnyCompList propsList={footer} />
            </div>
          )}
        </div>
      </div>
    </>
  )
}
