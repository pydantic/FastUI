import {FastUI, ClassNameFunction} from './FastUI'

export default function App() {
  return (
    <div className="app">
      <FastUI rootUrl="/api" defaultClassName={bootstrap}/>
    </div>
  )
}

const bootstrap: ClassNameFunction = (type) => {
  switch (type) {
    case 'Container':
      return 'container'
    case 'Row':
      return 'row'
    case 'Col':
      return 'col'
  }
}
