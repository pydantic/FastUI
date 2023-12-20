import { FC } from 'react'
import { components, models, renderClassName } from 'fastui'

interface Link {
  Display: FC
  ariaLabel?: string
  locked?: boolean
  active?: boolean
  page?: number
}

export const Pagination: FC<models.Pagination> = (props) => {
  const { page, pageCount } = props

  if (pageCount === 1) return null

  const links: Link[] = [
    {
      Display: () => <span aria-hidden="true">&laquo;</span>,
      ariaLabel: 'Previous',
      locked: page === 1,
      page: page - 1,
    },
    {
      Display: () => <>1</>,
      locked: page === 1,
      active: page === 1,
      page: 1,
    },
  ]

  if (page > 4) {
    links.push({ Display: () => <>...</> })
  }

  for (let p = page - 2; p <= page + 2; p++) {
    if (p <= 1 || p >= pageCount) continue
    links.push({
      Display: () => <>{p}</>,
      locked: page === p,
      active: page === p,
      page: p,
    })
  }

  if (page < pageCount - 3) {
    links.push({ Display: () => <>...</> })
  }

  links.push({
    Display: () => <>{pageCount}</>,
    locked: page === pageCount,
    page: pageCount,
  })

  links.push({
    Display: () => <span aria-hidden="true">&raquo;</span>,
    ariaLabel: 'Next',
    locked: page === pageCount,
    page: page + 1,
  })

  return (
    <nav aria-label="Pagination">
      <ul className="pagination justify-content-center">
        {links.map((link, i) => (
          <PaginationLink key={i} {...link} />
        ))}
      </ul>
    </nav>
  )
}

const PaginationLink: FC<Link> = ({ Display, ariaLabel, locked, active, page }) => {
  if (!page) {
    return (
      <li className="page-item">
        <span className="page-link px-2 text-muted">
          <Display />
        </span>
      </li>
    )
  }
  const className = renderClassName({ 'page-link': true, disabled: locked && !active, active } as models.ClassName)
  let onClick: models.GoToEvent
  if (page === 1) {
    onClick = { type: 'go-to', query: {} }
  } else {
    onClick = { type: 'go-to', query: { page } }
  }
  return (
    <li className="page-item">
      <components.LinkRender onClick={onClick} className={className} locked={locked || active} ariaLabel={ariaLabel}>
        <Display />
      </components.LinkRender>
    </li>
  )
}
