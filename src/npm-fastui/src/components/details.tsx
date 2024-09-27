import { FC } from 'react'

import type { Details, Display, DisplayMode } from '../models'

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

const FieldDetail: FC<{ props: Details; fieldDisplay: DisplayLookupProps | Display }> = ({ props, fieldDisplay }) => {
  const onClick = fieldDisplay.onClick
  let title = fieldDisplay.title
  const rest: { mode?: DisplayMode; tableWidthPercent?: number } = { mode: fieldDisplay.mode }
  let value: any

  if ('type' in fieldDisplay && fieldDisplay.type === 'Display') {
    // fieldDisplay is Display
    value = fieldDisplay.value
  } else if ('field' in fieldDisplay) {
    // fieldDisplay is DisplayLookupProps
    const field = fieldDisplay.field
    title = title ?? asTitle(field)
    value = props.data[field]
    rest.tableWidthPercent = fieldDisplay.tableWidthPercent
  }
  const renderedOnClick = renderEvent(onClick, props.data)
  return (
    <>
      <dt className={useClassName(props, { el: 'dt' })}>{title}</dt>
      <dd className={useClassName(props, { el: 'dd' })}>
        <DisplayComp type="Display" onClick={renderedOnClick} value={value !== undefined ? value : null} {...rest} />
      </dd>
    </>
  )
}
