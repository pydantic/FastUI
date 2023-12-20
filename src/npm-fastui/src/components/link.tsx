import { FC, MouseEventHandler, ReactNode, useContext } from 'react'

import type { Link, AnyEvent } from '../models'

import { useClassName } from '../hooks/className'
import { LocationContext } from '../hooks/locationContext'
import { useFireEvent } from '../events'

import { AnyCompList } from './index'

export const LinkComp: FC<Link> = (props) => (
  <LinkRender className={useClassName(props)} onClick={props.onClick} locked={props.locked}>
    <AnyCompList propsList={props.components} />
  </LinkRender>
)

interface LinkRenderProps {
  children: ReactNode
  locked?: boolean
  onClick?: AnyEvent
  className?: string
  ariaLabel?: string
}

export const LinkRender: FC<LinkRenderProps> = (props) => {
  const { className, ariaLabel, children, onClick, locked } = props

  const { fireEvent } = useFireEvent()
  const { computeQuery } = useContext(LocationContext)

  let href = locked ? undefined : '#'
  if (!locked && onClick && onClick.type === 'go-to') {
    if (onClick.url) {
      href = onClick.url
    } else if (onClick.query) {
      href = computeQuery(onClick.query)
    }
  }

  const clickHandler: MouseEventHandler<HTMLAnchorElement> = (e) => {
    e.preventDefault()
    if (!locked) {
      fireEvent(onClick)
    }
  }

  return (
    <a href={href} className={className} onClick={clickHandler} aria-label={ariaLabel} aria-disabled={locked}>
      {children}
    </a>
  )
}
