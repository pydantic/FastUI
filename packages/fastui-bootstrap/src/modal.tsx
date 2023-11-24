import { FC } from 'react'
import { components, events, renderClassName } from 'fastui'
import BootstrapModal from 'react-bootstrap/Modal'

export const Modal: FC<components.ModalProps> = (props) => {
  const { className, title, body, footer, openTrigger } = props

  const [open, toggle] = events.useEventListenerToggle(openTrigger, props.open)

  return (
    <BootstrapModal className={renderClassName(className)} show={open} onHide={toggle}>
      <BootstrapModal.Header closeButton>
        <BootstrapModal.Title>{title}</BootstrapModal.Title>
      </BootstrapModal.Header>
      <BootstrapModal.Body>
        <components.AnyCompList propsList={body} />
      </BootstrapModal.Body>
      {footer && (
        <BootstrapModal.Footer className="modal-footer">
          <components.AnyCompList propsList={footer} />
        </BootstrapModal.Footer>
      )}
    </BootstrapModal>
  )
}
