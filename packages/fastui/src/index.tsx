import { FC } from 'react'

import type { ErrorDisplayType } from './hooks/error'

import { LocationProvider } from './hooks/locationContext'
import { FastUIController } from './controller'
import { ClassNameContext, ClassNameGenerator } from './hooks/className'
import { ErrorContextProvider } from './hooks/error'
import { ConfigContext } from './hooks/config'
import { FastProps } from './components'
import { DevReloadProvider } from './hooks/dev'

export * as components from './components'
export * as events from './hooks/events'
export type { DisplayChoices } from './display'
export type { ClassName, ClassNameGenerator } from './hooks/className'
export { useClassName, renderClassName } from './hooks/className'
export { pathMatch } from './hooks/locationContext'

export type CustomRender = (props: FastProps) => FC | void

export interface FastUIProps {
  rootUrl: string
  // defaults to 'append'
  pathSendMode?: 'append' | 'query'
  Loading?: FC
  DisplayError?: ErrorDisplayType
  classNameGenerator?: ClassNameGenerator
  customRender?: CustomRender
  // defaults to `process.env.NODE_ENV === 'development'
  devMode?: boolean
}

export function FastUI(props: FastUIProps) {
  const { classNameGenerator, DisplayError, devMode, ...rest } = props
  return (
    <div className="fastui">
      <ErrorContextProvider DisplayError={DisplayError}>
        <DevReloadProvider enabled={devMode}>
          <LocationProvider>
            <ClassNameContext.Provider value={classNameGenerator ?? null}>
              <ConfigContext.Provider value={rest}>
                <FastUIController />
              </ConfigContext.Provider>
            </ClassNameContext.Provider>
          </LocationProvider>
        </DevReloadProvider>
      </ErrorContextProvider>
    </div>
  )
}
