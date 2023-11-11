import { FC } from 'react'
import { ClassName, useClassNameGenerator } from '../hooks/className'
import { PageEvent, GoToEvent } from '../hooks/event'
import {as_title, DisplayChoices, DisplayComp } from './display'
import { LinkRender } from './link'
import type { JSON } from './Json'

interface ColumnProps {
  field: string
  display?: DisplayChoices
  title?: string
  onClick?: PageEvent | GoToEvent
  className?: ClassName
}

type Row = Record<string, JSON>

export interface TableProps {
  type: 'Table'
  data: Row[]
  columns: ColumnProps[]
  className?: ClassName
}

export const TableComp: FC<TableProps> = (props) => {
  const { className, columns, data } = props

  return (
    <table className={useClassNameGenerator(className, props)}>
      <thead>
        <tr>
          {columns.map((col, id) => (
            <th key={id}>{col.title ?? as_title(col.field)}</th>
          ))}
        </tr>
      </thead>
      <tbody>
        {data.map((row, row_id) => (
          <tr key={row_id}>
            {columns.map((column, id) => (
              <Cell key={id} row_id={row_id} row={row} column={column} />
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  )
}

interface CellProps {
  row: Row
  column: ColumnProps
  row_id: number
}

const Cell: FC<CellProps> = ({ row, column }) => {
  const { field, display, onClick } = column
  const value = row[field]
  let event: PageEvent | GoToEvent | null = onClick ? { ...onClick } : null
  if (event) {
    if (event.type === 'go-to') {
      // for go-to events, substitute the row values into the url
      const url = sub_keys(event.url, row)
      if (url === null) {
        event = null
      } else {
        event.url = url
      }
    }
  }
  if (event) {
    return (
      <td>
        <LinkRender onClick={event}>
          <DisplayComp type="Display" display={display} value={value} />
        </LinkRender>
      </td>
    )
  } else {
    return (
      <td>
        <DisplayComp type="Display" display={display} value={value} />
      </td>
    )
  }
}

const sub_keys = (template: string, row: Row): string | null => {
  let return_null = false
  const r = template.replace(/{(.+?)}/g, (_, key: string): string => {
    const v: JSON | undefined = row[key]
    if (v === undefined) {
      throw new Error(`field "${key}" not found in ${JSON.stringify(row)}`)
    } else if (v === null) {
      return_null = true
      return 'null'
    } else {
      return v.toString()
    }
  })
  if (return_null) {
    return null
  } else {
    return r
  }
}
