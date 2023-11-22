import { ClassName, useClassName } from '../hooks/className'

import { LinkProps, LinkComp } from './link'

export interface LinkListProps {
  type: 'LinkList'
  links: LinkProps[]
  mode?: 'tabs' | 'vertical'
  className?: ClassName
}

export const LinkListComp = (props: LinkListProps) => (
  <div className={useClassName(props)}>
    {props.links.map((link, i) => (
      <LinkComp key={i} {...link} />
    ))}
  </div>
)
