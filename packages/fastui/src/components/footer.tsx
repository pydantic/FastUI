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
  const linkProp = useClassName(props, { el: 'link' })
  const extraSeparatorProp = useClassName(props, { el: 'extra-separator' })
  const extraProp = useClassName(props, { el: 'extra' })
  return (
    <div className={useClassName(props, { el: 'contents' })}>
      <footer className={useClassName(props)}>
        <ul className={useClassName(props, { el: 'link-list' })}>
          {links.map((link, i) => (
            <li className={linkProp}>
              <LinkComp key={i} {...link} />
            </li>
          ))}
        </ul>
        {props.extraText && props.links.length > 0 && <div className={extraSeparatorProp} />}
        {props.extraText && (
          <>
            <div className={extraProp}>
              <TextComp {...props.extraText} />
            </div>
          </>
        )}
      </footer>
    </div>
  )
}
