import { FC } from 'react'

import { ClassName, useClassNameGenerator } from '../hooks/className'

export interface HeadingProps {
  type: 'Heading'
  level: 1 | 2 | 3 | 4 | 5 | 6
  className?: ClassName
  text: string
}

export const HeadingComp: FC<HeadingProps> = (props) => {
  const { level, text, className } = props
  const HeadingComponent = getComponent(level)
  return <HeadingComponent text={text} className={useClassNameGenerator(className, props)} />
}

function getComponent(level: 1 | 2 | 3 | 4 | 5 | 6): FC<{ text: string; className: string }> {
  switch (level) {
    case 1:
      return ({ text, className }) => <h1 className={className}>{text}</h1>
    case 2:
      return ({ text, className }) => <h2 className={className}>{text}</h2>
    case 3:
      return ({ text, className }) => <h3 className={className}>{text}</h3>
    case 4:
      return ({ text, className }) => <h4 className={className}>{text}</h4>
    case 5:
      return ({ text, className }) => <h5 className={className}>{text}</h5>
    case 6:
      return ({ text, className }) => <h6 className={className}>{text}</h6>
  }
}
