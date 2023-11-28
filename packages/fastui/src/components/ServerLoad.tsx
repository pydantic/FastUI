import { FC, useCallback, useContext, useEffect, useState } from 'react'

import { ErrorContext } from '../hooks/error'
import { useRequest, useSSE } from '../tools'
import { DefaultLoading } from '../DefaultLoading'
import { ConfigContext } from '../hooks/config'
import { PageEvent, usePageEventListen } from '../events'
import { EventContextProvider, useEventContext } from '../hooks/eventContext'

import { AnyCompList, FastProps } from './index'

export interface ServerLoadProps {
  type: 'ServerLoad'
  path: string
  components?: FastProps[]
  loadTrigger?: PageEvent
  sse?: boolean
}
export const ServerLoadComp: FC<ServerLoadProps> = ({ path, components, loadTrigger, sse }) => {
  if (components) {
    return <ServerLoadDefer path={path} components={components} loadTrigger={loadTrigger} sse={sse} />
  } else if (sse) {
    return <ServerLoadSSE path={path} />
  } else {
    return <ServerLoadFetch path={path} />
  }
}

const ServerLoadDefer: FC<{ path: string; components: FastProps[]; loadTrigger?: PageEvent; sse?: boolean }> = ({
  components,
  path,
  loadTrigger,
  sse,
}) => {
  const { eventContext } = usePageEventListen(loadTrigger)

  if (eventContext) {
    return (
      <EventContextProvider context={eventContext}>
        {sse ? <ServerLoadSSE path={path} /> : <ServerLoadFetch path={path} />}
      </EventContextProvider>
    )
  } else {
    return <AnyCompList propsList={components} />
  }
}

export const ServerLoadFetch: FC<{ path: string; devReload?: number }> = ({ path, devReload }) => {
  const [componentProps, setComponentProps] = useState<FastProps[] | null>(null)

  const url = useServerUrl(path)
  const request = useRequest()

  useEffect(() => {
    const promise = request({ url })
    promise.then(([, data]) => setComponentProps(data as FastProps[]))

    return () => {
      promise.then(() => null)
    }
  }, [url, request, devReload])

  return <Render propsList={componentProps} />
}

export const ServerLoadSSE: FC<{ path: string }> = ({ path }) => {
  const [componentProps, setComponentProps] = useState<FastProps[] | null>(null)

  const url = useServerUrl(path)
  const onMessage = useCallback((data: any) => setComponentProps(data as FastProps[]), [])
  useSSE(url, onMessage)

  return <Render propsList={componentProps} />
}

const Render: FC<{ propsList: FastProps[] | null }> = ({ propsList }) => {
  const { error } = useContext(ErrorContext)
  const { Loading } = useContext(ConfigContext)

  if (propsList === null) {
    if (error) {
      return <></>
    } else if (Loading) {
      return <Loading />
    } else {
      return <DefaultLoading />
    }
  } else {
    return <AnyCompList propsList={propsList} />
  }
}

function useServerUrl(path: string): string {
  const { rootUrl, pathSendMode } = useContext(ConfigContext)
  const applyContext = useEventContext()
  const requestPath = applyContext(path)

  if (pathSendMode === 'query') {
    return `${rootUrl}?path=${encodeURIComponent(requestPath)}`
  } else {
    return rootUrl + requestPath
  }
}
