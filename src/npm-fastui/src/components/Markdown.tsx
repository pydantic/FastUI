import { lazy } from 'react'

import type { ClassName } from '../hooks/className'

export interface MarkdownProps {
  type: 'Markdown'
  text: string
  codeStyle?: string
  className?: ClassName
}

export const MarkdownComp = lazy(() => import('./MarkdownLazy'))
