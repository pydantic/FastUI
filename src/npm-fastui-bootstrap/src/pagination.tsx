import { FC } from 'react'
import { components, models, renderClassName } from 'fastui'

interface Link {
  Display: FC
  ariaLabel?: string
  locked?: boolean
  active?: boolean
  page?: number
  pageQueryParam?: string
}

export const Pagination: FC<models.Pagination> = (props) => {
  const { page, pageCount, pageQueryParam } = props
  if (pageCount === 1) return null

  const links: Link[] = [
    {
      Display: () => <span aria-hidden="true">&laquo;</span>,
      ariaLabel: 'Previous',
      locked: page === 1,
      page: page - 1,
      pageQueryParam,
    },
    {
      Display: () => <>1</>,
      locked: page === 1,
      active: page === 1,
      page: 1,
      pageQueryParam,
    },
  ]

  if (page > 4) {
    links.push({ Display: () => <>...</>, pageQueryParam })
  }

  for (let p = page - 2; p <= page + 2; p++) {
    if (p <= 1 || p >= pageCount) continue
    links.push({
      Display: () => <>{p}</>,
      locked: page === p,
      active: page === p,
      page: p,
      pageQueryParam,
    })
  }

  if (page < pageCount - 3) {
    links.push({ Display: () => <>...</>, pageQueryParam })
  }

  links.push({
    Display: () => <>{pageCount}</>,
    locked: page === pageCount,
    page: pageCount,
    pageQueryParam,
  })

  links.push({
    Display: () => <span aria-hidden="true">&raquo;</span>,
    ariaLabel: 'Next',
    locked: page === pageCount,
    page: page + 1,
    pageQueryParam,
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

const PaginationLink: FC<Link> = ({ Display, ariaLabel, locked, active, page, pageQueryParam }) => {
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
  const onClick: models.GoToEvent = {
    type: 'go-to',
    query: { [pageQueryParam !== undefined ? pageQueryParam : 'page']: page },
  }
  return (
    <li className="page-item">
      <components.LinkRender onClick={onClick} className={className} locked={locked || active} ariaLabel={ariaLabel}>
        <Display />
      </components.LinkRender>
    </li>
  )
}
