import { FastUI, ClassNameFunction, CustomRender } from './FastUI'

export default function App() {
  return (
    <div className="app">
      <FastUI rootUrl="/api" defaultClassName={bootstrapClassName} customRender={customRender} />
    </div>
  )
}

const customRender: CustomRender = () => {
  // const {type} = props
  // if (type == 'Text') {
  //   return () => <span style={{color: 'blue'}}>{props.text}</span>
  // }
  return null
}

const bootstrapClassName: ClassNameFunction = (props) => {
  const { type } = props
  switch (type) {
    case 'Container':
      return 'container'
    case 'Row':
      return 'row'
    case 'Col':
      return 'col'
  }
}
