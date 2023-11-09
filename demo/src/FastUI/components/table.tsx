import { FC } from 'react'
import { ClassName, useClassNameGenerator } from '../hooks/className'

type JSON = string | number | boolean | null | JSON[] | { [key: string]: JSON }

export interface TableProps {
  type: 'Table'
  headings: string[]
  rows: Record<string, JSON>[]
  className?: ClassName
}

// const DisplayValue: FC<{value: JSON}> = ({value}) => {
//   if (value === null) {
//     return <>&mdash;</>
//   } else if (Array.isArray(value)) {
//     const joined = value..join(', ')
//     return <td>{value.map((v, i) => )}</td>
//   } else {
//     return <td>{value.toString()}</td>
//   }
// }

const Cell: FC<{ value: JSON }> = ({ value }) => {
  if (value === null) {
    return <td>&mdash;</td>
  } else if (Array.isArray(value)) {
    const joined = value.join(', ')
    return <td>{joined}</td>
  } else {
    return <td>{value.toString()}</td>
  }
}

export const TableComp: FC<TableProps> = (props) => {
  console.log('TableComp', props)
  const { className, headings, rows } = props

  return (
    <table className={useClassNameGenerator(className, props)}>
      <thead>
        <tr>
          {headings.map((title, id) => (
            <th key={id}>{title}</th>
          ))}
        </tr>
      </thead>
      <tbody>
        {rows.map((row, i) => (
          <tr key={i}>
            {Object.entries(row).map(([key, value]) => (
              <Cell key={key} value={value}/>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  )
}
