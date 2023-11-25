import { FC, useState } from 'react'
import AsyncSelect from 'react-select/async'
import Select, { StylesConfig } from 'react-select'

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
  | FormFieldFileProps
  | FormFieldSelectProps
  | FormFieldSelectSearchProps

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

interface FormFieldFileProps extends BaseFormFieldProps {
  type: 'FormFieldFile'
  multiple?: boolean
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
        multiple={multiple ?? false}
        accept={accept}
      />
      <ErrorDescription {...props} />
    </div>
  )
}

interface SelectOption {
  value: string
  label: string
}

interface SelectGroup {
  label: string
  options: SelectOption[]
}

type SelectOptions = SelectOption[] | SelectGroup[]

// cheat slightly and match bootstrap 😱
// TODO make this configurable as an argument to `FastUI`
const styles: StylesConfig = {
  control: (base) => ({ ...base, borderRadius: '0.375rem', border: '1px solid #dee2e6' }),
}

interface FormFieldSelectProps extends BaseFormFieldProps {
  type: 'FormFieldSelect'
  options: SelectOptions
  initial?: string
  multiple?: boolean
  vanilla?: boolean
}

export const FormFieldSelectComp: FC<FormFieldSelectProps> = (props) => {
  const { name, required, locked, options, multiple, initial, vanilla } = props

  const className = useClassName(props)
  const classNameSelect = useClassName(props, { el: 'select' })
  const classNameSelectReact = useClassName(props, { el: 'select-react' })
  if (vanilla) {
    return (
      <div className={className}>
        <Label {...props} />
        <select
          id={inputId(props)}
          className={classNameSelect}
          defaultValue={initial}
          multiple={multiple}
          name={name}
          required={required}
          disabled={locked}
          aria-describedby={descId(props)}
        >
          {multiple ? null : <option></option>}
          {options.map((option, i) => (
            <SelectOptionComp key={i} option={option} />
          ))}
        </select>
        <ErrorDescription {...props} />
      </div>
    )
  } else {
    return (
      <div className={className}>
        <Label {...props} />
        <Select
          id={inputId(props)}
          className={classNameSelectReact}
          isMulti={multiple ?? false}
          isClearable
          defaultValue={findDefault(options, initial)}
          name={name}
          required={required}
          isDisabled={locked}
          options={options}
          aria-describedby={descId(props)}
          styles={styles}
        />
        <ErrorDescription {...props} />
      </div>
    )
  }
}

const SelectOptionComp: FC<{ option: SelectOption | SelectGroup }> = ({ option }) => {
  if ('options' in option) {
    return (
      <optgroup label={option.label}>
        {option.options.map((o) => (
          <SelectOptionComp key={o.value} option={o} />
        ))}
      </optgroup>
    )
  } else {
    return <option value={option.value}>{option.label}</option>
  }
}

function findDefault(options: SelectOptions, value?: string): SelectOption | undefined {
  for (const option of options) {
    if ('options' in option) {
      const found = findDefault(option.options, value)
      if (found) {
        return found
      }
    } else if (option.value === value) {
      return option
    }
  }
}

interface FormFieldSelectSearchProps extends BaseFormFieldProps {
  type: 'FormFieldSelectSearch'
  searchUrl: string
  debounce?: number
  initial?: SelectOption
  multiple?: boolean
}

export const FormFieldSelectSearchComp: FC<FormFieldSelectSearchProps> = (props) => {
  const { name, required, locked, searchUrl, initial, multiple } = props
  const [isLoading, setIsLoading] = useState(false)
  const request = useRequest()

  const loadOptions = debounce((inputValue: string, callback: (options: SelectOptions) => void) => {
    setIsLoading(true)
    request({
      url: searchUrl,
      query: { q: inputValue },
    })
      .then(([, response]) => {
        const { options } = response as { options: SelectOptions }
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
        className={useClassName(props, { el: 'select-react' })}
        isMulti={multiple ?? false}
        cacheOptions
        isClearable
        defaultOptions
        loadOptions={loadOptions}
        defaultValue={initial}
        noOptionsMessage={({ inputValue }) => (inputValue ? 'No results' : 'Type to search')}
        name={name}
        required={required}
        isDisabled={locked}
        isLoading={isLoading}
        aria-describedby={descId(props)}
        styles={styles}
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
