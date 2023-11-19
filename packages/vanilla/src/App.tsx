import { FastUI } from 'fastui'
import * as bootstrap from 'fastui-bootstrap'

export default function App() {
  return (
    <div className="app">
      <FastUI rootUrl="/api" classNameGenerator={bootstrap.classNameGenerator} customRender={bootstrap.customRender} />
    </div>
  )
}
