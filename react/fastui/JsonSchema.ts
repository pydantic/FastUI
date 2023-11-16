/* eslint-disable no-use-before-define */

export type JsonSchemaInput = JsonSchemaString | JsonSchemaInt | JsonSchemaNumber
export type JsonSchemaField = JsonSchemaInput | JsonSchemaBool

export type JsonSchemaAny = JsonSchemaField | JsonSchemaArray | JsonSchemaObject

export type SchemeLocation = (string | number)[]

interface JsonSchemaBase {
  title?: string
  description?: string
}

export interface JsonSchemaString extends JsonSchemaBase {
  type: 'string'
  default?: string
  format?: 'date' | 'date-time' | 'time' | 'email' | 'uri' | 'uuid'
}

export interface JsonSchemaBool extends JsonSchemaBase {
  type: 'boolean'
  default?: boolean
}

export interface JsonSchemaInt extends JsonSchemaBase {
  type: 'integer'
  default?: number
  minimum?: number
  exclusiveMinimum?: number
  maximum?: number
  exclusiveMaximum?: number
  multipleOf?: number
}

export interface JsonSchemaNumber extends JsonSchemaBase {
  type: 'number'
  default?: number
  minimum?: number
  exclusiveMinimum?: number
  maximum?: number
  exclusiveMaximum?: number
  multipleOf?: number
}

export interface JsonSchemaArray extends JsonSchemaBase {
  type: 'array'
  minItems?: number
  maxItems?: number
  prefixItems?: JsonSchemaAny[]
  items?: JsonSchemaAny
}

export interface JsonSchemaObject extends JsonSchemaBase {
  type: 'object'
  properties: Record<string, JsonSchemaAny>
  required?: string[]
}
