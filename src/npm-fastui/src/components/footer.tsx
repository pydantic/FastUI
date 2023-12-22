import type { Footer } from '../models'

import { useClassName } from '../hooks/className'

import { LinkComp } from './link'

export const FooterComp = (props: Footer) => {
  const links = props.links.map((link) => {
    link.mode = link.mode || 'footer'
    return link
  })
  const extraTextClassName = useClassName(props, { el: 'extra' })
  return (
    <footer className={useClassName(props)}>
      {links.map((link, i) => (
        <LinkComp key={i} {...link} />
      ))}
      {props.extraText && <div className={extraTextClassName}>{props.extraText}</div>}
    </footer>
  )
}
