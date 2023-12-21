import { FC, useContext, useEffect } from 'react'

import { sleep } from './tools'
import { ErrorContext } from './hooks/error'
import { fireLoadEvent } from './events'
import { ConfigContext } from './hooks/config'

let devConnected = false

export const DevReload: FC<{ enabled?: boolean }> = ({ enabled }) => {
  if (typeof enabled === 'undefined') {
    enabled = process.env.NODE_ENV === 'development'
  }

  if (enabled) {
    return <DevReloadActive />
  } else {
    return <></>
  }
}

const DevReloadActive = () => {
  const { setError } = useContext(ErrorContext)
  const { rootUrl } = useContext(ConfigContext)

  useEffect(() => {
    let listening = true
    let lastValue = 0

    async function listen() {
      let count = 0
      let failCount = 0
      // this avoids connecting twice when vite is reloading
      await sleep(100)
      while (true) {
        if (!listening || failCount >= 5) {
          return count
        }
        const response = await fetch(rootUrl + '/__dev__/reload')
        count++
        console.debug(`dev reload connected ${count}...`)
        // if the response is okay, and we previously failed, clear error
        if (response.ok && failCount > 0) {
          setError(null)
        } else if (response.status === 404) {
          console.log('dev reload endpoint not found, disabling dev reload')
          return count
        }
        // await like this means we wait for the entire response to be received
        const text = await response.text()
        if (response.ok && text.startsWith('fastui-dev-reload')) {
          failCount = 0
          const valueMatch = text.match(/(\d+)$/)
          const value = valueMatch ? parseInt(valueMatch[1]!) : 0
          if (value !== lastValue) {
            lastValue = value
            // wait long enough for the server to be back online
            await sleep(300)
            console.debug('dev reloading')
            fireLoadEvent({ reloadValue: value })
            setError(null)
          }
        } else if (response.ok) {
          console.log("dev reload endpoint didn't return magic value, disabling dev reload")
          return count
        } else {
          failCount++
          await sleep(2000)
        }
      }
    }

    if (!devConnected) {
      devConnected = true
      listen().then((count) => count > 0 && console.debug('dev reload disconnected.'))
      return () => {
        listening = false
        devConnected = false
      }
    }
  }, [setError, rootUrl])
  return <></>
}
