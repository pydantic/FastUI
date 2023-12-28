import { FC } from 'react'
import { components, models, useClassName } from 'fastui'

export const Footer: FC<models.Footer> = (props) => {
  const links = props.links.map((link) => {
    link.mode = link.mode || 'footer'
    return link
  })
  const extraProp = useClassName(props, { el: 'extra' })
  return (
    <footer className={useClassName(props)}>
      <ul className={useClassName(props, { el: 'link-list' })}>
        {links.map((link, i) => (
          <li key={i} className="nav-item">
            <components.LinkComp {...link} />
          </li>
        ))}
      </ul>
      {props.extraText && <div className={extraProp}>{props.extraText}</div>}
    </footer>
  )
}
