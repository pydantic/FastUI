import { useCallback, useContext, useEffect } from 'react'

import { ErrorContext } from './hooks/error'

export const AUTH_TOKEN_KEY = 'fastui-auth-token'

export function useRequest(): (args: RequestArgs) => Promise<[number, any]> {
  const { setError } = useContext(ErrorContext)

  return useCallback(
    async (args: RequestArgs) => {
      try {
        return await request(args)
      } catch (e) {
        setError({ title: 'Request Error', description: (e as any)?.message })
        throw e
      }
    },
    [setError],
  )
}

export function useSSE(url: string, onMessage: (data: any) => void): void {
  useEffect(() => {
    const source = new EventSource(url)
    source.onmessage = (e) => {
      const data = JSON.parse(e.data)
      onMessage(data)
    }
    source.onerror = (e) => {
      // we don't raise an error her as this can happen when the server is restarted
      console.debug('SSE error', e)
    }
    const cleanup = () => {
      source.onerror = null
      source.close()
    }
    window.addEventListener('beforeunload', cleanup)
    return () => {
      window.removeEventListener('beforeunload', cleanup)
      cleanup()
    }
  }, [url, onMessage])
}

export interface RequestArgs {
  url: string
  method?: 'GET' | 'POST' | 'PUT' | 'DELETE'
  // defaults to 200
  expectedStatus?: number[]
  query?: Record<string, string> | URLSearchParams
  json?: Record<string, any>
  formData?: FormData
  headers?: Record<string, string> | Headers
}

class RequestError extends Error {
  status: number

  constructor(message: string, status: number) {
    super(message)
    this.status = status
    this.name = 'RequestError'
  }
}

async function request({
  url,
  method,
  headers,
  query,
  json,
  expectedStatus,
  formData,
}: RequestArgs): Promise<[number, any]> {
  const init: RequestInit = {}

  let contentType = null
  if (json) {
    init.body = JSON.stringify(json)
    contentType = 'application/json'
    method = method ?? 'POST'
  } else if (formData) {
    // don't set content-type, let the browser set it
    init.body = formData
    method = method ?? 'POST'
  }

  if (query) {
    const searchParams = new URLSearchParams(query)
    url = `${url}?${searchParams.toString()}`
  }

  init.headers = new Headers(headers)
  if (contentType && !init.headers.get('Content-Type')) {
    init.headers.set('Content-Type', contentType)
  }

  const authToken = sessionStorage.getItem(AUTH_TOKEN_KEY)
  if (authToken) {
    // we use a custom auth-schema as well-known values like `Basic` and `Bearer` are not correct here
    init.headers.set('Authorization', `Token ${authToken}`)
  }

  if (method) {
    init.method = method
  }

  let response
  try {
    response = await fetch(url, init)
  } catch (e) {
    throw new RequestError('fetch failed', 0)
  }

  const { status } = response
  if (!responseOk(response, expectedStatus)) {
    let detail: null | string = null
    const content = await response.text()
    try {
      const jsonData = JSON.parse(content)
      console.warn(`${url} -> ${status} JSON:`, jsonData)
      if (typeof jsonData.detail === 'string') {
        detail = jsonData.detail
      }
    } catch (e) {
      console.warn(`${url} -> ${status} content:`, content)
      detail = content
    }
    const msg = `${detail || response.statusText} (${status})`
    throw new RequestError(msg, status)
  }

  let data
  try {
    data = await response.json()
  } catch (e) {
    console.warn(`${url} -> ${status} response not valid JSON`)
    throw new RequestError('Response not valid JSON', status)
  }
  console.debug(`${url} -> ${status} JSON:`, data)
  return [status, data]
}

function responseOk(response: Response, expectedStatus?: number[]) {
  if (expectedStatus) {
    return expectedStatus.includes(response.status)
  } else {
    return response.ok
  }
}

export function unreachable(msg: string, unexpectedValue: never, args?: any) {
  console.warn(msg, { unexpectedValue }, args)
}

type Callable = (...args: any[]) => void

export function debounce<C extends Callable>(fn: C, delay: number): C {
  let timerId: any

  // @ts-expect-error - functions are contravariant, so this should be fine, no idea how to satisfy TS though
  return (...args: any[]) => {
    clearTimeout(timerId)
    timerId = setTimeout(() => fn(...args), delay)
  }
}

export async function sleep(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms))
}

// usage `as_title('what_ever') > 'What Ever'`
export const asTitle = (s: string): string => s.replace(/[_-]/g, ' ').replace(/(_|\b)\w/g, (l) => l.toUpperCase())

export const slugify = (s: string): string =>
  s
    .toLowerCase()
    .replace(/\s+/g, '-') // Replace spaces with -
    .replace(/[^\w-]+/g, '') // Remove all non-word characters
    .replace(/--+/g, '-') // Replace multiple - with single -
    .replace(/^-+/, '') // Trim - from start of text
    .replace(/-+$/, '') // Trim - from end of text
