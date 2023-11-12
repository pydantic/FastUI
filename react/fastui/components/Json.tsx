import { FC } from 'react'

export type JSON = string | number | boolean | null | JSON[] | { [key: string]: JSON }

export interface JsonProps {
  value: JSON
  type: 'JSON'
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
