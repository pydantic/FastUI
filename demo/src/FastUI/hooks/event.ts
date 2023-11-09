import { useContext, useState, useEffect, useCallback } from 'react'
import { LocationContext } from './locationContext'

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

export function useFireEvent(): { fireEvent: (event?: PageEvent | GoToEvent) => void } {
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

export function useEventListenerToggle(event?: PageEvent, initialState = false): [boolean, () => void] {
  const [state, setState] = useState(initialState)

  const toggle = useCallback(() => setState((state) => !state), [])

  useEffect(() => {
    if (!event) {
      return
    }

    const eventType = pageEventType(event)

    document.addEventListener(eventType, toggle)
    return () => document.removeEventListener(eventType, toggle)
  }, [event, toggle])

  return [state, toggle]
}
