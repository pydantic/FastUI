import { FC } from 'react'

import type { Details } from '../models'

import { asTitle } from '../tools'
import { useClassName } from '../hooks/className'

import { DisplayComp, DisplayLookupProps, renderEvent } from './display'

export const DetailsComp: FC<Details> = (props) => (
  <dl className={useClassName(props)}>
    {props.fields.map((field, id) => (
      <FieldDetail key={id} props={props} fieldDisplay={field} />
    ))}
  </dl>
)

const FieldDetail: FC<{ props: Details; fieldDisplay: DisplayLookupProps }> = ({ props, fieldDisplay }) => {
  const { field, title, onClick, ...rest } = fieldDisplay
  const value = props.data[field]
  const renderedOnClick = renderEvent(onClick, props.data)
  return (
    <>
      <dt className={useClassName(props, { el: 'dt' })}>{title ?? asTitle(field)}</dt>
      <dd className={useClassName(props, { el: 'dd' })}>
        <DisplayComp type="Display" onClick={renderedOnClick} value={value || null} {...rest} />
      </dd>
    </>
  )
}
