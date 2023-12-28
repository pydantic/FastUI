import type { Navbar } from '../models'

import { useClassName } from '../hooks/className'

import { LinkComp, LinkRender } from './link'

export const NavbarComp = (props: Navbar) => {
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

const NavbarTitle = (props: Navbar) => {
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
