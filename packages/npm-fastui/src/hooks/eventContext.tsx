import { createContext, FC, ReactNode, useCallback, useContext } from 'react'

export type ContextType = Record<string, string | number>

const EventContext = createContext<ContextType | null>(null)

export const useEventContext = (): ((template: string) => string) => {
  const context = useContext(EventContext)

  return useCallback((template: string): string => applyContext(template, context), [context])
}

export const EventContextProvider: FC<{ children: ReactNode; context: ContextType | null }> = ({
  children,
  context,
}) => {
  return <EventContext.Provider value={context}>{children}</EventContext.Provider>
}

const applyContext = (template: string, context: ContextType | null): string => {
  if (!context) {
    return template
  }

  return template.replace(/{(.+?)}/g, (_, key: string): string => {
    const v = context[key]
    if (v === undefined) {
      throw new Error(`field "${key}" not found in ${JSON.stringify(context)}`)
    } else {
      return v.toString()
    }
  })
}
