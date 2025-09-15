'use client'

import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts'

interface VerticalProfilePoint {
  depth: number
  temperature?: number
  salinity?: number
  date: string
}

interface VerticalProfileChartProps {
  data: VerticalProfilePoint[]
  loading?: boolean
  height?: number
}

export function VerticalProfileChart({ 
  data, 
  loading = false, 
  height = 400 
}: VerticalProfileChartProps) {
  if (loading) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  if (!data || data.length === 0) {
    return (
      <div className="flex items-center justify-center h-full text-gray-500">
        <div className="text-center">
          <p>No profile data available</p>
          <p className="text-sm mt-1">Select a location to view vertical profile</p>
        </div>
      </div>
    )
  }

  // Transform data for recharts - invert depth for oceanographic convention
  const chartData = data
    .sort((a, b) => a.depth - b.depth)
    .map(point => ({
      ...point,
      depth: -point.depth, // Negative for plotting (surface at top)
      temperature: point.temperature || null,
      salinity: point.salinity || null,
    }))

  // Custom tooltip
  const CustomTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-white p-3 border border-gray-200 rounded-lg shadow-lg">
          <p className="font-medium text-gray-900 mb-2">
            Depth: {Math.abs(label).toFixed(0)}m
          </p>
          {payload.map((entry: any, index: number) => (
            <p key={index} style={{ color: entry.color }} className="text-sm">
              {entry.dataKey === 'temperature' ? 'Temperature: ' : 'Salinity: '}
              {entry.value?.toFixed(2)}
              {entry.dataKey === 'temperature' ? '°C' : ' PSU'}
            </p>
          ))}
        </div>
      )
    }
    return null
  }

  // Custom Y-axis tick formatter to show positive depths
  const formatDepthTick = (value: number) => Math.abs(value).toString()

  return (
    <ResponsiveContainer width="100%" height={height}>
      <LineChart
        data={chartData}
        layout="horizontal"
        margin={{ top: 5, right: 30, left: 40, bottom: 5 }}
      >
        <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
        <XAxis
          type="number"
          domain={['dataMin - 1', 'dataMax + 1']}
          tick={{ fontSize: 12 }}
          stroke="#666"
          label={{ value: 'Temperature (°C) / Salinity (PSU)', position: 'bottom', offset: -5 }}
        />
        <YAxis
          type="number"
          dataKey="depth"
          tick={{ fontSize: 12 }}
          stroke="#666"
          tickFormatter={formatDepthTick}
          label={{ value: 'Depth (m)', angle: -90, position: 'insideLeft' }}
        />
        <Tooltip content={<CustomTooltip />} />
        <Legend />
        
        <Line
          type="monotone"
          dataKey="temperature"
          stroke="#ef4444"
          strokeWidth={2.5}
          dot={{ fill: '#ef4444', strokeWidth: 2, r: 3 }}
          activeDot={{ r: 5 }}
          name="Temperature (°C)"
          connectNulls={false}
        />
        
        <Line
          type="monotone"
          dataKey="salinity"
          stroke="#06b6d4"
          strokeWidth={2.5}
          dot={{ fill: '#06b6d4', strokeWidth: 2, r: 3 }}
          activeDot={{ r: 5 }}
          name="Salinity (PSU)"
          connectNulls={false}
        />
      </LineChart>
    </ResponsiveContainer>
  )
}