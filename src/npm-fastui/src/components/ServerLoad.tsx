import { FC, useCallback, useContext, useEffect, useState } from 'react'

import type { ServerLoad, PageEvent, FastProps } from '../models'

import { ErrorContext } from '../hooks/error'
import { useRequest, useSSE, Method } from '../tools'
import { DefaultNotFound, DefaultTransition } from '../Defaults'
import { ConfigContext } from '../hooks/config'
import { usePageEventListen } from '../events'
import { EventContextProvider, useEventContext } from '../hooks/eventContext'
import { LocationContext } from '../hooks/locationContext'

import { AnyCompList } from './index'

import { SpinnerComp } from './spinner'

export const ServerLoadComp: FC<ServerLoad> = (props) => {
  const { path, components, loadTrigger, sse, method, sseRetry } = props
  if (components) {
    return (
      <ServerLoadDefer
        path={path}
        components={components}
        loadTrigger={loadTrigger}
        sse={sse}
        method={method}
        sseRetry={sseRetry}
      />
    )
  } else if (sse) {
    return <ServerLoadSSE path={path} method={method} sseRetry={sseRetry} />
  } else {
    return <ServerLoadFetch path={path} />
  }
}

interface DeferProps {
  path: string
  components: FastProps[]
  loadTrigger?: PageEvent
  sse?: boolean
  method?: Method
  sseRetry?: number
}

const ServerLoadDefer: FC<DeferProps> = ({ components, path, loadTrigger, sse, method, sseRetry }) => {
  const { eventContext } = usePageEventListen(loadTrigger)

  if (eventContext) {
    return (
      <EventContextProvider context={eventContext}>
        {sse ? (
          <ServerLoadSSE path={path} method={method} sseRetry={sseRetry} />
        ) : (
          <ServerLoadFetch path={path} method={method} />
        )}
      </EventContextProvider>
    )
  } else {
    return <AnyCompList propsList={components} />
  }
}

interface FetchProps {
  path: string
  devReload?: number
  method?: Method
}

export const ServerLoadFetch: FC<FetchProps> = ({ path, devReload, method }) => {
  const [transitioning, setTransitioning] = useState<boolean>(false)
  const [componentProps, setComponentProps] = useState<FastProps[] | null>(null)
  const [notFoundUrl, setNotFoundUrl] = useState<string | undefined>(undefined)

  const { fullPath } = useContext(LocationContext)
  const url = useServerUrl(path)
  const request = useRequest()

  useEffect(() => {
    setTransitioning(true)
    let componentLoaded = true
    request({ url, method, expectedStatus: [200, 345, 404] }).then(([status, data]) => {
      if (componentLoaded) {
        // 345 is treat the same as 200 - the server is expected to return valid FastUI components
        if (status === 200 || status === 345) {
          setComponentProps(data as FastProps[])
          // if there's a fragment, scroll to that ID once the page is loaded
          const fragment = getFragment(path)
          if (fragment) {
            setTimeout(() => {
              const element = document.getElementById(fragment)
              if (element) {
                element.scrollIntoView()
              }
            }, 50)
          }
        } else {
          setNotFoundUrl(url)
        }
      }
      setTransitioning(false)
    })

    return () => {
      componentLoaded = false
    }
  }, [url, path, request, devReload, method])

  useEffect(() => {
    setNotFoundUrl(undefined)
  }, [fullPath])

  return <Render propsList={componentProps} notFoundUrl={notFoundUrl} transitioning={transitioning} />
}

interface SSEProps {
  path: string
  method?: Method
  sseRetry?: number
}

export const ServerLoadSSE: FC<SSEProps> = ({ path, method, sseRetry }) => {
  const [componentProps, setComponentProps] = useState<FastProps[] | null>(null)

  const url = useServerUrl(path)
  const onMessage = useCallback((data: any) => setComponentProps(data as FastProps[]), [])
  useSSE(url, onMessage, method, sseRetry)

  return <Render propsList={componentProps} transitioning={false} />
}

const Render: FC<{ propsList: FastProps[] | null; notFoundUrl?: string; transitioning: boolean }> = ({
  propsList,
  notFoundUrl,
  transitioning,
}) => {
  const { error } = useContext(ErrorContext)
  const { NotFound, Transition } = useContext(ConfigContext)
  const NotFoundComp = NotFound ?? DefaultNotFound
  const TransitionComp = Transition ?? DefaultTransition

  if (notFoundUrl) {
    return <NotFoundComp url={notFoundUrl} />
  } else if (propsList === null) {
    if (error) {
      return <></>
    } else {
      return <SpinnerComp type="Spinner" />
    }
  } else {
    return (
      <TransitionComp transitioning={transitioning}>
        <AnyCompList propsList={propsList} />
      </TransitionComp>
    )
  }
}

function useServerUrl(path: string): string {
  const { APIRootUrl, APIPathMode, APIPathStrip } = useContext(ConfigContext)
  if (APIPathStrip && path.startsWith(APIPathStrip)) {
    path = path.slice(APIPathStrip.length)
  }
  const applyContext = useEventContext()
  const requestPath = applyContext(path)

  if (APIPathMode === 'query') {
    return `${APIRootUrl}?path=${encodeURIComponent(requestPath)}`
  } else {
    return APIRootUrl + requestPath
  }
}

function getFragment(path: string): string | undefined {
  const index = path.indexOf('#')
  if (index !== -1) {
    return path.slice(index + 1)
  }
}
