import { FC, useState } from 'react'

import { ClassName, useClassNameGenerator } from '../hooks/className'

interface BaseFormFieldProps {
  name: string
  title: string[]
  required: boolean
  locked: boolean
  error?: string
  className?: ClassName
}

export type FormFieldProps = FormFieldInputProps | FormFieldCheckboxProps | FormFieldSelectProps | FormFieldFileProps

interface FormFieldInputProps extends BaseFormFieldProps {
  type: 'FormFieldInput'
  htmlType?: 'text' | 'date' | 'datetime-local' | 'time' | 'email' | 'url' | 'file' | 'number'
  initial?: string | number
}

export const FormFieldInputComp: FC<FormFieldInputProps> = (props) => {
  const { className, name, title, required, htmlType, locked } = props
  const [value, setValue] = useState(props.initial ?? '')

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

interface FormFieldCheckboxProps extends BaseFormFieldProps {
  type: 'FormFieldCheckbox'
  initial?: boolean
}

export const FormFieldCheckboxComp: FC<FormFieldCheckboxProps> = (props) => {
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

interface FormFieldSelectProps extends BaseFormFieldProps {
  type: 'FormFieldSelect'
  choices: [string, string][]
  initial?: string
}

export const FormFieldSelectComp: FC<FormFieldSelectProps> = (props) => {
  const { className, name, title, required, locked, choices } = props
  const [value, setValue] = useState(props.initial ?? '')

  return (
    <div className={useClassNameGenerator(className, props)}>
      <label htmlFor={name}>
        <Title title={title} />
      </label>
      <select
        value={value}
        onChange={(e) => setValue(e.target.value)}
        name={name}
        required={required}
        disabled={locked}
      >
        <option></option>
        {choices.map(([value, label]) => (
          <option key={value} value={value}>
            {label}
          </option>
        ))}
      </select>
      {props.error ? <div>Error: {props.error}</div> : null}
    </div>
  )
}

interface FormFieldFileProps extends BaseFormFieldProps {
  type: 'FormFieldFile'
  multiple: boolean
  accept?: string
}

export const FormFieldFileComp: FC<FormFieldFileProps> = (props) => {
  const { className, name, title, required, locked, multiple, accept } = props

  return (
    <div className={useClassNameGenerator(className, props)}>
      <label htmlFor={name}>
        <Title title={title} />
      </label>
      <input type="file" name={name} required={required} disabled={locked} multiple={multiple} accept={accept} />
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
