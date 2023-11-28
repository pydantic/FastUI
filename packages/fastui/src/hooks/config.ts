import { createContext, FC, useContext } from 'react'

import type { FastUIProps } from '../index'

import { FastProps } from '../components'

type Config = Omit<FastUIProps, 'DisplayError' | 'classNameGenerator' | 'devMode'>

export const ConfigContext = createContext<Config>({ rootUrl: '' })

export const useCustomRender = (props: FastProps): FC | void => {
  const { customRender } = useContext(ConfigContext)

  if (customRender) {
    return customRender(props)
  }
}
