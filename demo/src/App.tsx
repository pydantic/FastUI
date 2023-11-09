import { FastUI, ClassNameGenerator, CustomRender } from './FastUI'

export default function App() {
  return (
    <div className="app">
      <FastUI rootUrl="/api" classNameGenerator={bootstrapClassName} customRender={customRender} />
    </div>
  )
}

const customRender: CustomRender = () => {
  // const { type } = props
  // if (type == 'Modal') {
  //   return () => <span style={{ color: 'blue' }}>modal</span>
  // }
  return null
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
