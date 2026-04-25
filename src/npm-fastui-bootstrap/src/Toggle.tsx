import { FC } from 'react'
import { components, models } from 'fastui'

/**
 * Bootstrap-flavoured wrapper around the core `FormFieldToggleComp`.
 *
 * The toggle (on/off switch) itself is rendered by the core npm-fastui package;
 * Bootstrap styling is supplied via the `classNameGenerator` in this package's
 * `index.tsx`. The wrapper exists so consumers can plug a Toggle in via
 * `customRender` (or import it directly) without having to reach into
 * `fastui/components`. Matches the file layout of `modal.tsx` / `navbar.tsx`.
 */
export const Toggle: FC<models.FormFieldToggle> = (props) => {
  return <components.FormFieldToggleComp {...props} />
}
