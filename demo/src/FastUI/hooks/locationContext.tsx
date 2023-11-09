import { createContext, ReactNode, useEffect, useState, useCallback } from 'react'


function parseLocation(): string {
  const { href, origin } = window.location
  // remove origin from the beginning of href
  return href.slice(origin.length)
}

export interface LocationState {
  fullPath: string
  goto: (pushPath: string) => void
}

const initialPath = parseLocation()

const initialState = {
  fullPath: initialPath,
  goto: () => null,
}

export const LocationContext = createContext<LocationState>(initialState)

export function LocationProvider({ children }: { children: ReactNode }) {
  const [fullPath, setFullPath] = useState(initialPath)

  const onPopState = () => {
    const fullPath = parseLocation()
    setFullPath(fullPath)
  }

  useEffect(() => {
    window.addEventListener('popstate', onPopState)
    return () => {
      window.removeEventListener('popstate', onPopState)
    }
  }, [])

  const value: LocationState = {
    fullPath,
    goto: useCallback(
      (pushPath: string) => {
        let newPath = pushPath
        if (!newPath.startsWith('/')) {
          // get rid of `.` and `./` at the beginning of the path
          if (newPath.startsWith('.')) {
            newPath = newPath.slice(1)
            if (newPath.startsWith('/')) {
              newPath = newPath.slice(1)
            }
          }

          const oldPath = (new URL(window.location.href)).pathname
          // we're now sure newPath does not start with a `/`
          if (oldPath.endsWith('/')) {
            newPath = oldPath + newPath
          } else {
            newPath = oldPath + '/' + newPath
          }
        }

        window.history.pushState(null, '', newPath)
        setFullPath(newPath)
      },
      [],
    ),
  }

  return <LocationContext.Provider value={value}>{children}</LocationContext.Provider>
}
