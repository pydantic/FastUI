import { createContext, FC, ReactNode, useEffect, useState } from 'react'

export const ReloadContext = createContext<number>(0)
let devConnected = false

export const DevReloadProvider: FC<{ children: ReactNode; enabled: boolean }> = ({ children, enabled }) => {
  const [value, setValue] = useState<number>(0)

  useEffect(() => {
    let listening = true
    async function listen() {
      let failCount = 0
      while (true) {
        const response = await fetch('/api/__dev__/reload')
        // await like this means we wait for the entire response to be received
        const text = await response.text()
        const value = parseInt(text.replace(/\./g, '')) || 0
        if (response.ok) {
          failCount = 0
        } else {
          failCount++
        }
        // wait long enough for the server to be back online
        await sleep(500)
        if (!listening || failCount >= 4) {
          return value
        }
        console.debug('dev reload...')
        setValue(value)
      }
    }

    if (enabled && !devConnected) {
      devConnected = true
      listen().then((value) => {
        console.debug('dev reload disconnected.')
        setValue(value)
      })
      return () => {
        listening = false
        devConnected = false
      }
    }
  }, [enabled])

  return <ReloadContext.Provider value={value}>{children}</ReloadContext.Provider>
}

async function sleep(ms: number) {
  return new Promise((resolve) => setTimeout(resolve, ms))
}
