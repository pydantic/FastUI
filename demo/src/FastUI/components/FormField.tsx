import { FC, useState } from 'react'
import { ClassName, useClassNameGenerator } from '../hooks/className.ts'

export interface FormFieldProps {
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

export const FormFieldComp: FC<FormFieldProps> = (props) => {
  const [value, setValue] = useState(props.initialValue ?? '')
  return (
    <div className={useClassNameGenerator(props.className, props)}>
      <label className={useClassNameGenerator(props.labelClassName, props, 'label')} htmlFor={props.name}>
        {props.label}
      </label>
      <input
        className={useClassNameGenerator(props.inputClassName, props, 'input')}
        type={props.htmlType ?? 'text'}
        value={value}
        onChange={(e) => setValue(e.target.value)}
        placeholder={props.placeholder}
        id={props.id}
        name={props.name}
      />
    </div>
  )
}
