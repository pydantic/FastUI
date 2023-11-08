import { createContext, ReactNode, useEffect, useState, useCallback } from 'react'

interface PureLocation {
  path: string
  query: URLSearchParams
  hash: string
}

function parseLocation(): PureLocation {
  const { pathname, search, hash } = window.location
  return {
    path: pathname,
    query: new URLSearchParams(search),
    hash,
  }
}

function genFullPath({ path, query, hash }: PureLocation): string {
  let fullPath = path
  if (query.size > 0) {
    fullPath += `?${query.toString()}`
  }
  if (hash) {
    fullPath += `#${hash}`
  }
  return fullPath
}

export interface LocationState extends PureLocation {
  fullPath: string
  goto: (pushPath: string, clear?: boolean) => void
  setQuery: (query: Record<string, string> | URLSearchParams) => void
  setQueryArg: (name: string, value: string | false) => void
}

const initialLocation = parseLocation()

const initialState = {
  ...initialLocation,
  fullPath: genFullPath(initialLocation),
  goto: () => null,
  setQuery: () => null,
  setQueryArg: () => null,
}

export const LocationContext = createContext<LocationState>(initialState)

export function LocationProvider({ children }: { children: ReactNode }) {
  const [pureLocation, setPureLocation] = useState(initialLocation)
  const [fullPath, setFullPath] = useState(initialState.fullPath)

  const onPopState = () => {
    setPureLocation(parseLocation())
  }

  useEffect(() => {
    window.addEventListener('popstate', onPopState)
    return () => {
      window.removeEventListener('popstate', onPopState)
    }
  }, [])

  const pushState = useCallback((path: string, query: URLSearchParams, hash: string) => {
    const fullPath = genFullPath({ path, query, hash })
    window.history.pushState(null, '', fullPath)
    setPureLocation({ path, query, hash })
    setFullPath(fullPath)
  }, [])

  const value: LocationState = {
    ...pureLocation,
    fullPath,
    goto: useCallback(
      (pushPath: string, clear?: boolean) => {
        let newPath = pushPath
        // TODO do better with url starting with `.`
        if (!newPath.startsWith('/')) {
          if (pureLocation.path.endsWith('/')) {
            newPath = pureLocation.path + newPath
          } else {
            newPath = pureLocation.path + '/' + newPath
          }
        }

        if (clear) {
          window.history.pushState(null, '', newPath)
          setPureLocation({
            path: newPath,
            query: new URLSearchParams(),
            hash: '',
          })
          setFullPath(newPath)
        } else {
          pushState(newPath, pureLocation.query, pureLocation.hash)
        }
      },
      [pushState, pureLocation],
    ),
    setQuery: useCallback(
      (query: Record<string, string> | URLSearchParams) => {
        const newQuery = new URLSearchParams(query)
        pushState(pureLocation.path, newQuery, pureLocation.hash)
      },
      [pushState, pureLocation],
    ),
    setQueryArg: useCallback(
      (name: string, value: string | false) => {
        if (value === false) {
          pureLocation.query.delete(name)
        } else {
          pureLocation.query.set(name, value)
        }
        pushState(pureLocation.path, pureLocation.query, pureLocation.hash)
      },
      [pushState, pureLocation],
    ),
  }

  return <LocationContext.Provider value={value}>{children}</LocationContext.Provider>
}
