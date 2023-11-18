import { useContext, useEffect, useState } from 'react'

import type { FastUIProps } from './index'

import { FastProps, AnyComp } from './components'
import { DefaultLoading } from './DefaultLoading'
import { LocationContext } from './hooks/locationContext'
import { ErrorContext } from './hooks/error'
import { request } from './tools'
import { ReloadContext } from './hooks/dev'

type Props = Omit<FastUIProps, 'defaultClassName' | 'OnError' | 'customRender'>

export function FastUIController({ rootUrl, pathSendMode, loading }: Props) {
  const [componentProps, setComponentProps] = useState<FastProps | null>(null)
  const { fullPath } = useContext(LocationContext)

  const { error, setError } = useContext(ErrorContext)
  const reloadValue = useContext(ReloadContext)

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
      .then(([, data]) => setComponentProps(data as FastProps))
      .catch((e) => {
        setError({ title: 'Request Error', description: e.message })
      })
    return () => {
      promise.then(() => null).catch(() => null)
    }
  }, [rootUrl, pathSendMode, fullPath, setError, reloadValue])

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
