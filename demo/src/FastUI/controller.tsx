import {useCallback, useContext, useEffect, useState} from 'react'
import {AnyComp, AnyCompRender} from './components'
import {DefaultErrorDisplay} from './DefaultErrorDisplay'
import {DefaultLoading} from './DefaultLoading'
import type {FastProps} from './index'
import {LocationContext} from './locationContext.tsx'

interface Request {
  url: string
  method?: 'GET' | 'POST' | 'PUT' | 'DELETE'
  body?: Record<string, any>
  headers?: Record<string, string>
}

type Props = Omit<FastProps, "defaultClassName">

export function FastUIController({rootUrl, pathSendMode, loading, onError}: Props) {
  const [viewData, setViewData] = useState<AnyComp | null>(null)
  const [shownError, setShownError] = useState<string | null>(null)
  const {fullPath} = useContext(LocationContext)

  const setError = useCallback(
    (description: string) => {
      // toast({ title: 'Request Error', description, className: 'bg-red-600' })
      console.error('FastUI Request Error:', description)
      if (onError) {
        onError(description)
      } else {
        setShownError(description)
      }
    },
    [onError],
  )

  const request = useCallback(
  async ({url, method, headers, body}: Request): Promise<AnyComp> => {
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
    },
    [],
  )

  useEffect(() => {
    setViewData(null)
    let url = rootUrl
    if (pathSendMode == 'query') {
      url += `?path=${encodeURIComponent(fullPath)}`
    } else {
      url += fullPath
    }

    request({url}).then(data => setViewData(data)).catch(e => setError(e.message))
  }, [rootUrl, pathSendMode, request, fullPath, setError])

  if (viewData === null) {
    return (
      <>
        {shownError && <DefaultErrorDisplay error={shownError} />}
        {loading ? loading() : <DefaultLoading/>}
      </>
    )
  } else {
    return (
      <>
        {shownError && <DefaultErrorDisplay error={shownError} />}
        <AnyCompRender {...viewData} />
      </>
    )
  }
}
