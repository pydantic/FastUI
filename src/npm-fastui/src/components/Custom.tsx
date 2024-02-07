import { FC } from 'react'

import type { Custom } from '../models'

import { DisplayError } from '../hooks/error'

import { JsonComp } from './Json'

export const CustomComp: FC<Custom> = (props) => {
  const { data, subType, library } = props

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
