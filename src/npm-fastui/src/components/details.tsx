import { FC } from 'react'

import { asTitle } from '../tools'
import { ClassName, useClassName } from '../hooks/className'

import { DisplayComp, DisplayLookupProps, DataModel, renderEvent } from './display'

export interface DetailsProps {
  type: 'Details'
  data: DataModel
  fields: DisplayLookupProps[]
  className?: ClassName
}

export const DetailsComp: FC<DetailsProps> = (props) => (
  <dl className={useClassName(props)}>
    {props.fields.map((field, id) => (
      <FieldDetail key={id} props={props} fieldDisplay={field} />
    ))}
  </dl>
)

const FieldDetail: FC<{ props: DetailsProps; fieldDisplay: DisplayLookupProps }> = ({ props, fieldDisplay }) => {
  const { field, title, onClick, ...rest } = fieldDisplay
  const value = props.data[field]
  const renderedOnClick = renderEvent(onClick, props.data)
  return (
    <>
      <dt className={useClassName(props, { el: 'dt' })}>{title ?? asTitle(field)}</dt>
      <dd className={useClassName(props, { el: 'dd' })}>
        <DisplayComp type="Display" onClick={renderedOnClick} value={value} {...rest} />
      </dd>
    </>
  )
}
