import {LocationContext} from './locationContext'
import {useContext} from 'react'

export interface PageEvent {
  type: 'page'
  name: string
}

export interface GoToEvent {
  type: 'go-to'
  url: string
}

function pageEventType(event: PageEvent): string {
  return `fastui:${event.name}`
}

export function useFireEvent(): {fireEvent: (event?: PageEvent | GoToEvent) => void} {
  const location = useContext(LocationContext)

  function fireEvent(event?: PageEvent | GoToEvent) {
    if (!event) {
      return
    }
    console.debug('firing event', event)
    const { type } = event
    switch (type) {
      case 'page':
        document.dispatchEvent(new CustomEvent(pageEventType(event)))
        break
      case 'go-to':
        location.goto(event.url)
        break
    }
  }

  return { fireEvent }
}
