import { FC } from 'react'

import { ClassName, useClassName } from '../hooks/className'

import { LinkProps } from './link'
import { LinkListComp } from './LinkList'

export interface PaginationProps {
  type: 'Pagination'
  /** @TJS-type integer */
  page: number
  /** @TJS-type integer */
  pageSize: number
  /** @TJS-type integer */
  total: number
  /** @TJS-type integer */
  pageCount: number
  className?: ClassName
}

export const PaginationComp: FC<PaginationProps> = (props) => {
  const { page, pageCount } = props
  const className = useClassName(props)

  if (pageCount === 1) return null

  const links: LinkProps[] = [
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
