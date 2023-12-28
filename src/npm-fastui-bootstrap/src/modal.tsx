import { FC } from 'react'
import { models, components, events, renderClassName, EventContextProvider } from 'fastui'
import BootstrapModal from 'react-bootstrap/Modal'

export const Modal: FC<models.Modal> = (props) => {
  const { className, title, body, footer, openTrigger, openContext } = props

  const { eventContext, fireId, clear } = events.usePageEventListen(openTrigger, openContext)

  return (
    <EventContextProvider context={eventContext}>
      <BootstrapModal className={renderClassName(className)} show={!!fireId} onHide={clear}>
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
