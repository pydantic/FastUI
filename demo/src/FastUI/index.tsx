import {ReactNode} from 'react'
import {LocationProvider} from './locationContext'
import {FastUIController} from './controller'
import {ClassNameContext, ClassNameFunction} from './ClassName'
import {ErrorContextProvider, OnErrorType} from './errorContext'
import {CustomRender} from './components'

export type {ClassNameFunction, CustomRender, OnErrorType}

export interface FastProps {
  rootUrl: string
  // defaults to 'append'
  pathSendMode?: 'append' | 'query'
  loading?: () => ReactNode
  OnError?: OnErrorType
  defaultClassName?: ClassNameFunction
  customRender?: CustomRender
}

export function FastUI(props: FastProps) {
  const {defaultClassName, OnError, ...rest} = props
  return (
    <div className="fastui">
      <LocationProvider>
        <ErrorContextProvider OnError={OnError}>
          <ClassNameContext.Provider value={defaultClassName ?? null}>
            <FastUIController {...rest} />
          </ClassNameContext.Provider>
        </ErrorContextProvider>
      </LocationProvider>
    </div>
  )
}
