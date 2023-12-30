import { FC, ReactNode } from 'react'

import type { ErrorDisplayType } from './hooks/error'
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
  rootUrl: string
  // defaults to 'append'
  pathSendMode?: 'append' | 'query'
  Spinner?: FC
  NotFound?: FC<{ url: string }>
  Transition?: FC<{ children: ReactNode; transitioning: boolean }>
  DisplayError?: ErrorDisplayType
  classNameGenerator?: ClassNameGenerator
  customRender?: CustomRender
  // defaults to `process.env.NODE_ENV === 'development'
  devMode?: boolean
}

export function FastUI(props: FastUIProps) {
  const { classNameGenerator, DisplayError, devMode, ...rest } = props
  return (
    <ErrorContextProvider DisplayError={DisplayError}>
      <LocationProvider>
        <ClassNameContext.Provider value={classNameGenerator ?? null}>
          <ConfigContext.Provider value={rest}>
            <DevReload enabled={devMode} />
            <FastUIController />
          </ConfigContext.Provider>
        </ClassNameContext.Provider>
      </LocationProvider>
    </ErrorContextProvider>
  )
}
