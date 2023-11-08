import { createContext, FC, ReactNode, useCallback, useContext, useState } from 'react'

const DefaultErrorDisplay: FC<{ error: ErrorDetails; children: ReactNode }> = ({ error, children }) => (
  <>
    <div className="alert alert-danger m-3" role="alert">
      <h2>{error.title}</h2>
      {error.description}
    </div>
    {children}
  </>
)

interface ErrorDetails {
  title: string
  description: string
}

export type OnErrorType = FC<{ error: ErrorDetails; children: ReactNode }>

interface ErrorContextType {
  error: ErrorDetails | null
  setError: (error: ErrorDetails | null) => void
}

export const ErrorContext = createContext<ErrorContextType>({
  error: null,
  setError: () => null,
})

const DisplayError: FC<{ OnError?: OnErrorType; children: ReactNode }> = ({ OnError, children }) => {
  const { error } = useContext(ErrorContext)
  if (error) {
    const ErrorDisplay = OnError ?? DefaultErrorDisplay
    return <ErrorDisplay error={error}>{children}</ErrorDisplay>
  } else {
    return <>{children}</>
  }
}

export const ErrorContextProvider: FC<{ OnError?: OnErrorType; children: ReactNode }> = ({ OnError, children }) => {
  const [error, setErrorState] = useState<ErrorDetails | null>(null)

  const setError = useCallback(
    (error: ErrorDetails | null) => {
      console.warn('setting error:', error)
      setErrorState(error)
    },
    [setErrorState],
  )

  return (
    <ErrorContext.Provider value={{ error, setError }}>
      <DisplayError OnError={OnError}>{children}</DisplayError>
    </ErrorContext.Provider>
  )
}
