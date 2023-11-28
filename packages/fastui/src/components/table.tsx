import { FC, CSSProperties } from 'react'

import type { JsonData } from './Json'

import { DisplayChoices, asTitle } from '../display'
import { ClassName, useClassName } from '../hooks/className'
import { AnyEvent } from '../events'

import { DisplayComp } from './display'
import { LinkRender } from './link'

interface ColumnProps {
  field: string
  display?: DisplayChoices
  title?: string
  onClick?: AnyEvent
  widthPercent?: number
  className?: ClassName
}

type Row = Record<string, JsonData>

export interface TableProps {
  type: 'Table'
  data: Row[]
  columns: ColumnProps[]
  className?: ClassName
}

export const TableComp: FC<TableProps> = (props) => {
  const { columns, data } = props

  return (
    <table className={useClassName(props)}>
      <thead>
        <tr>
          {columns.map((col, id) => (
            <th key={id} style={colWidth(col.widthPercent)}>
              {col.title ?? asTitle(col.field)}
            </th>
          ))}
        </tr>
      </thead>
      <tbody>
        {data.map((row, rowId) => (
          <tr key={rowId}>
            {columns.map((column, id) => (
              <Cell key={id} rowId={rowId} row={row} column={column} />
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  )
}

const colWidth = (w: number | undefined): CSSProperties | undefined => (w ? { width: `${w}%` } : undefined)

interface CellProps {
  row: Row
  column: ColumnProps
  rowId: number
}

const Cell: FC<CellProps> = ({ row, column }) => {
  const { field, display, onClick } = column
  const value = row[field]
  let event: AnyEvent | null = onClick ? { ...onClick } : null
  if (event) {
    if (event.type === 'go-to') {
      // for go-to events, substitute the row values into the url
      const url = subKeys(event.url, row)
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

const subKeys = (template: string, row: Row): string | null => {
  let returnNull = false
  const r = template.replace(/{(.+?)}/g, (_, key: string): string => {
    const v: JsonData | undefined = row[key]
    if (v === undefined) {
      throw new Error(`field "${key}" not found in ${JSON.stringify(row)}`)
    } else if (v === null) {
      returnNull = true
      return 'null'
    } else {
      return v.toString()
    }
  })
  if (returnNull) {
    return null
  } else {
    return r
  }
}
