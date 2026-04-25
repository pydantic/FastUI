import { FC } from 'react'
import { components, models } from 'fastui'

/**
 * Bootstrap-flavoured wrapper around the core `FormFieldRadioComp`.
 *
 * The radio button group itself is rendered by the core npm-fastui package; the
 * styling for Bootstrap is supplied via the `classNameGenerator` in this
 * package's `index.tsx`. This wrapper exists so consumers can plug a Radio in
 * via `customRender` (or import it directly) without having to reach into
 * `fastui/components`. Matches the file layout of `modal.tsx` / `navbar.tsx`.
 */
export const Radio: FC<models.FormFieldRadio> = (props) => {
  return <components.FormFieldRadioComp {...props} />
}
