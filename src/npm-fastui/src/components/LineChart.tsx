import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'

import type { RechartsLineChart as FastUILineChart } from '../models'

export const LineChartComp = (props: FastUILineChart) => {
  const { width, height, data, xKey, yKeys, yKeysNames, colors, tooltip } = props

  return (
    <ResponsiveContainer width={width} height={height}>
      <LineChart
        data={data}
        margin={{
          top: 5,
          right: 20,
          left: 20,
          bottom: 5,
        }}
      >
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey={xKey} />
        <YAxis />
        {tooltip && <Tooltip />}
        <Legend />
        {yKeys.map((yKey, i) => (
          <Line
            key={i}
            type="monotone"
            dataKey={yKey}
            name={yKeysNames && yKeysNames[i] ? yKeysNames[i] : yKey}
            stroke={colors[i % colors.length]}
          />
        ))}
      </LineChart>
    </ResponsiveContainer>
  )
}
