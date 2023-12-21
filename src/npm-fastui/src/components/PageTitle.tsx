import { FC, useEffect } from 'react'

import type { PageTitle } from '../models'

export const PageTitleComp: FC<PageTitle> = (props) => {
  const { text } = props

  useEffect(() => {
    document.title = text
  }, [text])

  return <></>
}
