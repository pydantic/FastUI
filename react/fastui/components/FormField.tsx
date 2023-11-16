import { FC, useState } from 'react'

import { ClassName, useClassNameGenerator } from '../hooks/className'

interface Props<T> {
  type: 'FormField'
  // defaults to 'text'
  htmlType: T
  initial?: string | number | boolean
  error?: string
  name: string
  title: string[]
  required: boolean
  locked: boolean
  className?: ClassName
}

type inputHtmlType = 'text' | 'date' | 'datetime-local' | 'time' | 'email' | 'url' | 'file' | 'number'
export type FormFieldProps = Props<inputHtmlType | 'checkbox'>

export const FormFieldComp: FC<FormFieldProps> = (props) => {
  const { htmlType } = props
  if (htmlType === 'checkbox') {
    return <Checkbox {...props} />
  } else {
    return <Input {...(props as Props<inputHtmlType>)} />
  }
}

const Checkbox: FC<FormFieldProps> = (props) => {
  const { className, name, title, required, locked } = props
  return (
    <div className={useClassNameGenerator(className, props)}>
      <label htmlFor={name}>
        <Title title={title} />
      </label>
      <input type="checkbox" defaultChecked={!!props.initial} name={name} required={required} disabled={locked} />
      {props.error ? <div>Error: {props.error}</div> : null}
    </div>
  )
}

const Input: FC<Props<inputHtmlType>> = (props) => {
  const { className, name, title, required, htmlType, locked } = props
  let initial = props.initial ?? ''
  if (typeof initial === 'boolean') {
    initial = initial ? 1 : 0
  }
  const [value, setValue] = useState(initial)

  // TODO placeholder
  return (
    <div className={useClassNameGenerator(className, props)}>
      <label htmlFor={name}>
        <Title title={title} />
      </label>
      <input
        type={htmlType}
        value={value}
        onChange={(e) => setValue(e.target.value)}
        name={name}
        required={required}
        disabled={locked}
      />
      {props.error ? <div>Error: {props.error}</div> : null}
    </div>
  )
}

const Title: FC<{ title: string[] }> = ({ title }) => {
  return (
    <>
      {title.map((t, i) => (
        <span key={i}>
          {i > 0 ? <> &rsaquo;</> : null} {t}
        </span>
      ))}
    </>
  )
}
