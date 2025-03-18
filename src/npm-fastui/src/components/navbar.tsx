import type { Navbar } from '../models'

import { useClassName } from '../hooks/className'

import { LinkComp, LinkRender } from './link'

export const NavbarComp = (props: Navbar) => {
  const startLinks = props.startLinks.map((link) => {
    link.mode = link.mode || 'navbar'
    return link
  })
  const endLinks = props.endLinks.map((link) => {
    link.mode = link.mode || 'navbar'
    return link
  })
  return (
    <nav className={useClassName(props)}>
      <div className={useClassName(props, { el: 'contents' })}>
        <NavbarTitle {...props} />
        {startLinks.map((link, i) =>
          link.type === 'LinkListDropdown' ? (
            <div key={i} className="alert-message">
              {'`Note: dropdowns for Navbars are not implemented by pure FastUI.`'}
            </div>
          ) : (
            <LinkComp key={i} {...link} />
          ),
        )}
        {endLinks.map((link, i) =>
          link.type === 'LinkListDropdown' ? (
            <div key={i} className="alert-message">
              {'`Note: dropdowns for Navbars are not implemented by pure FastUI.`'}
            </div>
          ) : (
            <LinkComp key={i} {...link} />
          ),
        )}
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
