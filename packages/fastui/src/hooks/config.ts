import { createContext, FC, useContext } from 'react'

import type { CustomRender } from '../index'

import { FastProps } from '../components'

interface Config {
  rootUrl: string
  // defaults to 'append'
  pathSendMode?: 'append' | 'query'
  customRender?: CustomRender
  Loading?: FC
}

export const ConfigContext = createContext<Config>({ rootUrl: '' })

export const useCustomRender = (props: FastProps): FC | void => {
  const { customRender } = useContext(ConfigContext)

  if (customRender) {
    return customRender(props)
  }
}
