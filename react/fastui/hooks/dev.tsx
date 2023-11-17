import { createContext, FC, ReactNode, useContext, useEffect, useState } from 'react'

import { ErrorContext } from './error'

export const ReloadContext = createContext<number>(0)
let devConnected = false

export const DevReloadProvider: FC<{ children: ReactNode; enabled?: boolean }> = ({ children, enabled }) => {
  const [value, setValue] = useState<number>(0)
  const { setError } = useContext(ErrorContext)
  if (typeof enabled === 'undefined') {
    enabled = process.env.NODE_ENV === 'development'
  }

  useEffect(() => {
    let listening = true
    async function listen() {
      let count = 0
      let failCount = 0
      // this avoids connecting twice when vite is reloading
      await sleep(100)
      while (true) {
        if (!listening || failCount >= 5) {
          return count
        }
        const response = await fetch('/api/__dev__/reload')
        count++
        console.debug(`dev reload connected ${count}...`)
        // if the response is okay, and we previously failed, clear error
        if (response.ok && failCount > 0) {
          setError(null)
        }
        // await like this means we wait for the entire response to be received
        const text = await response.text()
        const value = parseInt(text.replace(/\./g, '')) || 0
        if (response.status === 404) {
          console.log('dev reload endpoint not found, disabling dev reload')
          return count
        } else if (response.ok) {
          failCount = 0
          // wait long enough for the server to be back online
          await sleep(300)
          console.debug('dev reloading')
          setValue(value)
          setError(null)
        } else {
          failCount++
          await sleep(2000)
        }
      }
    }

    if (enabled && !devConnected) {
      devConnected = true
      listen().then((count) => count > 0 && console.debug('dev reload disconnected.'))
      return () => {
        listening = false
        devConnected = false
      }
    }
  }, [enabled, setError])

  return <ReloadContext.Provider value={value}>{children}</ReloadContext.Provider>
}

async function sleep(ms: number) {
  return new Promise((resolve) => setTimeout(resolve, ms))
}
