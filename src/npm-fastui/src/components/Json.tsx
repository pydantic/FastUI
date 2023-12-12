import { FC } from 'react'

import { ClassName } from '../hooks/className'

import { CodeComp } from './Code'

export type JsonData = string | number | boolean | null | JsonData[] | { [key: string]: JsonData }

export interface JsonProps {
  value: JsonData
  type: 'JSON'
  className?: ClassName
}

export const JsonComp: FC<JsonProps> = (props) => {
  let { value, className } = props
  // if the value is a string, we assume it's already JSON, and parse it
  if (typeof value === 'string') {
    try {
      value = JSON.parse(value)
    } catch (e) {
      // if it's not valid JSON, we just display it as a string
    }
  }
  return <CodeComp type="Code" text={JSON.stringify(value, null, 2)} language="json" className={className} />
}
