import {FC, useContext, useState} from 'react'
import {ClassName, ClassNameGenerator} from './ClassName'
import {ErrorContext} from './errorContext'


interface Text {
  type: 'Text'
  text: string
}

const TextRender: FC<Text> = ({text}) => (
  <>{text}</>
)

// Input types where the value is text
interface FormField {
  type: 'FormField'
  className?: ClassName
  labelClassName?: ClassName
  inputClassName?: ClassName
  label: string
  initialValue?: string
  placeholder?: string
  id?: string
  name?: string
  htmlType?: 'text' | 'password' | 'email' | 'url'
}

export const FormFieldRender: FC<FormField> = (props) => {
  const [value, setValue] = useState(props.initialValue ?? '')
  const {type} = props
  return (
    <div className={ClassNameGenerator(props.className, type)}>
      <label className={ClassNameGenerator(props.labelClassName, type, 'label')} htmlFor={props.name}>{props.label}</label>
      <input
        className={ClassNameGenerator(props.inputClassName, type, 'input')}
        type={props.htmlType ?? 'text'}
        value={value}
        onChange={e => setValue(e.target.value)}
        placeholder={props.placeholder}
        id={props.id}
        name={props.name}
      />
    </div>
  )
}

interface Div {
  type: 'Div'
  children: AnyComp[]
  className?: ClassName
}

interface Container {
  type: 'Container'
  children: AnyComp[]
  className?: ClassName
}

interface Row {
  type: 'Row'
  children: AnyComp[]
  className?: ClassName
}

interface Col {
  type: 'Col'
  children: AnyComp[]
  className?: ClassName
}


export type AnyComp = Text | Div | Container | Row | Col | FormField
export type CompTypes = 'Text' | 'FormField' | 'Div' | 'Container' | 'Row' | 'Col'

interface AnyDiv {
  type: 'Div' | 'Container' | 'Row' | 'Col'
  children: AnyComp[]
  className?: ClassName
}

const DivRender: FC<AnyDiv> = ({type, children, className}) => (
  <div className={ClassNameGenerator(className, type)}>
    {children.map((child, i) => <AnyCompRender key={i} {...child} />)}
  </div>
)

export const AnyCompRender: FC<AnyComp> = (props) => {
  const {setError} = useContext(ErrorContext)
  const {type} = props
  try {
    switch (type) {
      case 'Text':
        return TextRender(props)
      case 'Div':
      case 'Container':
      case 'Row':
      case 'Col':
        return DivRender(props)
      case 'FormField':
        return FormFieldRender(props)
      default:
        setError({title: 'Render Error', description: `Unknown component type: ${type}`})
    }
  } catch (e) {
    const description = (e as any).message
    setError({title: 'Render Error', description})
  }
}
