import { FastUI, renderClassName } from 'fastui'
import * as bootstrap from 'fastui-bootstrap'
import { FC, ReactNode } from 'react'

export default function App() {
  return (
    <div className="top-offset">
      <FastUI
        rootUrl="/api"
        classNameGenerator={bootstrap.classNameGenerator}
        customRender={bootstrap.customRender}
        NotFound={NotFound}
        Spinner={Spinner}
        Transition={Transition}
      />
    </div>
  )
}

const NotFound = ({ url }: { url: string }) => (
  <div className="container mt-5 text-center">
    <h1>Page not found</h1>
    <p>
      No page found at <code>{url}</code>.
    </p>
  </div>
)

const Spinner = () => (
  <div className="container d-flex justify-content-center my-3" role="status">
    <div className="spinner" />
  </div>
)

const Transition: FC<{ children: ReactNode; transitioning: boolean }> = ({ children, transitioning }) => (
  <div>
    <div className={renderClassName({ 'transition-overlay': true, transitioning })} />
    {children}
  </div>
)
