import { FC } from 'react'

import { ClassName, useClassName } from '../hooks/className'

import { FastProps, RenderChildren } from './index'

interface DivProps {
  type: 'Div'
  children: FastProps[]
  className?: ClassName
}

interface PageProps {
  type: 'Page'
  children: FastProps[]
  className?: ClassName
}

interface RowProps {
  type: 'Row'
  children: FastProps[]
  className?: ClassName
}

interface ColProps {
  type: 'Col'
  children: FastProps[]
  className?: ClassName
}

export type AllDivProps = DivProps | PageProps | RowProps | ColProps
type AllDivTypes = 'Div' | 'Page' | 'Row' | 'Col'

interface Props {
  type: AllDivTypes
  children: FastProps[]
  className?: ClassName
}

export const DivComp: FC<Props> = (props) => (
  <div className={useClassName(props)}>
    <RenderChildren children={props.children} />
  </div>
)
