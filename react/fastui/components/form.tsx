import { FC, FormEvent, useRef } from 'react'

import type * as js from '../JsonSchema'

import { ClassName, useClassNameGenerator } from '../hooks/className'
import { useFireEvent, PageEvent } from '../hooks/event'
import { useCustomRender } from '../hooks/customRender'

import { unreachable } from './index'

import { FormFieldProps, FormFieldComp } from './FormField'
import { JsonData } from './Json'

export interface FormProps {
  type: 'Form'
  formJsonSchema: js.JsonSchemaObject
  submitTrigger?: PageEvent
  submitUrl?: string
  nextUrl?: string
  className?: ClassName
}

export const FormComp: FC<FormProps> = (props) => {
  const formRef = useRef<HTMLFormElement>(null)
  const { className, formJsonSchema, submitTrigger, submitUrl, nextUrl } = props

  const { fireEvent } = useFireEvent()

  const onSubmit = (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    const formData = new FormData(formRef.current!)
    const entries = unflatten(formData, formJsonSchema)
    console.log({ submitUrl, nextUrl, entries })
    fireEvent(submitTrigger)
  }

  return (
    <form ref={formRef} className={useClassNameGenerator(className, props)} onSubmit={onSubmit}>
      <JsonSchemaAnyComp schema={formJsonSchema} loc={[]} required />
      <button type="submit">Submit</button>
    </form>
  )
}

interface JsonSchemaProps<T> {
  schema: T
  loc: js.SchemeLocation
  required: boolean
}

const JsonSchemaAnyComp: FC<JsonSchemaProps<js.JsonSchemaAny>> = ({ schema, loc, required }) => {
  const { type } = schema
  switch (type) {
    case 'string':
    case 'number':
    case 'integer':
    case 'boolean':
      return <JsonSchemaFieldComp schema={schema} loc={loc} required={required} />
    case 'array':
      return <JsonSchemaArrayComp schema={schema} loc={loc} required={required} />
    case 'object':
      return <JsonSchemaObjectComp schema={schema} loc={loc} required={required} />
    default:
      unreachable('Unexpected JsonSchema type', type)
      return <div>Unknown type: {type}</div>
  }
}

const JsonSchemaFieldComp: FC<JsonSchemaProps<js.JsonSchemaField>> = (props) => {
  const { loc, ...rest } = props
  const title = props.schema.title ?? loc[loc.length - 1]!.toString()
  const name = serializeLoc(loc)
  const formFieldProps: FormFieldProps = { type: 'FormField', title, name, ...rest }
  const CustomRenderComp = useCustomRender(formFieldProps)
  if (CustomRenderComp) {
    return <CustomRenderComp />
  } else {
    return <FormFieldComp {...formFieldProps} />
  }
}

const JsonSchemaObjectComp: FC<JsonSchemaProps<js.JsonSchemaObject>> = ({ schema, loc }) => {
  const required = schema.required ?? []
  return (
    <>
      {Object.entries(schema.properties).map(([name, schema]) => (
        <JsonSchemaAnyComp key={name} schema={schema} loc={[...loc, name]} required={required.includes(name)} />
      ))}
    </>
  )
}

const JsonSchemaArrayComp: FC<JsonSchemaProps<js.JsonSchemaArray>> = () => {
  return <div>TODO: array schema</div>
}

/**
 * Convert a location like `['foo', 'bar', 'baz']` into a flattened key like `foo.bar.baz`, uses JSON if any
 * of the values contains a `.` or `[` character.
 * @param loc
 */
function serializeLoc(loc: js.SchemeLocation) {
  if (loc.some((v) => typeof v === 'string' && (v.includes('.') || v.includes('[')))) {
    return JSON.stringify(loc)
  } else {
    return loc.join('.')
  }
}

function deserializeLoc(loc: string): js.SchemeLocation {
  if (loc.startsWith('[')) {
    return JSON.parse(loc)
  } else {
    return loc.split('.')
  }
}

/**
 * Convert the form data with flattened keys like `foo.bar.baz` into a nested object that matches the schema
 */
function unflatten(formData: FormData, formSchema: js.JsonSchemaObject) {
  const pairs = [...formData.entries()]
  return pairs.reduce((accumulator: Record<string, JsonData>, [key, value]) => {
    deserializeLoc(key).reduce((acc: Record<string, JsonData>, currentKey, i, path): any => {
      if (i === path.length - 1) {
        acc[currentKey] = convertValue(formSchema, path, value)
      } else if (acc[currentKey] === undefined) {
        acc[currentKey] = {}
      }
      return acc[currentKey]
    }, accumulator)
    return accumulator
  }, {})
}

/**
 * Convert a value from a form input into the correct type for the schema,
 * specifically convert `'on` from checkboxes into a `true`
 */
function convertValue(formSchema: js.JsonSchemaObject, path: js.SchemeLocation, value: FormDataEntryValue): JsonData {
  const schema = path.reduce((acc: js.JsonSchemaAny, currentKey) => {
    if (acc.type !== 'object') {
      throw new Error(`Invalid path ${path.join('.')} for schema ${JSON.stringify(schema)}`)
    }
    const s = acc.properties[currentKey]
    if (s === undefined) {
      throw new Error(`Invalid path ${path} for schema ${JSON.stringify(schema)}`)
    }
    return s
  }, formSchema)
  console.log({ formSchema, path, schema, value })

  if (typeof value === 'string') {
    const { type } = schema
    switch (type) {
      case 'string':
      case 'array':
      case 'object':
        return value
      case 'number':
      case 'integer':
        return Number(value)
      case 'boolean':
        return value === 'on'
      default:
        unreachable('Unexpected schema type', type)
        return value
    }
  } else {
    throw new Error('Files not yet supported')
  }
}
