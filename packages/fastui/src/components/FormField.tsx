import { FC, useState } from 'react'
import AsyncSelect from 'react-select/async'
import { StylesConfig } from 'react-select'

import { ClassName, useClassName } from '../hooks/className'
import { debounce, useRequest } from '../tools'

interface BaseFormFieldProps {
  name: string
  title: string[]
  required: boolean
  locked: boolean
  error?: string
  description?: string
  className?: ClassName
}

export type FormFieldProps =
  | FormFieldInputProps
  | FormFieldCheckboxProps
  | FormFieldSelectProps
  | FormFieldSelectSearchProps
  | FormFieldFileProps

interface FormFieldInputProps extends BaseFormFieldProps {
  type: 'FormFieldInput'
  htmlType?: 'text' | 'date' | 'datetime-local' | 'time' | 'email' | 'url' | 'number' | 'password'
  initial?: string | number
  placeholder?: string
}

export const FormFieldInputComp: FC<FormFieldInputProps> = (props) => {
  const { name, placeholder, required, htmlType, locked } = props

  return (
    <div className={useClassName(props)}>
      <Label {...props} />
      <input
        type={htmlType}
        className={useClassName(props, { el: 'input' })}
        defaultValue={props.initial}
        id={inputId(props)}
        name={name}
        required={required}
        disabled={locked}
        placeholder={placeholder}
        aria-describedby={descId(props)}
      />
      <ErrorDescription {...props} />
    </div>
  )
}

interface FormFieldCheckboxProps extends BaseFormFieldProps {
  type: 'FormFieldCheckbox'
  initial?: boolean
}

export const FormFieldCheckboxComp: FC<FormFieldCheckboxProps> = (props) => {
  const { name, required, locked } = props

  return (
    <div className={useClassName(props)}>
      <Label {...props} />
      <input
        type="checkbox"
        className={useClassName(props, { el: 'input' })}
        defaultChecked={!!props.initial}
        id={inputId(props)}
        name={name}
        required={required}
        disabled={locked}
        aria-describedby={descId(props)}
      />
      <ErrorDescription {...props} />
    </div>
  )
}

interface FormFieldSelectProps extends BaseFormFieldProps {
  type: 'FormFieldSelect'
  choices: [string, string][]
  initial?: string
}

export const FormFieldSelectComp: FC<FormFieldSelectProps> = (props) => {
  const { name, required, locked, choices } = props
  const [value, setValue] = useState(props.initial ?? '')

  return (
    <div className={useClassName(props)}>
      <Label {...props} />
      <select
        id={inputId(props)}
        className={useClassName(props, { el: 'select' })}
        value={value}
        onChange={(e) => setValue(e.target.value)}
        name={name}
        required={required}
        disabled={locked}
        aria-describedby={descId(props)}
      >
        <option></option>
        {choices.map(([value, label]) => (
          <option key={value} value={value}>
            {label}
          </option>
        ))}
      </select>
      <ErrorDescription {...props} />
    </div>
  )
}

interface SearchOption {
  value: string
  label: string
}

interface SearchGroup {
  label: string
  options: SearchOption[]
}

interface FormFieldSelectSearchProps extends BaseFormFieldProps {
  type: 'FormFieldSelectSearch'
  searchUrl: string
  debounce?: number
  initial?: SearchOption
}

// cheat slightly and match bootstrap 😱
// TODO make this configurable as an argument to `FastUI`
const styles: StylesConfig = {
  control: (base) => ({ ...base, borderRadius: '0.375rem', border: '1px solid #dee2e6' }),
}

type EitherOptions = SearchOption[] | SearchGroup[]

export const FormFieldSelectSearchComp: FC<FormFieldSelectSearchProps> = (props) => {
  const { name, required, locked, searchUrl, initial } = props
  const [isLoading, setIsLoading] = useState(false)
  const request = useRequest()

  const loadOptions = debounce((inputValue: string, callback: (options: EitherOptions) => void) => {
    setIsLoading(true)
    request({
      url: searchUrl,
      query: { q: inputValue },
    })
      .then(([, response]) => {
        const { options } = response as { options: EitherOptions }
        callback(options)
        setIsLoading(false)
      })
      .catch(() => {
        setIsLoading(false)
      })
  }, props.debounce ?? 300)

  return (
    <div className={useClassName(props)}>
      <Label {...props} />
      <AsyncSelect
        id={inputId(props)}
        className={useClassName(props, { el: 'select-search' })}
        cacheOptions
        isClearable
        loadOptions={loadOptions}
        defaultValue={initial}
        name={name}
        required={required}
        isDisabled={locked}
        isLoading={isLoading}
        aria-describedby={descId(props)}
        styles={styles}
        noOptionsMessage={({ inputValue }) => (inputValue ? 'No results' : 'Type to search')}
      />
      <ErrorDescription {...props} />
    </div>
  )
}

interface FormFieldFileProps extends BaseFormFieldProps {
  type: 'FormFieldFile'
  multiple: boolean
  accept?: string
}

export const FormFieldFileComp: FC<FormFieldFileProps> = (props) => {
  const { name, required, locked, multiple, accept } = props

  return (
    <div className={useClassName(props)}>
      <Label {...props} />
      <input
        type="file"
        className={useClassName(props, { el: 'input' })}
        id={inputId(props)}
        name={name}
        required={required}
        disabled={locked}
        multiple={multiple}
        accept={accept}
      />
      <ErrorDescription {...props} />
    </div>
  )
}

const Label: FC<FormFieldProps> = (props) => {
  const { title } = props
  return (
    <label htmlFor={inputId(props)} className={useClassName(props, { el: 'label' })}>
      {title.map((t, i) => (
        <span key={i}>
          {i > 0 ? <> &rsaquo;</> : null} {t}
        </span>
      ))}
    </label>
  )
}

const inputId = (props: FormFieldProps) => `form-field-${props.name}`
const descId = (props: FormFieldProps) => (props.description ? `${inputId(props)}-desc` : undefined)

const ErrorDescription: FC<FormFieldProps> = (props) => {
  const { description, error } = props
  const descClassName = useClassName(props, { el: 'description' })
  const errorClassName = useClassName(props, { el: 'error' })
  return (
    <>
      {description ? (
        <div id={descId(props)} className={descClassName}>
          {description}
        </div>
      ) : null}
      {error ? <div className={errorClassName}>{error}</div> : null}
    </>
  )
}
