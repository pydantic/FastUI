import { FC } from 'react'
import { components, useClassName } from 'fastui'

export const Footer: FC<components.FooterProps> = (props) => {
  const links = props.links.map((link) => {
    link.mode = link.mode || 'footer'
    return link
  })
  const extraSeparatorProp = useClassName(props, { el: 'extra-separator' })
  const extraProp = useClassName(props, { el: 'extra' })
  return (
    <div className={useClassName(props, { el: 'contents' })}>
      <footer className={useClassName(props)}>
        <ul className={useClassName(props, { el: 'link-list' })}>
          {links.map((link, i) => (
            <li className="nav-item">
              <components.LinkComp key={i} {...link} />
            </li>
          ))}
        </ul>
        {props.extraText && props.links.length > 0 && <div className={extraSeparatorProp} />}
        {props.extraText && (
          <div className={extraProp}>
            <components.TextComp {...props.extraText} />
          </div>
        )}
      </footer>
    </div>
  )
}
