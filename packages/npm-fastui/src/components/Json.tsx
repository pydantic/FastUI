import { FC } from 'react'

import { ClassName } from '../hooks/className'

export type JsonData = string | number | boolean | null | JsonData[] | { [key: string]: JsonData }

export interface JsonProps {
  value: JsonData
  type: 'JSON'
  className?: ClassName
}

export const JsonComp: FC<JsonProps> = ({ value }) => {
  // if the value is a string, we assume it's already JSON, and parse it
  if (typeof value === 'string') {
    value = JSON.parse(value)
  }
  return (
    <div className="code-block">
      <pre>
        <code>{JSON.stringify(value, null, 2)}</code>
      </pre>
    </div>
  )
}
