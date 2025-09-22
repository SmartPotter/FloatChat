'use client'

import { ResponsiveLine } from '@nivo/line'
import type { VerticalProfilePoint } from '../../lib/api-client'

interface VerticalProfileChartProps {
  data: VerticalProfilePoint[]
  loading?: boolean
  height?: number
}

export default function VerticalProfileChart({
  data,
  loading = false,
  height = 400,
}: VerticalProfileChartProps) {
  if (loading) {
    return (
      <div
        className="w-full h-full bg-gray-100 animate-pulse rounded-lg flex items-center justify-center"
        style={{ height }}
      >
        Loading...
      </div>
    )
  }

  // Transform VerticalProfilePoint[] into Nivo line series
  const temperatureSeries = {
    id: 'Temperature',
    data: data
      .filter(p => p.temperature !== undefined && p.depth !== undefined)
      .map(p => ({ x: p.temperature!, y: p.depth })),
  }

  const salinitySeries = {
    id: 'Salinity',
    data: data
      .filter(p => p.salinity !== undefined && p.depth !== undefined)
      .map(p => ({ x: p.salinity!, y: p.depth })),
  }

  const series = [temperatureSeries, salinitySeries]

  return (
    <div style={{ height }}>
      <ResponsiveLine
        data={series}
        margin={{ top: 20, right: 50, bottom: 50, left: 60 }}
        xScale={{ type: 'linear' }}
        yScale={{ type: 'linear', min: 'auto', max: 'auto' }}
        axisBottom={{
          legend: 'Value',
          legendPosition: 'middle',
          legendOffset: 36,
        }}
        axisLeft={{
          legend: 'Depth (m)',
          legendPosition: 'middle',
          legendOffset: -50,
        }}
        colors={{ scheme: 'set2' }}
        pointSize={6}
        pointColor={{ from: 'color' }}
        pointBorderWidth={1}
        pointBorderColor={{ from: 'serieColor' }}
        enableSlices="x"
        useMesh={true}
      />
    </div>
  )
}
