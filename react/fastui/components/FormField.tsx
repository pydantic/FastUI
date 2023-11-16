import { FC, useState } from 'react'

import type { JsonSchemaField, JsonSchemaInput, JsonSchemaBool } from '../JsonSchema'

import { ClassName, useClassNameGenerator } from '../hooks/className'

import { unreachable } from './index'

interface Props<T> {
  type: 'FormField'
  schema: T
  name: string
  title: string
  required: boolean
  className?: ClassName
}

export type FormFieldProps = Props<JsonSchemaField>

export const FormFieldComp: FC<FormFieldProps> = (props) => {
  const { schema } = props
  if (schema.type === 'boolean') {
    return <Checkbox {...(props as Props<JsonSchemaBool>)} />
  } else {
    return <Input {...(props as Props<JsonSchemaInput>)} />
  }
}

const Input: FC<Props<JsonSchemaInput>> = (props) => {
  const { className, name, title, required, schema } = props
  const [value, setValue] = useState(schema.default ?? '')

  // TODO placeholder
  const htmlType = getHtmlType(schema)
  return (
    <div className={useClassNameGenerator(className, props)}>
      <label htmlFor={name}>{title}</label>
      <input
        type={htmlType}
        value={value}
        onChange={(e) => setValue(e.target.value)}
        name={name}
        required={required}
      />
    </div>
  )
}

const Checkbox: FC<Props<JsonSchemaBool>> = (props) => {
  const { className, name, title, required, schema } = props
  const [checked, setChecked] = useState(schema.default ?? false)
  return (
    <div className={useClassNameGenerator(className, props)}>
      <label htmlFor={name}>{title}</label>
      <input
        type="checkbox"
        defaultChecked={checked}
        onChange={() => setChecked((state) => !state)}
        name={name}
        required={required}
      />
    </div>
  )
}

function getHtmlType(schema: JsonSchemaInput): string {
  const { type } = schema
  switch (type) {
    case 'string':
      switch (schema.format) {
        case 'date':
          return 'date'
        case 'date-time':
          return 'datetime-local'
        case 'time':
          return 'time'
        case 'email':
          return 'email'
        case 'uri':
          return 'url'
        case 'uuid':
          return 'text'
        // case 'binary':
        //   return 'file'
        default:
          return 'text'
      }
    case 'number':
    case 'integer':
      return 'number'
    default:
      unreachable('Unexpected JsonSchemaInput type', type)
      throw new Error(`Unknown type: ${type}`)
  }
}
