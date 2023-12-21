import { FC, useCallback, useContext, useEffect, useState } from 'react'

import type { ServerLoad, PageEvent, FastProps } from '../models'

import { ErrorContext } from '../hooks/error'
import { useRequest, useSSE } from '../tools'
import { DefaultSpinner, DefaultNotFound, DefaultTransition } from '../Defaults'
import { ConfigContext } from '../hooks/config'
import { usePageEventListen } from '../events'
import { EventContextProvider, useEventContext } from '../hooks/eventContext'
import { LocationContext } from '../hooks/locationContext'

import { AnyCompList } from './index'

export const ServerLoadComp: FC<ServerLoad> = ({ path, components, loadTrigger, sse }) => {
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
  const [transitioning, setTransitioning] = useState<boolean>(false)
  const [componentProps, setComponentProps] = useState<FastProps[] | null>(null)
  const [notFoundUrl, setNotFoundUrl] = useState<string | undefined>(undefined)

  const { fullPath } = useContext(LocationContext)
  const url = useServerUrl(path)
  const request = useRequest()

  useEffect(() => {
    setTransitioning(true)
    const promise = request({ url, expectedStatus: [200, 404] })
    promise.then(([status, data]) => {
      if (status === 200) {
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
      setTransitioning(false)
    })

    return () => {
      promise.then(() => null)
    }
  }, [url, path, request, devReload])

  useEffect(() => {
    setNotFoundUrl(undefined)
  }, [fullPath])

  return <Render propsList={componentProps} notFoundUrl={notFoundUrl} transitioning={transitioning} />
}

export const ServerLoadSSE: FC<{ path: string }> = ({ path }) => {
  const [componentProps, setComponentProps] = useState<FastProps[] | null>(null)

  const url = useServerUrl(path)
  const onMessage = useCallback((data: any) => setComponentProps(data as FastProps[]), [])
  useSSE(url, onMessage)

  return <Render propsList={componentProps} transitioning={false} />
}

const Render: FC<{ propsList: FastProps[] | null; notFoundUrl?: string; transitioning: boolean }> = ({
  propsList,
  notFoundUrl,
  transitioning,
}) => {
  const { error } = useContext(ErrorContext)
  const { Spinner, NotFound, Transition } = useContext(ConfigContext)
  const SpinnerComp = Spinner ?? DefaultSpinner
  const NotFoundComp = NotFound ?? DefaultNotFound
  const TransitionComp = Transition ?? DefaultTransition

  if (notFoundUrl) {
    return <NotFoundComp url={notFoundUrl} />
  } else if (propsList === null) {
    if (error) {
      return <></>
    } else {
      return <SpinnerComp />
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
  const { rootUrl, pathSendMode } = useContext(ConfigContext)
  const applyContext = useEventContext()
  const requestPath = applyContext(path)

  if (pathSendMode === 'query') {
    return `${rootUrl}?path=${encodeURIComponent(requestPath)}`
  } else {
    return rootUrl + requestPath
  }
}

function getFragment(path: string): string | undefined {
  const index = path.indexOf('#')
  if (index !== -1) {
    return path.slice(index + 1)
  }
}
