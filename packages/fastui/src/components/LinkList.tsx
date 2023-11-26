import { ClassName, useClassName } from '../hooks/className'

import { LinkProps, LinkComp } from './link'

export interface LinkListProps {
  type: 'LinkList'
  links: LinkProps[]
  mode?: 'tabs' | 'vertical'
  className?: ClassName
}

export const LinkListComp = (props: LinkListProps) => {
  const itemClassName = useClassName(props, { el: 'link-list-item' })
  return (
    <div className={useClassName(props)}>
      {props.links.map((link, i) => (
        <div key={i} className={itemClassName}>
          <LinkComp {...{ ...link, mode: props.mode }} />
        </div>
      ))}
    </div>
  )
}
