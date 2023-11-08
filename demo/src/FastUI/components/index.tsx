import { useContext, FC } from 'react'
import { ErrorContext } from '../hooks/error'
import { CustomRenderContext } from '../hooks/customRender'
import { DivComp, AllDivProps } from './div'
import { TextProps, TextComp } from './text'
import { FormFieldComp, FormFieldProps } from './FormField'

export type FastProps = TextProps | AllDivProps | FormFieldProps

export const AnyComp: FC<FastProps> = (props) => {
  const { setError } = useContext(ErrorContext)
  const customRender = useContext(CustomRenderContext)
  const { type } = props

  if (customRender) {
    try {
      const CustomRenderComp = customRender(props)
      if (CustomRenderComp) {
        return <CustomRenderComp />
      }
    } catch (e) {
      const description = (e as any).message
      setError({title: 'Custom Render Error', description})
    }
  }

  try {
    switch (type) {
      case 'Text':
        return <TextComp {...props} />
      case 'Div':
      case 'Container':
      case 'Row':
      case 'Col':
        return DivComp(props)
      case 'FormField':
        return FormFieldComp(props)
      default:
        setError({ title: 'Render Error', description: `Unknown component type: ${type}` })
        return <></>
    }
  } catch (e) {
    const description = (e as any).message
    setError({ title: 'Render Error', description })
    return <></>
  }
}
