import { FC } from 'react'

import { useCustomRender } from '../hooks/customRender'
import { DisplayChoices, asTitle } from '../display'
import { unreachable } from '../tools'

import { JsonComp, JsonData } from './Json'

interface DisplayProps {
  type: 'Display'
  display?: DisplayChoices
  value?: JsonData
}

export const DisplayComp: FC<DisplayProps> = (props) => {
  const CustomRenderComp = useCustomRender(props)
  if (CustomRenderComp) {
    return <CustomRenderComp />
  }

  const display = props.display ?? DisplayChoices.auto
  const value = props.value ?? null
  if (display === DisplayChoices.json) {
    return <JsonComp type="JSON" value={value} />
  } else if (Array.isArray(value)) {
    return <DisplayArray type="DisplayArray" display={display} value={value} />
  } else if (typeof value === 'object' && value !== null) {
    return <DisplayObject type="DisplayObject" display={display} value={value} />
  } else {
    return <DisplayPrimitive type="DisplayPrimitive" display={display} value={value} />
  }
}

interface DisplayArrayProps {
  value: JsonData[]
  display?: DisplayChoices
  type: 'DisplayArray'
}

export const DisplayArray: FC<DisplayArrayProps> = (props) => {
  const CustomRenderComp = useCustomRender(props)
  if (CustomRenderComp) {
    return <CustomRenderComp />
  }
  const { display, value } = props

  return (
    <>
      {value.map((v, i) => (
        <span key={i}>
          <DisplayComp type="Display" display={display} value={v} />,{' '}
        </span>
      ))}
    </>
  )
}

interface DisplayObjectProps {
  value: { [key: string]: JsonData }
  display?: DisplayChoices
  type: 'DisplayObject'
}

export const DisplayObject: FC<DisplayObjectProps> = (props) => {
  const CustomRenderComp = useCustomRender(props)
  if (CustomRenderComp) {
    return <CustomRenderComp />
  }
  const { display, value } = props

  return (
    <>
      {Object.entries(value).map(([key, v], i) => (
        <span key={key}>
          {key}: <DisplayComp type="Display" display={display} key={i} value={v} />,{' '}
        </span>
      ))}
    </>
  )
}

type JSONPrimitive = string | number | boolean | null

interface DisplayPrimitiveProps {
  value: JSONPrimitive
  display: DisplayChoices
  type: 'DisplayPrimitive'
}

export const DisplayPrimitive: FC<DisplayPrimitiveProps> = (props) => {
  const CustomRenderComp = useCustomRender(props)
  if (CustomRenderComp) {
    return <CustomRenderComp />
  }
  const { display, value } = props

  switch (display) {
    case DisplayChoices.auto:
      return <DisplayAuto value={value} />
    case DisplayChoices.plain:
      return <DisplayPlain value={value} />
    case DisplayChoices.datetime:
      return <DisplayDateTime value={value} />
    case DisplayChoices.date:
      return <DisplayDate value={value} />
    case DisplayChoices.duration:
      return <DisplayDuration value={value} />
    case DisplayChoices.as_title:
      return <DisplayAsTitle value={value} />
    case DisplayChoices.markdown:
      return <DisplayMarkdown value={value} />
    case DisplayChoices.json:
    case DisplayChoices.inline_code:
      return <DisplayInlineCode value={value} />
    default:
      unreachable('Unexpected display type', display, props)
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
    return <>{value.toString()}</>
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
