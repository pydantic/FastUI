import { ClassName, useClassName } from '../hooks/className'

import { LinkProps, LinkComp } from './link'
import { TextComp, TextProps } from './text'

export interface FooterProps {
  type: 'Footer'
  extraText?: TextProps
  links: LinkProps[]
  className?: ClassName
}

export const FooterComp = (props: FooterProps) => {
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
      {props.extraText && (
        <div className={extraTextClassName}>
          <TextComp {...props.extraText} />
        </div>
      )}
    </footer>
  )
}
