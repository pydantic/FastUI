import { FC } from 'react'
import { components, events, renderClassName, EventContextProvider } from 'fastui'
import BootstrapModal from 'react-bootstrap/Modal'

export const Modal: FC<components.ModalProps> = (props) => {
  const { className, title, body, footer, openTrigger, openContext } = props

  const { eventContext, clear } = events.usePageEventListen(openTrigger, openContext)

  return (
    <EventContextProvider context={eventContext}>
      <BootstrapModal className={renderClassName(className)} show={!!eventContext} onHide={clear}>
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
    </EventContextProvider>
  )
}
