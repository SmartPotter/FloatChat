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
import { format } from 'date-fns'

interface TimeSeriesPoint {
  time: string
  temperature?: number
  salinity?: number
  depth?: number
}

interface TimeSeriesChartProps {
  data: TimeSeriesPoint[]
  loading?: boolean
  height?: number
}

export function TimeSeriesChart({ 
  data, 
  loading = false, 
  height = 400 
}: TimeSeriesChartProps) {
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
          <p>No time series data available</p>
          <p className="text-sm mt-1">Select a location on the map to view data</p>
        </div>
      </div>
    )
  }

  // Transform data for recharts
  const chartData = data.map(point => ({
    ...point,
    time: format(new Date(point.time), 'yyyy-MM-dd'),
    temperature: point.temperature || null,
    salinity: point.salinity || null,
  }))

  // Custom tooltip
  const CustomTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-white p-3 border border-gray-200 rounded-lg shadow-lg">
          <p className="font-medium text-gray-900 mb-2">{label}</p>
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

  return (
    <ResponsiveContainer width="100%" height={height}>
      <LineChart data={chartData} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
        <XAxis
          dataKey="time"
          tick={{ fontSize: 12 }}
          stroke="#666"
        />
        <YAxis
          yAxisId="temp"
          orientation="left"
          tick={{ fontSize: 12 }}
          stroke="#666"
          label={{ value: 'Temperature (°C)', angle: -90, position: 'insideLeft' }}
        />
        <YAxis
          yAxisId="sal"
          orientation="right"
          tick={{ fontSize: 12 }}
          stroke="#666"
          label={{ value: 'Salinity (PSU)', angle: 90, position: 'insideRight' }}
        />
        <Tooltip content={<CustomTooltip />} />
        <Legend />
        
        <Line
          yAxisId="temp"
          type="monotone"
          dataKey="temperature"
          stroke="#3b82f6"
          strokeWidth={2}
          dot={{ fill: '#3b82f6', strokeWidth: 2, r: 3 }}
          activeDot={{ r: 5 }}
          name="Temperature"
          connectNulls={false}
        />
        
        <Line
          yAxisId="sal"
          type="monotone"
          dataKey="salinity"
          stroke="#14b8a6"
          strokeWidth={2}
          dot={{ fill: '#14b8a6', strokeWidth: 2, r: 3 }}
          activeDot={{ r: 5 }}
          name="Salinity"
          connectNulls={false}
        />
      </LineChart>
    </ResponsiveContainer>
  )
}