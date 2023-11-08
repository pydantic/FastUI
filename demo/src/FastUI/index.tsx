import { ReactNode } from 'react'
import { LocationProvider } from './hooks/locationContext.tsx'
import { FastUIController } from './controller'
import { ClassNameContext, ClassNameFunction } from './hooks/className'
import { ErrorContextProvider, ErrorDisplayType } from './hooks/error'
import { CustomRender, CustomRenderContext } from './hooks/customRender'
import { FastProps } from './components'

export type {
  ClassNameFunction,
  CustomRender,
  ErrorDisplayType,
  FastProps
}

export interface FastUIProps {
  rootUrl: string
  // defaults to 'append'
  pathSendMode?: 'append' | 'query'
  loading?: () => ReactNode
  DisplayError?: ErrorDisplayType
  defaultClassName?: ClassNameFunction
  customRender?: CustomRender
}

export function FastUI(props: FastUIProps) {
  const { defaultClassName, DisplayError, customRender, ...rest } = props
  return (
    <div className="fastui">
      <LocationProvider>
        <ErrorContextProvider DisplayError={DisplayError}>
          <ClassNameContext.Provider value={defaultClassName ?? null}>
            <CustomRenderContext.Provider value={customRender ?? null}>
              <FastUIController {...rest} />
            </CustomRenderContext.Provider>
          </ClassNameContext.Provider>
        </ErrorContextProvider>
      </LocationProvider>
    </div>
  )
}
