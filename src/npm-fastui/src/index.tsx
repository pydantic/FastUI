import { FC, ReactNode } from 'react'

import type { FastProps } from './models'

import { LocationProvider } from './hooks/locationContext'
import { FastUIController } from './controller'
import { ClassNameContext, ClassNameGenerator } from './hooks/className'
import { ErrorContextProvider } from './hooks/error'
import { ConfigContext } from './hooks/config'
import { DevReload } from './dev'
export type * as models from './models'
export * as components from './components'
export * as events from './events'
export type { ClassNameGenerator } from './hooks/className'
export { useClassName, renderClassName } from './hooks/className'
export { pathMatch } from './hooks/locationContext'
export { EventContextProvider } from './hooks/eventContext'

export type CustomRender = (props: FastProps) => FC | void

export interface FastUIProps {
  APIRootUrl: string
  // defaults to 'append'
  APIPathMode?: 'append' | 'query'
  // start of the path to remove from the URL before making a request to the API
  APIPathStrip?: string
  Spinner?: FC
  NotFound?: FC<{ url: string }>
  Transition?: FC<{ children: ReactNode; transitioning: boolean }>
  classNameGenerator?: ClassNameGenerator
  customRender?: CustomRender
  // defaults to `process.env.NODE_ENV === 'development'
  devMode?: boolean
}

export function FastUI(props: FastUIProps) {
  const { classNameGenerator, devMode, ...rest } = props
  return (
    <ClassNameContext.Provider value={classNameGenerator ?? null}>
      <ErrorContextProvider>
        <LocationProvider>
          <ConfigContext.Provider value={rest}>
            <DevReload enabled={devMode} />
            <FastUIController />
          </ConfigContext.Provider>
        </LocationProvider>
      </ErrorContextProvider>
    </ClassNameContext.Provider>
  )
}
