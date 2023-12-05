import { useContext, useState, useEffect, useCallback } from 'react'

import { LocationContext } from './hooks/locationContext'
import { ContextType } from './hooks/eventContext'

export interface PageEvent {
  type: 'page'
  name: string
  pushPath?: string
  context?: ContextType
  clear?: boolean
}

export interface GoToEvent {
  type: 'go-to'
  url?: string
  query?: Record<string, string | number | null>
}

export interface BackEvent {
  type: 'back'
}

export type AnyEvent = PageEvent | GoToEvent | BackEvent

export interface PageEventDetail {
  clear: boolean
  context?: ContextType
}

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
      case 'page': {
        if (event.pushPath) {
          location.gotoCosmetic(event.pushPath)
        }
        const detail: PageEventDetail = { clear: event.clear || false, context: event.context }
        document.dispatchEvent(new CustomEvent(pageEventType(event), { detail }))
        break
      }
      case 'go-to':
        if (event.url) {
          location.goto(event.url)
        }
        if (event.query) {
          location.setQuery(event.query)
        }
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

export function usePageEventListen(
  event?: PageEvent,
  initialContext: ContextType | null = null,
): { eventContext: ContextType | null; clear: () => void } {
  const [eventContext, setEventContext] = useState<ContextType | null>(initialContext)

  const onEvent = useCallback((e: Event) => {
    const { context, clear } = (e as CustomEvent<PageEventDetail>).detail
    if (clear) {
      setEventContext(null)
    } else {
      setEventContext(context ?? {})
    }
  }, [])

  useEffect(() => {
    if (!event) {
      return
    }

    const eventType = pageEventType(event)

    document.addEventListener(eventType, onEvent)
    return () => document.removeEventListener(eventType, onEvent)
  }, [event, onEvent])

  return {
    eventContext,
    clear: useCallback(() => setEventContext(null), []),
  }
}
