import { CustomRender, FastUI, renderClassName } from 'fastui'
import * as bootstrap from 'fastui-bootstrap'
import { FC, ReactNode } from 'react'

export default function App() {
  return (
    <FastUI
      APIRootUrl={getMetaContent('fastui:APIRootUrl') || '/api'}
      APIPathMode={getMetaContent('fastui:APIPathMode') as undefined | 'append' | 'query'}
      APIPathStrip={getMetaContent('fastui:APIPathStrip')}
      classNameGenerator={bootstrap.classNameGenerator}
      customRender={customRender}
      NotFound={NotFound}
      Transition={Transition}
    />
  )
}

function getMetaContent(name: string): string | undefined {
  return document.querySelector(`meta[name="${name}"]`)?.getAttribute('content') || undefined
}

const NotFound = ({ url }: { url: string }) => (
  <div className="container mt-5 text-center">
    <h1>Page not found</h1>
    <p>
      No page found at <code>{url}</code>.
    </p>
  </div>
)

const Transition: FC<{ children: ReactNode; transitioning: boolean }> = ({ children, transitioning }) => (
  <>
    <div className={renderClassName({ 'transition-overlay': true, transitioning })} />
    {children}
  </>
)

const customRender: CustomRender = (props) => {
  const { type } = props
  if (type === 'Custom' && props.library === undefined && props.subType === 'cowsay') {
    console.assert(typeof props.data === 'string', 'cowsay data must be a string')
    const text = props.data as string
    return () => <Cowsay text={text} />
  } else {
    return bootstrap.customRender(props)
  }
}

const COWSAY = ` {above}
< {text} >
 {below}
        \\   ^__^
         \\  (oo)\\_______
            (__)\\       )\\/\\
                ||----w |
                ||     ||`

const Cowsay: FC<{ text: string }> = ({ text }) => {
  const len = text.length
  const cowsay = COWSAY.replace('{text}', text)
    .replace('{above}', '_'.repeat(len + 2))
    .replace('{below}', '-'.repeat(len + 2))
  return <pre>{cowsay}</pre>
}
