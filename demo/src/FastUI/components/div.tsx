import {ClassName, ClassNameGenerator} from '../ClassName'
import {AnyComp, AnyCompRender} from '../components'
import {FC} from 'react'

interface Div {
  type: 'Div'
  children: AnyComp[]
  className?: ClassName
}

interface Container {
  type: 'Container'
  children: AnyComp[]
  className?: ClassName
}

interface Row {
  type: 'Row'
  children: AnyComp[]
  className?: ClassName
}

interface Col {
  type: 'Col'
  children: AnyComp[]
  className?: ClassName
}

export type DivComp = Div | Container | Row | Col
export type DivTypes = 'Div' | 'Container' | 'Row' | 'Col'

interface AnyDiv {
  type: 'Div' | 'Container' | 'Row' | 'Col'
  children: AnyComp[]
  className?: ClassName
}

export const DivRender: FC<AnyDiv> = ({type, children, className}) => (
  <div className={ClassNameGenerator(className, type)}>
    {children.map((child, i) => <AnyCompRender key={i} {...child} />)}
  </div>
)
