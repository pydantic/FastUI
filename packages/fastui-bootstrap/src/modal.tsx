import { FC } from 'react'
import { components, events, renderClassName } from 'fastui'
import Modal from 'react-bootstrap/Modal'

export const ModalComp: FC<components.ModalProps> = (props) => {
  const { className, title, body, footer, openTrigger } = props

  const [open, toggle] = events.useEventListenerToggle(openTrigger, props.open)

  return (
    <Modal className={renderClassName(className)} show={open} onHide={toggle}>
      <Modal.Header closeButton>
        <Modal.Title>{title}</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <components.RenderChildren children={body} />
      </Modal.Body>
      {footer && (
        <Modal.Footer className="modal-footer">
          <components.RenderChildren children={footer} />
        </Modal.Footer>
      )}
    </Modal>
  )
}
