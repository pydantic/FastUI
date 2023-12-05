import { createContext, ReactNode, useEffect, useState, useCallback, useContext } from 'react'

import { fireLoadEvent } from '../events'

import { ErrorContext } from './error'

function parseLocation(): string {
  const { href, origin } = window.location
  // remove origin from the beginning of href
  return href.slice(origin.length)
}

export interface LocationState {
  fullPath: string
  goto: (pushPath: string) => void
  computeQuery: (queryUpdate: Record<string, string | number | null>) => string
  setQuery: (queryUpdate: Record<string, string | number | null>) => void
  // like `goto`, but does not fire `fireLoadEvent`
  gotoCosmetic: (pushPath: string) => void
  back: () => void
}

const initialPath = parseLocation()

const initialState = {
  fullPath: initialPath,
  goto: () => null,
  computeQuery: () => '',
  setQuery: () => null,
  gotoCosmetic: () => null,
  back: () => null,
}

export const LocationContext = createContext<LocationState>(initialState)

export function LocationProvider({ children }: { children: ReactNode }) {
  const [fullPath, setFullPath] = useState(initialPath)
  const { setError } = useContext(ErrorContext)

  const onPopState = useCallback(() => {
    const fullPath = parseLocation()
    setError(null)
    setFullPath(fullPath)
    fireLoadEvent({ path: fullPath })
  }, [setError, setFullPath])

  useEffect(() => {
    window.addEventListener('popstate', onPopState)
    return () => {
      window.removeEventListener('popstate', onPopState)
    }
  }, [onPopState])

  const pushPath = useCallback(
    (newPath: string): string => {
      if (newPath === '.' || newPath === '') {
        newPath = stripQuery(fullPath)
      } else if (!newPath.startsWith('/')) {
        // get rid of `.` and `./` at the beginning of the path
        if (newPath.startsWith('.')) {
          newPath = newPath.slice(1)
          if (newPath.startsWith('/')) {
            newPath = newPath.slice(1)
          }
        }

        const oldPath = stripQuery(fullPath)
        // we're now sure newPath does not start with a `/`
        if (oldPath.endsWith('/') || newPath.startsWith('?')) {
          newPath = oldPath + newPath
        } else {
          newPath = oldPath + '/' + newPath
        }
      }

      window.history.pushState(null, '', newPath)
      setError(null)
      setFullPath(newPath)
      return newPath
    },
    [setError, fullPath],
  )
  const computeQuery = useCallback(
    (queryUpdate: Record<string, string | number | null>): string => {
      const query = getQuery(fullPath)
      for (const [key, value] of Object.entries(queryUpdate)) {
        if (value === null) {
          query.delete(key)
        } else {
          query.set(key, value.toString())
        }
      }
      const queryString = query.toString()
      if (queryString !== '') {
        return '?' + queryString
      } else {
        return ''
      }
    },
    [fullPath],
  )

  const value: LocationState = {
    fullPath,
    goto: useCallback(
      (newPath) => {
        if (newPath.startsWith('http')) {
          window.location.href = newPath
        } else {
          const path = pushPath(newPath)
          fireLoadEvent({ path })
        }
      },
      [pushPath],
    ),
    computeQuery,
    setQuery: useCallback(
      (queryUpdate) => {
        const newPath = stripQuery(fullPath) + computeQuery(queryUpdate)
        const path = pushPath(newPath)
        fireLoadEvent({ path })
      },
      [computeQuery, fullPath, pushPath],
    ),
    gotoCosmetic: useCallback(
      (newPath) => {
        pushPath(newPath)
      },
      [pushPath],
    ),
    back: useCallback(() => {
      window.history.back()
    }, []),
  }

  return <LocationContext.Provider value={value}>{children}</LocationContext.Provider>
}

export function pathMatch(matchPath: string | boolean | undefined, fullPath: string): boolean {
  const path = stripQuery(fullPath)
  if (typeof matchPath === 'string') {
    if (matchPath.startsWith('regex:')) {
      const regex = new RegExp(matchPath.slice(6))
      return regex.test(path)
    } else if (matchPath.startsWith('startswith:')) {
      return path.startsWith(matchPath.slice(11))
    } else {
      return path === matchPath
    }
  } else if (matchPath === undefined) {
    return false
  } else {
    return matchPath
  }
}

function stripQuery(fullPath: string): string {
  const q = fullPath.indexOf('?')
  if (q === -1) {
    return fullPath
  } else {
    return fullPath.slice(0, q)
  }
}

function getQuery(fullPath: string): URLSearchParams {
  const q = fullPath.indexOf('?')
  if (q === -1) {
    return new URLSearchParams()
  } else {
    return new URLSearchParams(fullPath.slice(q + 1))
  }
}
