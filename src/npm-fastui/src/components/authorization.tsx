import { FC, useEffect, useState } from 'react'

import { AnyEvent, useFireEvent } from '../events'
import { AUTH_TOKEN_KEY } from '../tools'
import { ClassName } from '../hooks/className'

export interface AuthorizationProps {
  type: 'Authorization'
  token?: string
  afterAuthorize?: AnyEvent
  className?: ClassName
}

export const AuthorizationComp: FC<AuthorizationProps> = ({ token, afterAuthorize }) => {
  const [after] = useState(afterAuthorize)

  const { fireEvent } = useFireEvent()

  useEffect(() => {
    if (token) {
      console.debug('Authorizing with token', token)
      sessionStorage.setItem(AUTH_TOKEN_KEY, token)
    } else {
      console.debug('Removing Authorization token')
      sessionStorage.removeItem(AUTH_TOKEN_KEY)
    }
    fireEvent(after)
  }, [token, after, fireEvent])

  return <></>
}
