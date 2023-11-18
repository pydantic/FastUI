import { FastUI, ClassNameGenerator, CustomRender } from 'fastui'

export default function App() {
  return (
    <div className="app">
      <FastUI rootUrl="/api" classNameGenerator={bootstrapClassName} customRender={customRender} />
    </div>
  )
}

const customRender: CustomRender = (props) => {
  const { type } = props
  if (type === 'DisplayPrimitive') {
    const { value } = props
    if (typeof value === 'boolean') {
      return () => <>{value ? '👍' : '👎'}</>
    }
  }
}

const bootstrapClassName: ClassNameGenerator = (props) => {
  const { type } = props
  switch (type) {
    case 'Page':
      return 'container py-4'
    case 'Row':
      return 'row'
    case 'Col':
      return 'col'
    case 'Button':
      return 'btn btn-primary'
    case 'Table':
      return 'table table-striped'
  }
}
