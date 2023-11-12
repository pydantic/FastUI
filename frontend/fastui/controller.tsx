import { useContext, useEffect, useState } from 'react'

import type { FastUIProps } from './index'

import { FastProps, AnyComp } from './components'
import { DefaultLoading } from './DefaultLoading'
import { LocationContext } from './hooks/locationContext'
import { ErrorContext } from './hooks/error'

interface Request {
  url: string
  method?: 'GET' | 'POST' | 'PUT' | 'DELETE'
  body?: Record<string, any>
  headers?: Record<string, string>
}

type Props = Omit<FastUIProps, 'defaultClassName' | 'OnError' | 'customRender'>

const request = async ({ url, method, headers, body }: Request): Promise<FastProps> => {
  const init: RequestInit = {}
  if (method) {
    init.method = method
  }

  if (body) {
    init.body = JSON.stringify(body)
    headers = headers ?? {}
    headers['Content-Type'] = 'application/json'
  }

  if (headers) {
    init.headers = headers
  }

  let response
  try {
    response = await fetch(url, init)
  } catch (e) {
    throw new Error('fetch failed')
  }

  const { status } = response
  if (!response.ok) {
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
    throw new Error(msg)
  }

  let data
  try {
    data = await response.json()
  } catch (e) {
    console.warn(`${url} -> ${status} response not valid JSON`)
    throw new Error('Response not valid JSON')
  }
  console.debug(`${url} -> ${status} JSON:`, data)
  return data as FastProps
}

export function FastUIController({ rootUrl, pathSendMode, loading }: Props) {
  const [componentProps, setComponentProps] = useState<FastProps | null>(null)
  const { fullPath } = useContext(LocationContext)

  const { error, setError } = useContext(ErrorContext)

  useEffect(() => {
    // setViewData(null)
    let url = rootUrl
    if (pathSendMode === 'query') {
      url += `?path=${encodeURIComponent(fullPath)}`
    } else {
      url += fullPath
    }

    const promise = request({ url })

    promise
      .then((data) => setComponentProps(data))
      .catch((e) => {
        setError({ title: 'Request Error', description: e.message })
      })
    return () => {
      promise.then(() => null).catch(() => null)
    }
  }, [rootUrl, pathSendMode, fullPath, setError])

  if (componentProps === null) {
    if (error) {
      return <></>
    } else {
      return <>{loading ? loading() : <DefaultLoading />}</>
    }
  } else {
    return <AnyComp {...componentProps} />
  }
}
