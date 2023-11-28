import { useContext, useEffect, useState } from 'react'

import { LocationContext } from './hooks/locationContext'
import { ServerLoadFetch } from './components/ServerLoad'
import { loadEvent, LoadEventDetail } from './events'

export function FastUIController() {
  const { fullPath } = useContext(LocationContext)
  const [path, setPath] = useState(fullPath)
  const [reloadValue, setReloadValue] = useState(0)

  useEffect(() => {
    function onEvent(e: Event) {
      const { path, reloadValue } = (e as CustomEvent<LoadEventDetail>).detail

      setPath(path ?? fullPath)
      setReloadValue(reloadValue ?? 0)
    }

    document.addEventListener(loadEvent, onEvent)

    return () => {
      document.removeEventListener(loadEvent, onEvent)
    }
  }, [fullPath])

  return <ServerLoadFetch path={path} devReload={reloadValue} />
}
