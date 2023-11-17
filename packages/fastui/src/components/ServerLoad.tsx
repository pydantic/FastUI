import { FC, useContext, useEffect, useState } from 'react'

import { ErrorContext } from '../hooks/error'
import { ReloadContext } from '../hooks/dev'
import { request } from '../tools'
import { DefaultLoading } from '../DefaultLoading'
import { ConfigContext } from '../hooks/config'

import { AnyComp, FastProps } from './index'

export interface ServerLoadProps {
  type: 'ServerLoad'
  url: string
}

export const ServerLoadComp: FC<ServerLoadProps> = ({ url }) => {
  const [componentProps, setComponentProps] = useState<FastProps | null>(null)

  const { error, setError } = useContext(ErrorContext)
  const reloadValue = useContext(ReloadContext)
  const { rootUrl, pathSendMode, Loading } = useContext(ConfigContext)

  useEffect(() => {
    // setViewData(null)
    let fetchUrl = rootUrl
    if (pathSendMode === 'query') {
      fetchUrl += `?path=${encodeURIComponent(url)}`
    } else {
      fetchUrl += url
    }

    const promise = request({ url: fetchUrl })

    promise
      .then(([, data]) => setComponentProps(data as FastProps))
      .catch((e) => {
        setError({ title: 'Request Error', description: e.message })
      })
    return () => {
      promise.then(() => null)
    }
  }, [rootUrl, pathSendMode, url, setError, reloadValue])

  if (componentProps === null) {
    if (error) {
      return <></>
    } else if (Loading) {
      return <Loading />
    } else {
      return <DefaultLoading />
    }
  } else {
    return <AnyComp {...componentProps} />
  }
}
