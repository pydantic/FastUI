import { FastUI } from 'fastui'
import * as bootstrap from 'fastui-bootstrap'

export default function App() {
  return (
    <div className="top-offset">
      <FastUI
        rootUrl="/api"
        classNameGenerator={bootstrap.classNameGenerator}
        customRender={bootstrap.customRender}
        NotFound={NotFound}
        Spinner={Spinner}
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
