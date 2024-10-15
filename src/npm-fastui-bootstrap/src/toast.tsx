import { FC } from 'react'
import { components, events, renderClassName, EventContextProvider, models } from 'fastui'
import BootstrapToast from 'react-bootstrap/Toast'
import BootstrapToastContainer from 'react-bootstrap/ToastContainer'

export const Toast: FC<models.Toast> = (props) => {
  const { className, title, body, position, delay, openTrigger, openContext } = props

  const { eventContext, fireId, clear } = events.usePageEventListen(openTrigger, openContext)

  return (
    <EventContextProvider context={eventContext}>
      <BootstrapToastContainer position={position} className="position-fixed bottom-0 end-0 p-3">
        <BootstrapToast
          className={renderClassName(className)}
          show={!!fireId}
          onClose={clear}
          delay={delay}
          autohide={!!delay}
        >
          <BootstrapToast.Header>
            <strong className="me-auto">{title}</strong>
          </BootstrapToast.Header>
          <BootstrapToast.Body>
            <components.AnyCompList propsList={body} />
          </BootstrapToast.Body>
        </BootstrapToast>
      </BootstrapToastContainer>
    </EventContextProvider>
  )
}
