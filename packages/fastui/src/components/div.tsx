import { FC } from 'react'

import { ClassName, useClassName } from '../hooks/className'

import { FastProps, AnyCompList } from './index'

export interface DivProps {
  type: 'Div'
  components: FastProps[]
  className?: ClassName
}

interface PageProps {
  type: 'Page'
  components: FastProps[]
  className?: ClassName
}

export type AllDivProps = DivProps | PageProps

export const DivComp: FC<AllDivProps> = (props) => (
  <div className={useClassName(props)}>
    <AnyCompList propsList={props.components} />
  </div>
)
