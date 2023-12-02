import {FC} from 'react'

import {ClassName, useClassName} from '../hooks/className'
import {useFireEvent, AnyEvent} from '../events'

export interface ImageProps {
    type: 'Image'
    src: string
    alt?: string
    width?: number | string
    height?: number | string
    onClick?: AnyEvent
    className?: ClassName
}

export const ImageComp: FC<ImageProps> = (props) => {
    const {src, alt, width, height, onClick} = props

    const {fireEvent} = useFireEvent()

    return (
        <img
            className={useClassName(props)}
            src={src}
            alt={alt}
            width={width}
            height={height}
            onClick={() => fireEvent(onClick)}
        />
    )
}
