import { createContext, FC } from 'react'
import {FastProps} from '../components'

export type CustomRender = (props: FastProps) => FC | null

export const CustomRenderContext = createContext<CustomRender | null>(null)
