import { FC, useEffect } from 'react'

export interface PageTitleProps {
  type: 'PageTitle'
  text: string
}

export const PageTitleComp: FC<PageTitleProps> = (props) => {
  const { text } = props

  useEffect(() => {
    document.title = text
  }, [text])

  return <></>
}
