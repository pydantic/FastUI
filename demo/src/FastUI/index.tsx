import {ReactNode} from 'react'
import {LocationProvider} from './locationContext'
import {FastUIController} from './controller'
import {ClassNameContext, ClassNameFunction} from './ClassName'

export interface FastProps {
  rootUrl: string
  // defaults to 'append'
  pathSendMode?: 'append' | 'query'
  loading?: () => ReactNode
  onError?: (description: string) => void
  defaultClassName?: ClassNameFunction
}

export function FastUI(props: FastProps) {
  const {defaultClassName, ...rest} = props
  return (
    <div className="fastui">
      <LocationProvider>
          <ClassNameContext.Provider value={defaultClassName ?? null}>
            <FastUIController {...rest} />
          </ClassNameContext.Provider>
      </LocationProvider>
    </div>
  )
}
