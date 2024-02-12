import { FC, ReactNode } from 'react'

export const DefaultNotFound: FC<{ url: string }> = ({ url }) => <div>Page not found: {url}</div>

// default here does nothing
export const DefaultTransition: FC<{ children: ReactNode; transitioning: boolean }> = ({ children }) => (
  <div>{children}</div>
)
