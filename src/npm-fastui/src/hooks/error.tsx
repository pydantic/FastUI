import { createContext, FC, ReactNode, useCallback, useContext, useState } from 'react'

interface ErrorDetails {
  title: string
  description: string
}

interface ErrorDisplayProps extends ErrorDetails {
  children?: ReactNode
}

export type ErrorDisplayType = FC<ErrorDisplayProps>

interface ErrorContextType {
  error: ErrorDetails | null
  setError: (error: ErrorDetails | null) => void
  DisplayError: ErrorDisplayType
}

const DefaultErrorDisplay: ErrorDisplayType = ({ title, description, children }) => (
  <>
    <div className="alert alert-danger m-3" role="alert">
      <h4>{title}</h4>
      {description}
    </div>
    {children}
  </>
)

export const ErrorContext = createContext<ErrorContextType>({
  error: null,
  setError: () => null,
  DisplayError: DefaultErrorDisplay,
})

const MaybeError: FC<{ children: ReactNode }> = ({ children }) => {
  const { error, DisplayError } = useContext(ErrorContext)
  if (error) {
    return <DisplayError {...error}>{children}</DisplayError>
  } else {
    return <>{children}</>
  }
}

interface Props {
  DisplayError?: ErrorDisplayType
  children: ReactNode
}

export const ErrorContextProvider: FC<Props> = ({ DisplayError, children }) => {
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
  const contextValue: ErrorContextType = { error, setError, DisplayError: DisplayError ?? DefaultErrorDisplay }

  return (
    <ErrorContext.Provider value={contextValue}>
      <MaybeError>{children}</MaybeError>
    </ErrorContext.Provider>
  )
}
