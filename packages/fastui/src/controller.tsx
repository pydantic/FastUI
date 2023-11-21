import { useContext } from 'react'

import { LocationContext } from './hooks/locationContext'
import { ServerLoadComp } from './components/ServerLoad'

export function FastUIController() {
  const { fullPath } = useContext(LocationContext)

  return <ServerLoadComp type="ServerLoad" url={fullPath} />
}
