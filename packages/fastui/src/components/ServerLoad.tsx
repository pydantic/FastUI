import { FC, useCallback, useContext, useEffect, useState } from 'react'

import { ErrorContext } from '../hooks/error'
import { useRequest, useSSE } from '../tools'
import { DefaultSpinner, DefaultNotFound } from '../Defaults'
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
  const [notFoundUrl, setNotFoundUrl] = useState<string | undefined>(undefined)

  const url = useServerUrl(path)
  const request = useRequest()

  useEffect(() => {
    const promise = request({ url, expectedStatus: [200, 404] })
    promise.then(([status, data]) => {
      if (status === 200) {
        setComponentProps(data as FastProps[])
      } else {
        setNotFoundUrl(url)
      }
    })

    return () => {
      promise.then(() => null)
    }
  }, [url, request, devReload])

  return <Render propsList={componentProps} notFoundUrl={notFoundUrl} />
}

export const ServerLoadSSE: FC<{ path: string }> = ({ path }) => {
  const [componentProps, setComponentProps] = useState<FastProps[] | null>(null)

  const url = useServerUrl(path)
  const onMessage = useCallback((data: any) => setComponentProps(data as FastProps[]), [])
  useSSE(url, onMessage)

  return <Render propsList={componentProps} />
}

const Render: FC<{ propsList: FastProps[] | null; notFoundUrl?: string }> = ({ propsList, notFoundUrl }) => {
  const { error } = useContext(ErrorContext)
  const { Spinner, NotFound } = useContext(ConfigContext)
  const SpinnerComp = Spinner ?? DefaultSpinner
  const NotFoundComp = NotFound ?? DefaultNotFound

  if (notFoundUrl) {
    return <NotFoundComp url={notFoundUrl} />
  } else if (propsList === null) {
    if (error) {
      return <></>
    } else {
      return <SpinnerComp />
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
