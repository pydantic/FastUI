import { FC } from 'react'
import { components, useClassName } from 'fastui'

export const Footer: FC<components.FooterProps> = (props) => {
  const links = props.links.map((link) => {
    link.mode = link.mode || 'footer'
    return link
  })
  const extraProp = useClassName(props, { el: 'extra' })
  return (
    <footer className={useClassName(props, { el: 'contents' })}>
      <ul className={useClassName(props, { el: 'link-list' })}>
        {links.map((link, i) => (
          <li className="nav-item">
            <components.LinkComp key={i} {...link} />
          </li>
        ))}
      </ul>
      {props.extraText && <div className={extraProp}>{props.extraText}</div>}
    </footer>
  )
}
