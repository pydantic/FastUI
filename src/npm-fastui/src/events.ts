import { useContext, useState, useEffect, useCallback } from 'react'

import type { PageEvent, AnyEvent } from './models'

import { LocationContext } from './hooks/locationContext'
import { ContextType } from './hooks/eventContext'
import { AUTH_TOKEN_KEY } from './tools'

export interface PageEventDetail {
  clear: boolean
  context?: ContextType
}

function pageEventType(event: PageEvent): string {
  return `fastui:${event.name}`
}

export function useFireEvent(): { fireEvent: (event?: AnyEvent) => void } {
  const location = useContext(LocationContext)

  function fireEventImpl(event?: AnyEvent) {
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
      case 'auth':
        if (event.token) {
          sessionStorage.setItem(AUTH_TOKEN_KEY, event.token)
        } else {
          sessionStorage.removeItem(AUTH_TOKEN_KEY)
        }
        if (event.url) {
          location.goto(event.url)
        }
        break
      case 'back':
        location.back()
        break
    }
  }

  const fireEvent = useCallback(fireEventImpl, [location])

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

interface EventDetails {
  eventContext: ContextType | null
  fireId: string | null
  clear: () => void
}

export function usePageEventListen(event?: PageEvent, initialContext: ContextType | null = null): EventDetails {
  const [eventContext, setEventContext] = useState<ContextType | null>(initialContext)
  const [fireId, setFireId] = useState<string | null>(null)

  const eventType = event && pageEventType(event)

  useEffect(() => {
    if (!eventType) {
      setEventContext(null)
      setFireId(null)
      return
    }

    const onEvent = (e: Event) => {
      console.log('event:', e)
      const event = e as CustomEvent<PageEventDetail>
      const { context, clear } = event.detail
      if (clear) {
        setEventContext(null)
        setFireId(null)
      } else {
        setEventContext(context || {})
        setFireId(`${event.type}:${event.timeStamp}`)
      }
    }

    document.addEventListener(eventType, onEvent)
    return () => document.removeEventListener(eventType, onEvent)
  }, [eventType])

  return {
    eventContext,
    fireId,
    clear: useCallback(() => setEventContext(null), []),
  }
}
