import { useContext, useState, useEffect, useCallback } from 'react'

import { LocationContext } from './hooks/locationContext'

export interface PageEvent {
  type: 'page'
  name: string
  pushPath?: string
}

export interface GoToEvent {
  type: 'go-to'
  url: string
}

export interface BackEvent {
  type: 'back'
}

export type AnyEvent = PageEvent | GoToEvent | BackEvent

function pageEventType(event: PageEvent): string {
  return `fastui:${event.name}`
}

export function useFireEvent(): { fireEvent: (event?: AnyEvent) => void } {
  const location = useContext(LocationContext)

  function fireEvent(event?: AnyEvent) {
    if (!event) {
      return
    }
    console.debug('firing event', event)
    const { type } = event
    switch (type) {
      case 'page':
        if (event.pushPath) {
          location.gotoCosmetic(event.pushPath)
        }
        document.dispatchEvent(new CustomEvent(pageEventType(event)))
        break
      case 'go-to':
        location.goto(event.url)
        break
      case 'back':
        location.back()
        break
    }
  }

  return { fireEvent }
}

export const loadEvent = 'fastui:load'

export interface LoadEventDetail {
  path?: string
  reloadValue?: number
}

export function fireLoadEvent(detail: LoadEventDetail) {
  document.dispatchEvent(new CustomEvent(loadEvent, { detail }))
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
