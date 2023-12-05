import { ClassName, useClassName } from '../hooks/className'
import { AnyEvent } from '../events'

import { LinkProps, LinkComp, LinkRender } from './link'

export interface NavbarProps {
  type: 'Navbar'
  title?: string
  titleEvent?: AnyEvent
  links: LinkProps[]
  className?: ClassName
}

export const NavbarComp = (props: NavbarProps) => {
  const links = props.links.map((link) => {
    link.mode = link.mode || 'navbar'
    return link
  })
  return (
    <nav className={useClassName(props)}>
      <div className={useClassName(props, { el: 'contents' })}>
        <NavbarTitle {...props} />
        {links.map((link, i) => (
          <LinkComp key={i} {...link} />
        ))}
      </div>
    </nav>
  )
}

const NavbarTitle = (props: NavbarProps) => {
  const { title, titleEvent } = props
  const className = useClassName(props, { el: 'title' })
  if (title) {
    if (titleEvent) {
      return (
        <LinkRender onClick={titleEvent} className={className}>
          {title}
        </LinkRender>
      )
    } else {
      return <span className={className}>{title}</span>
    }
  }
}
