import { FC } from 'react'

import type { Error } from '../models'

import { useClassName } from '../hooks/className'

export const ErrorComp: FC<Error> = (props) => {
  const { title, description, statusCode, children } = props
  return (
    <>
      <div className={useClassName(props)} role="alert">
        {statusCode === 502 ? (
          <>Backend server down.</>
        ) : (
          <>
            <h4>{title}</h4>
            {description}
          </>
        )}
      </div>
      {children}
    </>
  )
}
