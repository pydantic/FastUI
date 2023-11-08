import { ClassName, useClassNameGenerator } from '../hooks/className'
import { FastProps, AnyComp } from './index'
import { FC } from 'react'

interface DivProps {
  type: 'Div'
  children: FastProps[]
  className?: ClassName
}

interface ContainerProps {
  type: 'Container'
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

export type AllDivProps = DivProps | ContainerProps | RowProps | ColProps
type AllDivTypes = 'Div' | 'Container' | 'Row' | 'Col'

interface Props {
  type: AllDivTypes
  children: FastProps[]
  className?: ClassName
}

export const DivComp: FC<Props> = (props) => (
  <div className={useClassNameGenerator(props.className, props)}>
    {props.children.map((child, i) => (
      <AnyComp key={i} {...child} />
    ))}
  </div>
)
