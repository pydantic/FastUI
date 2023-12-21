import { FC } from 'react'

import type { AnyEvent, DisplayMode, Display, JsonData } from '../models'

import { useCustomRender } from '../hooks/config'
import { unreachable, asTitle } from '../tools'

import { JsonComp } from './Json'
import { LinkRender } from './link'

export const DisplayComp: FC<Display> = (props) => {
  const CustomRenderComp = useCustomRender(props)
  if (CustomRenderComp) {
    return <CustomRenderComp />
  }

  const { onClick } = props
  if (onClick) {
    return (
      <LinkRender onClick={onClick}>
        <DisplayRender {...props} />
      </LinkRender>
    )
  } else {
    return <DisplayRender {...props} />
  }
}

const DisplayRender: FC<Display> = (props) => {
  const mode = props.mode ?? 'auto'
  const value = props.value ?? null
  if (mode === 'json') {
    return <JsonComp type="JSON" value={value} />
  } else if (Array.isArray(value)) {
    return <DisplayArray mode={mode} value={value} />
  } else if (typeof value === 'object' && value !== null) {
    return <DisplayObject mode={mode} value={value} />
  } else {
    return <DisplayPrimitive mode={mode} value={value} />
  }
}

interface DisplayArrayProps {
  value: JsonData[]
  mode?: DisplayMode
}

export const DisplayArray: FC<DisplayArrayProps> = (props) => {
  const { mode, value } = props

  return (
    <>
      {value.map((v, i) => (
        <span key={i}>
          <DisplayComp type="Display" mode={mode} value={v} />,{' '}
        </span>
      ))}
    </>
  )
}

interface DisplayObjectProps {
  value: { [key: string]: JsonData }
  mode?: DisplayMode
}

export const DisplayObject: FC<DisplayObjectProps> = (props) => {
  const { mode, value } = props

  return (
    <>
      {Object.entries(value).map(([key, v], i) => (
        <span key={key}>
          {key}: <DisplayComp type="Display" mode={mode} key={i} value={v} />,{' '}
        </span>
      ))}
    </>
  )
}

type JSONPrimitive = string | number | boolean | null

export interface DisplayPrimitiveProps {
  value: JSONPrimitive
  mode: DisplayMode
}

export const DisplayPrimitive: FC<DisplayPrimitiveProps> = (props) => {
  const { mode, value } = props

  switch (mode) {
    case 'auto':
      return <DisplayAuto value={value} />
    case 'plain':
      return <DisplayPlain value={value} />
    case 'datetime':
      return <DisplayDateTime value={value} />
    case 'date':
      return <DisplayDate value={value} />
    case 'duration':
      return <DisplayDuration value={value} />
    case 'as_title':
      return <DisplayAsTitle value={value} />
    case 'markdown':
      return <DisplayMarkdown value={value} />
    case 'json':
    case 'inline_code':
      return <DisplayInlineCode value={value} />
    default:
      unreachable('Unexpected display type', mode, props)
  }
}

const DisplayNull: FC = () => {
  return <span className="fu-null">&mdash;</span>
}

const DisplayAuto: FC<{ value: JSONPrimitive }> = ({ value }) => {
  if (value === null) {
    return <DisplayNull />
  } else if (typeof value === 'boolean') {
    if (value) {
      return <>✓</>
    } else {
      return <>&times;</>
    }
  } else if (typeof value === 'number') {
    return <>{value.toLocaleString()}</>
  } else {
    return <>{value}</>
  }
}

const DisplayPlain: FC<{ value: JSONPrimitive }> = ({ value }) => {
  if (value === null) {
    return <DisplayNull />
  } else {
    return <>{value.toString()}</>
  }
}

const DisplayDateTime: FC<{ value: JSONPrimitive }> = ({ value }) => {
  if (value === null) {
    return <DisplayNull />
  } else {
    // TODO
    return <>{value.toString()}</>
  }
}

const DisplayDate: FC<{ value: JSONPrimitive }> = ({ value }) => {
  if (value === null) {
    return <DisplayNull />
  } else {
    // TODO
    return <>{value.toString()}</>
  }
}

const DisplayDuration: FC<{ value: JSONPrimitive }> = ({ value }) => {
  if (value === null) {
    return <DisplayNull />
  } else {
    // TODO
    return <>{value.toString()}</>
  }
}

const DisplayAsTitle: FC<{ value: JSONPrimitive }> = ({ value }) => {
  if (value === null) {
    return <DisplayNull />
  } else {
    return <>{asTitle(value.toString())}</>
  }
}

const DisplayMarkdown: FC<{ value: JSONPrimitive }> = ({ value }) => {
  if (value === null) {
    return <DisplayNull />
  } else {
    // TODO
    return <>{value.toString()}</>
  }
}

const DisplayInlineCode: FC<{ value: JSONPrimitive }> = ({ value }) => {
  if (value === null) {
    return <DisplayNull />
  } else {
    return <code className="fu-inline-code">{value.toString()}</code>
  }
}

export type DataModel = Record<string, JsonData>

export interface DisplayLookupProps extends Omit<Display, 'type' | 'value'> {
  field: string
  tableWidthPercent?: number
}

export function renderEvent(event: AnyEvent | undefined, data: DataModel): AnyEvent | undefined {
  let newEvent: AnyEvent | undefined = event ? { ...event } : undefined
  if (newEvent) {
    if (newEvent.type === 'go-to' && newEvent.url) {
      // for go-to events with a URL, substitute the row values into the url
      const url = subKeys(newEvent.url, data)
      if (url === null) {
        newEvent = undefined
      } else {
        newEvent.url = url
      }
    }
  }
  return newEvent
}

const subKeys = (template: string, row: DataModel): string | null => {
  let returnNull = false
  const r = template.replace(/{(.+?)}/g, (_, key: string): string => {
    const v: JsonData | undefined = row[key]
    if (v === undefined) {
      throw new Error(`field "${key}" not found in ${JSON.stringify(row)}`)
    } else if (v === null) {
      returnNull = true
      return 'null'
    } else {
      return v.toString()
    }
  })
  if (returnNull) {
    return null
  } else {
    return r
  }
}
