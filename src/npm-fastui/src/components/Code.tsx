import { lazy } from 'react'

import { ClassName } from '../hooks/className'

export interface CodeProps {
  type: 'Code'
  text: string
  language?: string
  className?: ClassName
  codeStyle?: string
}

export const CodeComp = lazy(() => import('./CodeLazy'))
