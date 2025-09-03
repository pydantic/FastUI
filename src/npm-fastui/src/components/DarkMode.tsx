import { FC } from 'react'

import { DarkMode } from '../models'

export const DarkModeComp: FC<DarkMode> = (props: DarkMode) => {
  return <>`${props.type} are not implemented by pure FastUI, implement a component for &apos;DarkModeProps&apos;.`</>
}
