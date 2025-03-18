import { FC, Fragment } from 'react'
import { components, useClassName, models } from 'fastui'
import BootstrapNavbar from 'react-bootstrap/Navbar'
import NavDropdown from 'react-bootstrap/NavDropdown'

export const Navbar: FC<models.Navbar> = (props) => {
  const startLinks = props.startLinks.map((link) => {
    link.mode = link.mode || 'navbar'
    return link
  })
  const endLinks = props.endLinks.map((link) => {
    link.mode = link.mode || 'navbar'
    return link
  })
  return (
    <BootstrapNavbar expand="lg" className={useClassName(props)}>
      <div className={useClassName(props, { el: 'contents' })}>
        <NavbarTitle {...props} />
        <BootstrapNavbar.Toggle aria-controls="navbar-collapse" />
        <BootstrapNavbar.Collapse id="navbar-collapse">
          <ul className="navbar-nav me-auto">
            {startLinks.map((item, i) => (
              <li key={i} className="nav-item">
                <NavBarItem {...item} />
              </li>
            ))}
          </ul>
          <ul className="navbar-nav ms-auto">
            {endLinks.map((item, i) => (
              <li key={i} className="nav-item">
                <NavBarItem {...item} />
              </li>
            ))}
          </ul>
        </BootstrapNavbar.Collapse>
      </div>
    </BootstrapNavbar>
  )
}

const NavBarItem = (props: models.Link | models.LinkListDropdown) => {
  if (props.type === 'LinkListDropdown') {
    return (
      <NavDropdown title={props.name}>
        {props.links.map((link, j) =>
          Array.isArray(link) ? (
            link.map((innerLink, jj) => (
              <Fragment key={`${j}-${jj}`}>
                <components.LinkComp {...innerLink} className="dropdown-item" />
                {j !== props.links.length - 1 && <NavDropdown.Divider />}
              </Fragment>
            ))
          ) : (
            <Fragment key={`${j}`}>
              <components.LinkComp {...link} className="dropdown-item" />
              {j !== props.links.length - 1 && <NavDropdown.Divider />}
            </Fragment>
          ),
        )}
      </NavDropdown>
    )
  } else {
    return <components.LinkComp {...props} />
  }
}

const NavbarTitle = (props: models.Navbar) => {
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
