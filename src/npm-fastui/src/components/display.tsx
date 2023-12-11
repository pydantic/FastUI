import { FC } from 'react'

import { useCustomRender } from '../hooks/config'
import { unreachable, asTitle } from '../tools'
import { AnyEvent } from '../events'

import { JsonComp, JsonData } from './Json'
import { LinkRender } from './link'

export enum DisplayMode {
  auto = 'auto',
  plain = 'plain',
  datetime = 'datetime',
  date = 'date',
  duration = 'duration',
  as_title = 'as_title',
  markdown = 'markdown',
  json = 'json',
  inline_code = 'inline_code',
}

export interface DisplayProps {
  type: 'Display'
  /** @TJS-type JSON */
  value?: JsonData
  mode?: DisplayMode
  title?: string
  onClick?: AnyEvent
}

export const DisplayComp: FC<DisplayProps> = (props) => {
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

const DisplayRender: FC<DisplayProps> = (props) => {
  const mode = props.mode ?? DisplayMode.auto
  const value = props.value ?? null
  if (mode === DisplayMode.json) {
    return <JsonComp type="JSON" value={value} />
  } else if (Array.isArray(value)) {
    return <DisplayArray type="DisplayArray" mode={mode} value={value} />
  } else if (typeof value === 'object' && value !== null) {
    return <DisplayObject type="DisplayObject" mode={mode} value={value} />
  } else {
    return <DisplayPrimitive type="DisplayPrimitive" mode={mode} value={value} />
  }
}

interface DisplayArrayProps {
  value: JsonData[]
  mode?: DisplayMode
  type: 'DisplayArray'
}

export const DisplayArray: FC<DisplayArrayProps> = (props) => {
  const CustomRenderComp = useCustomRender(props)
  if (CustomRenderComp) {
    return <CustomRenderComp />
  }
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
  type: 'DisplayObject'
}

export const DisplayObject: FC<DisplayObjectProps> = (props) => {
  const CustomRenderComp = useCustomRender(props)
  if (CustomRenderComp) {
    return <CustomRenderComp />
  }
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
  type: 'DisplayPrimitive'
}

export const DisplayPrimitive: FC<DisplayPrimitiveProps> = (props) => {
  const CustomRenderComp = useCustomRender(props)
  if (CustomRenderComp) {
    return <CustomRenderComp />
  }
  const { mode, value } = props

  switch (mode) {
    case DisplayMode.auto:
      return <DisplayAuto value={value} />
    case DisplayMode.plain:
      return <DisplayPlain value={value} />
    case DisplayMode.datetime:
      return <DisplayDateTime value={value} />
    case DisplayMode.date:
      return <DisplayDate value={value} />
    case DisplayMode.duration:
      return <DisplayDuration value={value} />
    case DisplayMode.as_title:
      return <DisplayAsTitle value={value} />
    case DisplayMode.markdown:
      return <DisplayMarkdown value={value} />
    case DisplayMode.json:
    case DisplayMode.inline_code:
      return <DisplayInlineCode value={value} />
    default:
      unreachable('Unexpected display type', mode, props)
  }
}

export type AllDisplayProps = DisplayProps | DisplayArrayProps | DisplayObjectProps | DisplayPrimitiveProps

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

export type ModelData = Record<string, JsonData>

export interface DisplayLookupProps extends Omit<DisplayProps, 'type' | 'value'> {
  field: string
  tableWidthPercent?: number
}

export function renderEvent(event: AnyEvent | undefined, data: ModelData): AnyEvent | undefined {
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

const subKeys = (template: string, row: ModelData): string | null => {
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
