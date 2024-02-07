import { createContext, FC, ReactNode, useCallback, useContext, useState } from 'react'

import type { Error as ErrorProps } from '../models'

import { ErrorComp } from '../components'

import { useCustomRender } from './config'

interface ErrorDetails {
  title: string
  description: string
  statusCode?: number
}

interface ErrorDisplayProps extends ErrorDetails {
  children?: ReactNode
}

interface ErrorContextType {
  error: ErrorDetails | null
  setError: (error: ErrorDetails | null) => void
}

export const DisplayError: FC<ErrorDisplayProps> = ({ title, description, statusCode, children }) => {
  const props: ErrorProps = {
    title,
    description,
    statusCode,
    children,
    type: 'Error',
  }
  const CustomRenderComp = useCustomRender(props)
  if (CustomRenderComp) {
    return <CustomRenderComp />
  } else {
    return <ErrorComp {...props} />
  }
}

export const ErrorContext = createContext<ErrorContextType>({
  error: null,
  setError: () => null,
})

const MaybeError: FC<{ children: ReactNode }> = ({ children }) => {
  const { error } = useContext(ErrorContext)
  if (error) {
    return <DisplayError {...error}>{children}</DisplayError>
  } else {
    return <>{children}</>
  }
}

interface Props {
  children: ReactNode
}

export const ErrorContextProvider: FC<Props> = ({ children }) => {
  const [error, setErrorState] = useState<ErrorDetails | null>(null)

  const setError = useCallback(
    (error: ErrorDetails | null) => {
      if (error) {
        console.warn('setting error:', error)
      }
      setErrorState(error)
    },
    [setErrorState],
  )

  return (
    <ErrorContext.Provider value={{ error, setError }}>
      <MaybeError>{children}</MaybeError>
    </ErrorContext.Provider>
  )
}
