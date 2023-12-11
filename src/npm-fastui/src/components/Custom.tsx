import { FC, useContext } from 'react'

import { ClassName } from '../hooks/className'
import { ErrorContext } from '../hooks/error'

import { JsonData, JsonComp } from './Json'

export interface CustomProps {
  type: 'Custom'
  data: JsonData
  subType: string
  library?: string
  className?: ClassName
}

export const CustomComp: FC<CustomProps> = (props) => {
  const { data, subType, library } = props
  const { DisplayError } = useContext(ErrorContext)

  let description = `Custom component "${subType}"`
  if (library) {
    description += ` from library "${library}"`
  }
  description += ` has no custom implementation.`

  return (
    <DisplayError title="Custom component without implementation" description={description}>
      Custom component data:
      <JsonComp type="JSON" value={data} />
    </DisplayError>
  )
}
