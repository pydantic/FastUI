import { FC } from 'react'

import type { Heading } from '../models'

import { useClassName } from '../hooks/className'
import { slugify } from '../tools'

export const HeadingComp: FC<Heading> = (props) => {
  const { level, text, htmlId } = props
  const HeadingComponent = getComponent(level)
  return <HeadingComponent text={text} id={htmlId || slugify(text)} className={useClassName(props)} />
}

function getComponent(level: 1 | 2 | 3 | 4 | 5 | 6): FC<{ text: string; id?: string; className?: string }> {
  switch (level) {
    case 1:
      return ({ text, ...rest }) => <h1 {...rest}>{text}</h1>
    case 2:
      return ({ text, ...rest }) => <h2 {...rest}>{text}</h2>
    case 3:
      return ({ text, ...rest }) => <h3 {...rest}>{text}</h3>
    case 4:
      return ({ text, ...rest }) => <h4 {...rest}>{text}</h4>
    case 5:
      return ({ text, ...rest }) => <h5 {...rest}>{text}</h5>
    case 6:
      return ({ text, ...rest }) => <h6 {...rest}>{text}</h6>
  }
}
