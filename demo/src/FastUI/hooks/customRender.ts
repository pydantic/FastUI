import { createContext, FC, useContext } from 'react'
import { FastProps } from '../components'

export type CustomRender = (props: FastProps) => FC | null

export const CustomRenderContext = createContext<CustomRender | null>(null)

export const useCustomRender = (props: FastProps): FC | null => {
  const customRender = useContext(CustomRenderContext)

  if (customRender) {
    return customRender(props)
  } else {
    return null
  }
}
