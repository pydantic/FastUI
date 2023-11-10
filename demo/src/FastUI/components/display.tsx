import { FC } from 'react'

export type JSON = string | number | boolean | null | JSON[] | { [key: string]: JSON }

// eslint-disable-next-line react-refresh/only-export-components
export enum DisplayChoices {
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
  display?: DisplayChoices
  value?: JSON
}

export const DisplayComp: FC<DisplayProps> = ({ value, display }) => {
  display = display ?? DisplayChoices.auto
  value = value ?? null
  if (display == DisplayChoices.json) {
    return <DisplayJsonComp value={value} />
  } else if (Array.isArray(value)) {
    return <DisplayArray display={display} value={value} />
  } else if (typeof value === 'object' && value !== null) {
    return <DisplayObject display={display} value={value} />
  }

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
    case DisplayChoices.inline_code:
      return <DisplayInlineCode value={value} />
  }
}

const DisplayJsonComp: FC<{ value: JSON }> = ({ value }) => {
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

const DisplayArray: FC<{ display?: DisplayChoices; value: JSON[] }> = ({ display, value }) => (
  <>
    {value.map((v, i) => (
      <span key={i}>
        <DisplayComp display={display} value={v} />,{' '}
      </span>
    ))}
  </>
)

const DisplayObject: FC<{ display?: DisplayChoices; value: { [key: string]: JSON } }> = ({ display, value }) => (
  <>
    {Object.entries(value).map(([key, v], i) => (
      <span key={key}>
        {key}: <DisplayComp display={display} key={i} value={v} />,{' '}
      </span>
    ))}
  </>
)

type JSONPrimitive = string | number | boolean | null

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

// usage as_title('what_ever') > 'What Ever'
// eslint-disable-next-line react-refresh/only-export-components
export const as_title = (s: string): string => s.replace(/(_|-)/g, ' ').replace(/(_|\b)\w/g, (l) => l.toUpperCase())

const DisplayAsTitle: FC<{ value: JSONPrimitive }> = ({ value }) => {
  if (value === null) {
    return <DisplayNull />
  } else {
    return <>{as_title(value.toString())}</>
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
