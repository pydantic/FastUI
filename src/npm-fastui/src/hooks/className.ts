import { createContext, useContext } from 'react'

import type { FastClassNameProps } from '../components'
import type { ClassName } from '../models'

import { LocationContext } from './locationContext'

interface ClassNameGeneratorArgs {
  props: FastClassNameProps
  fullPath: string
  subElement?: string
}

export type ClassNameGenerator = (args: ClassNameGeneratorArgs) => ClassName | undefined
export const ClassNameContext = createContext<ClassNameGenerator | null>(null)

interface UseClassNameExtra {
  // default className to use if the class name generator is not set or returns undefined.
  dft?: ClassName
  // identifier of the element within the component to generate the class name for.
  el?: string
}

/**
 * Generates a `className` from `props`, `classNameGenerator` or the default value.
 *
 * @param props The full props object sent from the backend, this is passed to the class name generator.
 * @param extra dft class name or sub-element
 */
export function useClassName(props: FastClassNameProps, extra?: UseClassNameExtra): string | undefined {
  const classNameGenerator = useContext(ClassNameContext)
  const { fullPath } = useContext(LocationContext)
  let { dft, el } = extra || {}
  const genArgs: ClassNameGeneratorArgs = { props, fullPath, subElement: el }

  if (el) {
    // if getting the class for a sub-element, we don't care about `props.ClassName`
    if (classNameGenerator) {
      const generated = classNameGenerator(genArgs)
      if (generated) {
        return renderClassName(classNameGenerator(genArgs))
      }
    }
    return renderClassName(dft)
  } else {
    const { className } = props
    if (combineClassNameProp(className)) {
      if (classNameGenerator) {
        dft = classNameGenerator(genArgs) || dft
      }
      return combine(dft, className)
    } else {
      return renderClassName(className)
    }
  }
}

/**
 * Decide whether we should generate combine the props class name with the generated or default, or not.
 *
 * e.g. if the ClassName contains a `+` if it's an Array or Record, or starts with `+ `
 * then we generate the default className and append the user's className to it.
 * @param classNameProp
 */
function combineClassNameProp(classNameProp?: ClassName): boolean {
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

function combine(cn1?: ClassName, cn2?: ClassName): string {
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
export function renderClassName(className?: ClassName): string {
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
