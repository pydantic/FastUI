import { createContext, useContext } from 'react'

import type { FastProps } from '../components'

export type ClassName = string | ClassName[] | Record<string, boolean | null> | undefined

export type ClassNameGenerator = (props: FastProps) => ClassName
export const ClassNameContext = createContext<ClassNameGenerator | null>(null)

/**
 * Generates a `className` from a component.
 *
 * @param classNameProp The `className` taken from the props sent from the backend.
 * @param props The full props object sent from the backend, this is passed to the class name generator.
 * @param dft default className to use if the class name generator is not set or returns undefined.
 */
export function useClassNameGenerator(classNameProp: ClassName, props: FastProps, dft?: ClassName): string {
  const classNameGenerator = useContext(ClassNameContext)
  if (combineClassNameProp(classNameProp)) {
    if (!dft && classNameGenerator) {
      dft = classNameGenerator(props)
    }
    return combine(dft, classNameProp)
  } else {
    return renderClassName(classNameProp)
  }
}

/**
 * Decide whether we should generate combine the props class name with the generated or default, or not.
 *
 * e.g. if the ClassName contains a `+` if it's an Array or Record, or starts with `+ `
 * then we generate the default className and append the user's className to it.
 * @param classNameProp
 */
function combineClassNameProp(classNameProp: ClassName): boolean {
  if (Array.isArray(classNameProp)) {
    // classNameProp is an array, check if it contains `+`
    return classNameProp.some((c) => c === '+')
  } else if (typeof classNameProp === 'string') {
    // classNameProp is a string, check if it starts with `+ `
    return /^\+ /.test(classNameProp)
  } else if (typeof classNameProp === 'object') {
    // classNameProp is an object, check if its keys contain `+`
    return Object.keys(classNameProp).some((key) => key === '+')
  } else {
    // classNameProp is undefined, return true as we want to generate the default className
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
export function renderClassName(className: ClassName): string {
  if (typeof className === 'string') {
    return className.replace(/^\+ /, '')
  } else if (Array.isArray(className)) {
    return className
      .filter((c) => c !== '+')
      .map(renderClassName)
      .join(' ')
  } else if (typeof className === 'object') {
    return Object.entries(className)
      .filter(([key, value]) => key !== '+' && !!value)
      .map(([key]) => key)
      .join(' ')
  } else {
    return ''
  }
}
