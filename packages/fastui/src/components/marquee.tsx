import { FC } from 'react'

export interface MarqueeProps {
  type: 'Marquee'
  text: string
}

export const MarqueeComp: FC<MarqueeProps> = ({ text }) => <marquee>{text}</marquee>
