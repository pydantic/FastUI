import {createContext, useContext} from 'react'
import type {CompTypes} from './components'

export type ClassName = string | string[] | Record<string, boolean | null> | undefined

export type ClassNameFunction = (type: CompTypes, nested?: string) => ClassName
export const ClassNameContext = createContext<ClassNameFunction | null>(null)

export function ClassNameGenerator(className: ClassName, type: CompTypes, nested?: string): string {
  const defaultClassName = useContext(ClassNameContext)
  if (defaultClassName !== null && generateDefault(className)) {
    const dft = defaultClassName(type, nested)
    return combine(dft, className)
  } else {
    return renderClassName(className)
  }
}

/**
 * Checks whether the default className should be generated.
 *
 * e.g. if the ClassName contains a `+` if it's an Array or Record, or starts with `+ `
 * then we generate the default className and append the user's className to it.
 * @param className
 */
function generateDefault(className: ClassName): boolean {
  if (Array.isArray(className)) {
    // className is an array, check if it contains `+`
    return className.some(c => c == '+')
  } else if (typeof className === 'string') {
    // className is a string, check if it starts with `+ `
    return /^\+ /.test(className)
  } else if (typeof className === 'object') {
    // className is an object, check if its keys contain `+`
    return Object.keys(className).some(key => key === '+')
  } else {
    // className is undefined, return false
    return true
  }
}

function combine(cn1: ClassName, cn2: ClassName): string {
  if (!cn1) {
    return renderClassName(cn2)
  } else if (!cn2) {
    return renderClassName(cn1)
  } else {
    return renderClassName(cn1) + ' ' + renderClassName(cn2)
  }
}

/**
 * Renders the className to a string, removing plus signs.
 * @param className
 */
function renderClassName(className: ClassName): string {
  if (typeof className === 'string') {
    return className.replace(/^\+ /, '')
  } else if (Array.isArray(className)) {
    return className.filter(c => c != '+') .join(' ')
  } else if (typeof className === 'object') {
    return Object.entries(className).filter(([key, value]) => key !== '+' && !!value).map(([key]) => key).join(' ')
  } else {
    return ''
  }
}
