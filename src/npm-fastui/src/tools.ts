import { useCallback, useContext, useEffect } from 'react'
import { fetchEventSource, EventStreamContentType } from '@microsoft/fetch-event-source'

import { ErrorContext } from './hooks/error'

export const AUTH_TOKEN_KEY = 'fastui-auth-token'
export type Method = 'GET' | 'POST' | 'PATCH' | 'PUT' | 'DELETE'

export function useRequest(): (args: RequestArgs) => Promise<[number, any]> {
  const { setError } = useContext(ErrorContext)

  return useCallback(
    async (args: RequestArgs) => {
      try {
        return await request(args)
      } catch (e) {
        const title = 'Request Error'
        if (e instanceof RequestError) {
          setError({ title, description: e.message, statusCode: e.status })
        } else {
          setError({ title, description: (e as any)?.message })
        }
        throw e
      }
    },
    [setError],
  )
}

export interface RequestArgs {
  url: string
  method?: Method
  // defaults to 200
  expectedStatus?: number[]
  query?: Record<string, string> | URLSearchParams
  json?: Record<string, any>
  formData?: FormData
  headers?: Record<string, string> | Headers
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

  const authHeader = getAuthHeader()
  if (authHeader) {
    init.headers.set(authHeader.key, authHeader.value)
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

  const status = await checkResponse(url, response, expectedStatus)
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

export function useSSE(url: string, onMessage: (data: any) => void, method?: Method, retry?: number): void {
  const { setError } = useContext(ErrorContext)

  useEffect(() => {
    let stop = false
    const headers: Record<string, string> = {}
    const authHeader = getAuthHeader()
    if (authHeader) {
      headers[authHeader.key] = authHeader.value
    }
    fetchEventSource(url, {
      method,
      headers,
      onopen: async function (response) {
        const status = await checkResponse(url, response, [200])
        const ct = response.headers.get('content-type')
        if (!ct || !ct.startsWith(EventStreamContentType)) {
          console.warn(`${url} -> ${status} content-type "${ct}" != "${EventStreamContentType}"`)
          throw new RequestError('Response not valid event stream', status)
        }
        console.debug(`${url} -> ${status} event stream`)
        // ok
      },
      onmessage(e) {
        if (stop) {
          throw new SSEStopError()
        }
        const data = JSON.parse(e.data)
        onMessage(data)
      },
      onclose() {
        if (typeof retry === 'number') {
          throw new SSERetryError()
        } else {
          throw new SSEStopError()
        }
      },
      onerror(e) {
        if (e instanceof SSERetryError) {
          console.debug('SSE retrying')
          return retry
        } else {
          throw e
        }
      },
    }).catch((e) => {
      if (e instanceof SSEStopError) {
        // do nothing, this is fine
        return
      }
      const title = 'Request Error'
      if (e instanceof RequestError) {
        setError({ title, description: e.message, statusCode: e.status })
      } else {
        setError({ title, description: (e as any)?.message })
      }
      throw e
    })

    return () => {
      stop = true
    }
  }, [setError, url, onMessage, method, retry])
}

class SSERetryError extends Error {}
class SSEStopError extends Error {}

class RequestError extends Error {
  status: number

  constructor(message: string, status: number) {
    super(message)
    this.status = status
    this.name = 'RequestError'
  }
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

export const deepLookup = (obj: object, path: string): any =>
  path.split('.').reduce((o: any, p) => (o && o[p] !== undefined ? o[p] : undefined), obj)

function getAuthHeader(): { key: string; value: string } | undefined {
  const authToken = localStorage.getItem(AUTH_TOKEN_KEY)
  if (authToken) {
    // we use a custom auth-schema as well-known values like `Basic` and `Bearer` are not correct here
    return { key: 'Authorization', value: `Token ${authToken}` }
  }
}

async function checkResponse(url: string, response: Response, expectedStatus: number[] | undefined): Promise<number> {
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
  return status
}
