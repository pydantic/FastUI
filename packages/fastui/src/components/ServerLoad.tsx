import { FC, useContext, useEffect, useState } from 'react'

import { ErrorContext } from '../hooks/error'
import { useRequest } from '../tools'
import { DefaultLoading } from '../DefaultLoading'
import { ConfigContext } from '../hooks/config'
import { PageEvent, useEventListenerToggle } from '../events'

import { AnyCompList, FastProps } from './index'

export interface ServerLoadProps {
  type: 'ServerLoad'
  path: string
  components?: FastProps[]
  loadTrigger?: PageEvent
}
export const ServerLoadComp: FC<ServerLoadProps> = ({ path, components, loadTrigger }) => {
  if (components) {
    return <ServerLoadDefer path={path} components={components} loadTrigger={loadTrigger} />
  } else {
    return <ServerLoadDirect path={path} />
  }
}

const ServerLoadDefer: FC<{ path: string; components: FastProps[]; loadTrigger?: PageEvent }> = ({
  components,
  path,
  loadTrigger,
}) => {
  const [loadFromServer] = useEventListenerToggle(loadTrigger)

  if (loadFromServer) {
    return <ServerLoadDirect path={path} />
  } else {
    return <AnyCompList propsList={components} />
  }
}

export const ServerLoadDirect: FC<{ path: string; devReload?: number }> = ({ path, devReload }) => {
  const [componentProps, setComponentProps] = useState<FastProps[] | null>(null)

  const { error } = useContext(ErrorContext)
  const { rootUrl, pathSendMode, Loading } = useContext(ConfigContext)
  const request = useRequest()

  useEffect(() => {
    let fetchUrl = rootUrl
    if (pathSendMode === 'query') {
      fetchUrl += `?path=${encodeURIComponent(path)}`
    } else {
      fetchUrl += path
    }
    const promise = request({ url: fetchUrl })
    promise.then(([, data]) => setComponentProps(data as FastProps[]))

    return () => {
      promise.then(() => null)
    }
  }, [rootUrl, pathSendMode, path, request, devReload])

  if (componentProps === null) {
    if (error) {
      return <></>
    } else if (Loading) {
      return <Loading />
    } else {
      return <DefaultLoading />
    }
  } else {
    return <AnyCompList propsList={componentProps} />
  }
}
