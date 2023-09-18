import {FC} from 'react'

export const DefaultErrorDisplay: FC<{ error: string }> = ({ error }) => (
  <div className="alert alert-danger" role="alert">
    <h2>Request Error:</h2>
    {error}
  </div>
)
