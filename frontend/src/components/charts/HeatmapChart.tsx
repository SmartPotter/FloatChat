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
  Area,
  AreaChart,
} from 'recharts'
import { format } from 'date-fns'

interface HeatContentPoint {
  time: string
  lat: number
  lon: number
  heat_content: number
}

interface HeatmapChartProps {
  data: HeatContentPoint[]
  loading?: boolean
  height?: number
}

export function HeatmapChart({ 
  data, 
  loading = false, 
  height = 400 
}: HeatmapChartProps) {
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
          <p>No heat content data available</p>
          <p className="text-sm mt-1">Select a location to view heat content trends</p>
        </div>
      </div>
    )
  }

  // Transform data for recharts
  const chartData = data.map(point => ({
    ...point,
    time: format(new Date(point.time), 'yyyy-MM'),
    heat_content: point.heat_content,
    location: `${point.lat}°N, ${point.lon}°E`
  }))

  // Group data by location for multiple series
  const locationGroups = data.reduce((acc, point) => {
    const key = `${point.lat}_${point.lon}`
    if (!acc[key]) {
      acc[key] = []
    }
    acc[key].push({
      time: format(new Date(point.time), 'yyyy-MM'),
      heat_content: point.heat_content,
      location: `${point.lon}°E`
    })
    return acc
  }, {} as Record<string, any[]>)

  // Create chart data with all locations
  const allTimes = Array.from(new Set(chartData.map(d => d.time))).sort()
  const mergedData = allTimes.map(time => {
    const point: any = { time }
    Object.entries(locationGroups).forEach(([key, points]) => {
      const timePoint = points.find(p => p.time === time)
      const location = points[0]?.location || key
      point[location] = timePoint?.heat_content || null
    })
    return point
  })

  // Colors for different locations
  const colors = ['#3b82f6', '#14b8a6', '#f59e0b', '#ef4444', '#8b5cf6']

  // Custom tooltip
  const CustomTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-white p-3 border border-gray-200 rounded-lg shadow-lg">
          <p className="font-medium text-gray-900 mb-2">{label}</p>
          {payload.map((entry: any, index: number) => (
            entry.value && (
              <p key={index} style={{ color: entry.color }} className="text-sm">
                {entry.dataKey}: {entry.value.toFixed(0)} units
              </p>
            )
          ))}
        </div>
      )
    }
    return null
  }

  const locationKeys = Object.keys(locationGroups).map((key, index) => 
    locationGroups[key][0]?.location || key
  )

  return (
    <ResponsiveContainer width="100%" height={height}>
      <AreaChart data={mergedData} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
        <XAxis
          dataKey="time"
          tick={{ fontSize: 12 }}
          stroke="#666"
        />
        <YAxis
          tick={{ fontSize: 12 }}
          stroke="#666"
          label={{ value: 'Heat Content (units)', angle: -90, position: 'insideLeft' }}
        />
        <Tooltip content={<CustomTooltip />} />
        <Legend />
        
        {locationKeys.map((location, index) => (
          <Area
            key={location}
            type="monotone"
            dataKey={location}
            stackId={index < 2 ? "1" : undefined} // Stack first two areas
            stroke={colors[index % colors.length]}
            fill={colors[index % colors.length]}
            fillOpacity={0.3}
            strokeWidth={2}
            name={location}
            connectNulls={false}
          />
        ))}
      </AreaChart>
    </ResponsiveContainer>
  )
}