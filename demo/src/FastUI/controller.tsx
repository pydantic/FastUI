import {useContext, useEffect, useState} from 'react'
import {AnyComp, AnyCompRender} from './components'
import {DefaultLoading} from './DefaultLoading'
import type {FastProps} from './index'
import {LocationContext} from './locationContext'
import {ErrorContext} from './errorContext'

interface Request {
  url: string
  method?: 'GET' | 'POST' | 'PUT' | 'DELETE'
  body?: Record<string, any>
  headers?: Record<string, string>
}

type Props = Omit<FastProps, "defaultClassName" | "OnError">

const request = async ({url, method, headers, body}: Request): Promise<AnyComp> => {
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
      console.warn(`${url} -> ${status} JSON:`, detail)
      detail = content
    }
    const msg = `${detail ?? response.statusText} (${status})`
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
  return data as AnyComp
}

export function FastUIController({rootUrl, pathSendMode, loading, customRender}: Props) {
  const [viewData, setViewData] = useState<AnyComp | null>(null)
  const {fullPath} = useContext(LocationContext)

  const {setError} = useContext(ErrorContext)

  useEffect(() => {
    // setViewData(null)
    let url = rootUrl
    if (pathSendMode == 'query') {
      url += `?path=${encodeURIComponent(fullPath)}`
    } else {
      url += fullPath
    }

    const promise = request({url})

    promise.then(data => setViewData(data)).catch(e => {
      setError({title: 'Request Error', description: e.message})
    })
    return () => {
      promise.then(() => null).catch(() => null)
    }
  }, [rootUrl, pathSendMode, fullPath, setError])

  if (viewData === null) {
    return (
      <>
        {loading ? loading() : <DefaultLoading/>}
      </>
    )
  } else {
    return AnyCompRender(viewData, customRender)
  }
}
