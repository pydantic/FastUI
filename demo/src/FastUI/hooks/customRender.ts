import { createContext, FC, useContext } from 'react'
import { FastProps } from '../components'

export type CustomRender = (props: FastProps) => FC | void

export const CustomRenderContext = createContext<CustomRender | null>(null)

export const useCustomRender = (props: FastProps): FC | void => {
  const customRender = useContext(CustomRenderContext)

  if (customRender) {
    return customRender(props)
  }
}
