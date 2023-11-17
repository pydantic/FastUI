import { ReactNode } from 'react'

import { LocationProvider } from './hooks/locationContext'
import { FastUIController } from './controller'
import { ClassNameContext, ClassNameGenerator } from './hooks/className'
import { ErrorContextProvider, ErrorDisplayType } from './hooks/error'
import { CustomRender, CustomRenderContext } from './hooks/customRender'
import { FastProps } from './components'
import { DisplayChoices } from './display'
import { DevReloadProvider } from './hooks/dev'

export type { ClassNameGenerator, CustomRender, ErrorDisplayType, FastProps, DisplayChoices }

export interface FastUIProps {
  rootUrl: string
  // defaults to 'append'
  pathSendMode?: 'append' | 'query'
  loading?: () => ReactNode
  DisplayError?: ErrorDisplayType
  classNameGenerator?: ClassNameGenerator
  customRender?: CustomRender
  dev?: boolean
}

export function FastUI(props: FastUIProps) {
  const { classNameGenerator, DisplayError, customRender, dev, ...rest } = props
  return (
    <div className="fastui">
      <DevReloadProvider enabled={dev ?? false}>
        <ErrorContextProvider DisplayError={DisplayError}>
          <LocationProvider>
            <ClassNameContext.Provider value={classNameGenerator ?? null}>
              <CustomRenderContext.Provider value={customRender ?? null}>
                <FastUIController {...rest} />
              </CustomRenderContext.Provider>
            </ClassNameContext.Provider>
          </LocationProvider>
        </ErrorContextProvider>
      </DevReloadProvider>
    </div>
  )
}
