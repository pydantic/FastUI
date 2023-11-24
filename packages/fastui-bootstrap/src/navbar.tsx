import { FC } from 'react'
import { components, useClassName } from 'fastui'
import BootstrapNavbar from 'react-bootstrap/Navbar'

export const Navbar: FC<components.NavbarProps> = (props) => {
  const links = props.links.map((link) => {
    link.mode = link.mode || 'navbar'
    return link
  })
  return (
    <BootstrapNavbar expand="lg" className="bg-body-tertiary">
      <div className={useClassName(props, { el: 'contents' })}>
        <NavbarTitle {...props} />
        <BootstrapNavbar.Toggle aria-controls="navbar-collapse" />
        <BootstrapNavbar.Collapse id="navbar-collapse">
          <ul className="navbar-nav me-auto">
            {links.map((link, i) => (
              <li className="nav-item">
                <components.LinkComp key={i} {...link} />
              </li>
            ))}
          </ul>
        </BootstrapNavbar.Collapse>
      </div>
    </BootstrapNavbar>
  )
}

const NavbarTitle = (props: components.NavbarProps) => {
  const { title, titleEvent } = props
  const className = useClassName(props, { el: 'title' })
  if (title) {
    if (titleEvent) {
      return (
        <components.LinkRender onClick={titleEvent} className={className}>
          {title}
        </components.LinkRender>
      )
    } else {
      return <span className={className}>{title}</span>
    }
  }
}
