import { FC } from 'react'

import type { Pagination, Link } from '../models'

import { useClassName } from '../hooks/className'

import { LinkListComp } from './LinkList'

export const PaginationComp: FC<Pagination> = (props) => {
  const { page, pageCount } = props
  const className = useClassName(props)

  if (pageCount === 1) return null

  const links: Link[] = [
    {
      type: 'Link',
      components: [{ type: 'Text', text: 'Previous' }],
      locked: page !== 1,
      onClick: { type: 'go-to', query: { page: page - 1 } },
    },
    {
      type: 'Link',
      components: [{ type: 'Text', text: 'Next' }],
      locked: page !== pageCount,
      onClick: { type: 'go-to', query: { page: page + 1 } },
    },
  ]

  return (
    <div className={className}>
      <LinkListComp type="LinkList" links={links} mode="pagination" />
    </div>
  )
}
