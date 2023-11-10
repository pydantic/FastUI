import { ReactNode } from 'react'
import { LocationProvider } from './hooks/locationContext.tsx'
import { FastUIController } from './controller'
import { ClassNameContext, ClassNameGenerator } from './hooks/className'
import { ErrorContextProvider, ErrorDisplayType } from './hooks/error'
import { CustomRender, CustomRenderContext } from './hooks/customRender'
import { FastProps } from './components'

export type { ClassNameGenerator, CustomRender, ErrorDisplayType, FastProps }

export interface FastUIProps {
  rootUrl: string
  // defaults to 'append'
  pathSendMode?: 'append' | 'query'
  loading?: () => ReactNode
  DisplayError?: ErrorDisplayType
  classNameGenerator?: ClassNameGenerator
  customRender?: CustomRender
}

export function FastUI(props: FastUIProps) {
  const { classNameGenerator, DisplayError, customRender, ...rest } = props
  return (
    <div className="fastui">
      <ErrorContextProvider DisplayError={DisplayError}>
        <LocationProvider>
          <ClassNameContext.Provider value={classNameGenerator ?? null}>
            <CustomRenderContext.Provider value={customRender ?? null}>
              <FastUIController {...rest} />
            </CustomRenderContext.Provider>
          </ClassNameContext.Provider>
        </LocationProvider>
      </ErrorContextProvider>
    </div>
  )
}
