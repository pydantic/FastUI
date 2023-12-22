import { FC, CSSProperties } from 'react'

import type { Table } from '../models'

import { asTitle } from '../tools'
import { useClassName } from '../hooks/className'

import { DisplayComp, DisplayLookupProps, DataModel, renderEvent } from './display'

export const TableComp: FC<Table> = (props) => {
  const { columns, data, noDataMessage } = props
  const noDataClassName = useClassName(props, { el: 'no-data-message' })

  return (
    <table className={useClassName(props)}>
      <thead>
        <tr>
          {columns.map((col, id) => (
            <th key={id} style={colWidth(col.tableWidthPercent)}>
              {col.title ?? asTitle(col.field)}
            </th>
          ))}
        </tr>
      </thead>
      <tbody>
        {data.map((row, rowId) => (
          <tr key={rowId}>
            {columns.map((column, id) => (
              <Cell key={id} row={row} column={column} />
            ))}
          </tr>
        ))}
      </tbody>
      {data.length === 0 && <caption className={noDataClassName}>{noDataMessage || 'No data'}</caption>}
    </table>
  )
}

const colWidth = (w: number | undefined): CSSProperties | undefined => (w ? { width: `${w}%` } : undefined)

const Cell: FC<{ row: DataModel; column: DisplayLookupProps }> = ({ row, column }) => {
  const { field, onClick, ...rest } = column
  const value = row[field]
  const renderedOnClick = renderEvent(onClick, row)
  return (
    <td>
      <DisplayComp type="Display" onClick={renderedOnClick} value={value || null} {...rest} />
    </td>
  )
}
