import {FC, useState} from 'react'
import {ClassName, ClassNameGenerator} from '../ClassName'

export interface FormField {
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
