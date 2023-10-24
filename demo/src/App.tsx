import {FastUI, ClassNameFunction} from './FastUI'

export default function App() {
  return (
    <div className="app">
      <FastUI rootUrl="/api" defaultClassName={bootstrapClassName}/>
    </div>
  )
}

const bootstrapClassName: ClassNameFunction = (type) => {
  switch (type) {
    case 'Container':
      return 'container'
    case 'Row':
      return 'row'
    case 'Col':
      return 'col'
  }
}
