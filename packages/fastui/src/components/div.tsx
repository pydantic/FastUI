import { FC } from 'react'

import { ClassName, useClassName } from '../hooks/className'

import { FastProps, AnyCompList } from './index'

interface DivProps {
  type: 'Div'
  components: FastProps[]
  className?: ClassName
}

interface PageProps {
  type: 'Page'
  components: FastProps[]
  className?: ClassName
}

interface RowProps {
  type: 'Row'
  components: FastProps[]
  className?: ClassName
}

interface ColProps {
  type: 'Col'
  components: FastProps[]
  className?: ClassName
}

export type AllDivProps = DivProps | PageProps | RowProps | ColProps
type AllDivTypes = 'Div' | 'Page' | 'Row' | 'Col'

interface Props {
  type: AllDivTypes
  components: FastProps[]
  className?: ClassName
}

export const DivComp: FC<Props> = (props) => (
  <div className={useClassName(props)}>
    <AnyCompList propsList={props.components} />
  </div>
)
