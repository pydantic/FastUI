import { FC, MouseEventHandler, ReactNode } from 'react'

import { ClassName, useClassName } from '../hooks/className'
import { useFireEvent, AnyEvent } from '../hooks/events'

import { FastProps, AnyCompList } from './index'

export interface LinkProps {
  type: 'Link'
  components: FastProps[]
  mode?: 'navbar' | 'tabs' | 'vertical'
  active?: boolean | string
  onClick?: AnyEvent
  className?: ClassName
}

export const LinkComp: FC<LinkProps> = (props) => (
  <LinkRender className={useClassName(props)} onClick={props.onClick}>
    <AnyCompList propsList={props.components} />
  </LinkRender>
)

interface LinkRenderProps {
  children: ReactNode
  mode?: 'navbar' | 'tabs' | 'vertical'
  active?: boolean | string
  onClick?: AnyEvent
  className?: string
}

export const LinkRender: FC<LinkRenderProps> = (props) => {
  const { className, children, onClick } = props

  const { fireEvent } = useFireEvent()

  let href = '#'
  if (onClick && onClick.type === 'go-to') {
    href = onClick.url
  }

  const clickHandler: MouseEventHandler<HTMLAnchorElement> = (e) => {
    e.preventDefault()
    fireEvent(onClick)
  }

  return (
    <a href={href} className={className} onClick={clickHandler}>
      {children}
    </a>
  )
}
