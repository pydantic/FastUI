import { FC } from 'react'

import { ClassName } from '../hooks/className'

export interface DarkModeProps {
  type: 'DarkMode'
  className?: ClassName
}

export const DarkModeComp: FC<DarkModeProps> = (props: DarkModeProps) => {
  return <>`${props.type} are not implemented by pure FastUI, implement a component for 'DarkModeProps'.`</>
}
