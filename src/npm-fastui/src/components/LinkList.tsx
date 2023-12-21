import type { LinkList } from '../models'

import { useClassName } from '../hooks/className'

import { LinkComp } from './link'

export const LinkListComp = (props: LinkList) => {
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
