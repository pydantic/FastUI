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

  const description = [`The custom component "${subType}"`]
  if (library) {
    description.push(`from library "${library}"`)
  }
  description.push(`has no implementation with this frontend app.`)

  return (
    <DisplayError title="Custom component without implementation" description={description.join(' ')}>
      Custom component data:
      <JsonComp type="JSON" value={data} />
    </DisplayError>
  )
}
