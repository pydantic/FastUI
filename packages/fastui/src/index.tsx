import { FC } from 'react'

import { LocationProvider } from './hooks/locationContext'
import { FastUIController } from './controller'
import { ClassNameContext, ClassNameGenerator } from './hooks/className'
import { ErrorContextProvider, ErrorDisplayType } from './hooks/error'
import { ConfigContext } from './hooks/config'
import { FastProps } from './components'
import { DisplayChoices } from './display'
import { DevReloadProvider } from './hooks/dev'

export type { ClassNameGenerator, ErrorDisplayType, FastProps, DisplayChoices }

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
