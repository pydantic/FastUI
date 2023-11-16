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

  const defs = formJsonSchema.$defs ?? {}
  return (
    <form ref={formRef} className={useClassNameGenerator(className, props)} onSubmit={onSubmit}>
      <JsonSchemaAnyComp schema={formJsonSchema} loc={[]} required defs={defs} />
      <button type="submit">Submit</button>
    </form>
  )
}

interface JsonSchemaProps<T> {
  schema: T
  loc: js.SchemeLocation
  required: boolean
  defs: js.JsonSchemaDefs
}

const JsonSchemaAnyComp: FC<JsonSchemaProps<js.JsonSchemaAny>> = (props) => {
  const { schema, ...rest } = props
  const concreteSchema = dereferenceJsonSchema(schema, props.defs)

  const { type } = concreteSchema
  switch (type) {
    case 'string':
    case 'number':
    case 'integer':
    case 'boolean':
      return <JsonSchemaFieldComp schema={concreteSchema} {...rest} />
    case 'array':
      return <JsonSchemaArrayComp schema={concreteSchema} {...rest} />
    case 'object':
      return <JsonSchemaObjectComp schema={concreteSchema} {...rest} />
    default:
      unreachable('Unexpected JsonSchema type', type)
      return <div>Unknown type: {type || 'undefined'}</div>
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

const JsonSchemaObjectComp: FC<JsonSchemaProps<js.JsonSchemaObject>> = ({ schema, loc, defs }) => {
  const required = schema.required ?? []
  return (
    <>
      {Object.entries(schema.properties).map(([name, schema]) => (
        <JsonSchemaAnyComp
          key={name}
          schema={schema}
          loc={[...loc, name]}
          required={required.includes(name)}
          defs={defs}
        />
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
 * specifically convert `'on` from checkboxes into a `true`.
 * @param formSchema
 * @param path
 * @param value
 */
function convertValue(formSchema: js.JsonSchemaObject, path: js.SchemeLocation, value: FormDataEntryValue): JsonData {
  const defs = formSchema.$defs ?? {}
  const schema = path.reduce((acc: js.JsonSchemaConcrete, currentKey) => {
    if (acc.type !== 'object') {
      throw new Error(`Invalid path ${path.join('.')} for schema ${JSON.stringify(acc)}`)
    }
    const s = acc.properties[currentKey]
    if (s === undefined) {
      throw new Error(`Invalid path ${path} for schema ${JSON.stringify(schema)}`)
    }
    return dereferenceJsonSchema(s, defs)
  }, formSchema)

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

/**
 * Convert a schema which might be a reference to a concrete schema.
 * @param schema
 * @param defs
 */
function dereferenceJsonSchema(schema: js.JsonSchemaAny, defs?: js.JsonSchemaDefs): js.JsonSchemaConcrete {
  if ('$ref' in schema) {
    defs = defs ?? {}
    const defSchema = defs[schema.$ref.slice('#/$defs/'.length)]
    if (defSchema === undefined) {
      throw new Error(`Invalid $ref "${schema.$ref}", not found in ${JSON.stringify(defs)}`)
    } else {
      return defSchema
    }
  } else {
    return schema
  }
}
