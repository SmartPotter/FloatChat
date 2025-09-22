// 'use client'

// import { useState, useEffect } from 'react'
// import dynamic from 'next/dynamic'
// import { Calendar, Download, Filter, MapPin } from 'lucide-react'
// import { TimeSeriesChart } from '../../components/charts/TimeSeriesChart'
// import { VerticalProfileChart } from '../../components/charts/VerticalProfileChart'
// import { HeatmapChart } from '../../components/charts/HeatmapChart'
// import { FilterPanel } from '../../components/FilterPanel'
// import { DataSummaryCard } from '../../components/DataSummaryCard'
// import { apiClient } from '../../lib/api-client'
// import type { TimeSeriesPoint, VerticalProfilePoint, HeatContentPoint } from '../../lib/api-client'

// const OceanMap = dynamic(() => import('../../components/OceanMap'), {
//   ssr: false,
//   loading: () => <div className="h-96 bg-gray-100 rounded-lg animate-pulse" />
// })

// interface DataSummary {
//   total_records: number
//   date_range: { start: string; end: string }
//   spatial_coverage: {
//     latitude: { min: number; max: number }
//     longitude: { min: number; max: number }
//   }
//   measurement_counts: Record<string, number>
// }

// export default function DashboardPage() {
//   const [dataSummary, setDataSummary] = useState<DataSummary | null>(null)
//   const [selectedLocation, setSelectedLocation] = useState<{ lat: number; lon: number } | null>(null)
//   const [timeSeriesData, setTimeSeriesData] = useState<TimeSeriesPoint[]>([])
//   const [profileData, setProfileData] = useState<VerticalProfilePoint[]>([])
//   const [heatContentData, setHeatContentData] = useState<HeatContentPoint[]>([])
//   const [loading, setLoading] = useState(true)
//   const [showFilters, setShowFilters] = useState(false)

//   useEffect(() => {
//     loadDataSummary()
//   }, [])

//   useEffect(() => {
//     if (selectedLocation) {
//       loadLocationData(selectedLocation)
//     }
//   }, [selectedLocation])

//   const loadDataSummary = async () => {
//     try {
//       const summary = await apiClient.getDataSummary()
//       setDataSummary(summary)
      
      
//       if (summary.spatial_coverage) {
//         setSelectedLocation({
//           lat: 0, // Equatorial focus based on the dat
//           lon: 60  
//         })
//       }
//     } catch (error) {
//       console.error('Failed to load data summary:', error)
//     } finally {
//       setLoading(false)
//     }
//   }

//   const loadLocationData = async (location: { lat: number; lon: number }) => {
//     setLoading(true)
//     try {
      
//       const timeSeries = await apiClient.getSurfaceTimeseries({
//         lat: location.lat,
//         lon: location.lon,
//         start: '2010-01-01',
//         end: '2013-12-31'
//       })
//       setTimeSeriesData(timeSeries)

      
//       const profile = await apiClient.getVerticalProfile({
//         lat: location.lat,
//         lon: location.lon,
//         date: '2012-06-15'
//       })
//       setProfileData(profile)

      
//       const heatContent = await apiClient.getHeatContent({
//         lat: location.lat,
//         lon: location.lon,
//         start: '2010-01-01',
//         end: '2013-12-31'
//       })
//       setHeatContentData(heatContent)

//     } catch (error) {
//       console.error('Failed to load location data:', error)
//     } finally {
//       setLoading(false)
//     }
//   }

//   const handleLocationSelect = (lat: number, lon: number) => {
//     setSelectedLocation({ lat, lon })
//   }

//   if (loading && !dataSummary) {
//     return (
//       <div className="min-h-screen bg-gray-50 flex items-center justify-center">
//         <div className="text-center">
//           <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto mb-4"></div>
//           <p className="text-gray-600">Loading dashboard...</p>
//         </div>
//       </div>
//     )
//   }

//   return (
//     <div className="min-h-screen bg-gray-50">
//       {/* Header */}
//       <header className="bg-white shadow-sm border-b">
//         <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
//           <div className="flex justify-between items-center py-6">
//             <div>
//               <h1 className="text-2xl font-bold text-gray-900">Ocean Data Dashboard</h1>
//               <p className="text-gray-600 mt-1">Interactive visualization of ARGO float data</p>
//             </div>
            
//             <div className="flex items-center space-x-4">
//               <button
//                 type="button"
//                 onClick={() => setShowFilters(!showFilters)}
//                 className="btn-secondary inline-flex items-center"
//               >
//                 <Filter className="h-4 w-4 mr-2" />
//                 Filters
//               </button>
//               <button type="button" className="btn-primary inline-flex items-center">
//                 <Download className="h-4 w-4 mr-2" />
//                 Export
//               </button>
//             </div>
//           </div>
//         </div>
//       </header>

//       <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
//         {/* Data Summary Cards */}
//         {dataSummary && (
//           <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
//             <DataSummaryCard
//               title="Total Records"
//               value={dataSummary.total_records.toLocaleString()}
//               icon={<Calendar className="h-6 w-6" />}
//               trend="+12.5%"
//             />
//             <DataSummaryCard
//               title="Date Range"
//               value={`${dataSummary.date_range.start} to ${dataSummary.date_range.end}`}
//               icon={<Calendar className="h-6 w-6" />}
//             />
//             <DataSummaryCard
//               title="Spatial Coverage"
//               value={`${dataSummary.spatial_coverage.longitude.min}°E - ${dataSummary.spatial_coverage.longitude.max}°E`}
//               icon={<MapPin className="h-6 w-6" />}
//             />
//             <DataSummaryCard
//               title="Data Types"
//               value={Object.keys(dataSummary.measurement_counts).length.toString()}
//               icon={<Filter className="h-6 w-6" />}
//             />
//           </div>
//         )}

//         {/* Filter Panel */}
//         {showFilters && (
//           <div className="mb-8">
//             <FilterPanel
//               onLocationChange={handleLocationSelect}
//               onDateRangeChange={(start, end) => console.log('Date range:', start, end)}
//             />
//           </div>
//         )}

//         {/* Main Content Grid */}
//         <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
//           {/* Map Section */}
//           <div className="card">
//             <div className="flex justify-between items-center mb-4">
//               <h2 className="text-lg font-semibold text-gray-900">Float Locations</h2>
//               {selectedLocation && (
//                 <div className="text-sm text-gray-600">
//                   Selected: {selectedLocation.lat}°N, {selectedLocation.lon}°E
//                 </div>
//               )}
//             </div>
//             <div className="h-96">
//               <OceanMap
//                 onLocationSelect={handleLocationSelect}
//                 selectedLocation={selectedLocation}
//                 floatLocations={[
//                   { lat: 0, lon: 60, id: 'float-60E' },
//                   { lat: 0, lon: 80, id: 'float-80E' },
//                   { lat: 0, lon: 100, id: 'float-100E' }
//                 ]}
//               />
//             </div>
//           </div>

//           {/* Time Series Chart */}
//           <div className="card">
//             <h2 className="text-lg font-semibold text-gray-900 mb-4">Surface Temperature & Salinity</h2>
//             <div className="h-96">
//               <TimeSeriesChart data={timeSeriesData} loading={loading} />
//             </div>
//           </div>

//           {/* Vertical Profile Chart */}
//           <div className="card">
//             <h2 className="text-lg font-semibold text-gray-900 mb-4">Vertical Profile</h2>
//             <p className="text-sm text-gray-600 mb-4">Sample date: June 15, 2012</p>
//             <div className="h-96">
//               <VerticalProfileChart data={profileData} loading={loading} />
//             </div>
//           </div>

//           {/* Heat Content Heatmap */}
//           <div className="card">
//             <h2 className="text-lg font-semibold text-gray-900 mb-4">Heat Content Over Time</h2>
//             <div className="h-96">
//               <HeatmapChart data={heatContentData} loading={loading} />
//             </div>
//           </div>
//         </div>

//         {/* Additional Info */}
//         <div className="mt-8 card">
//           <h2 className="text-lg font-semibold text-gray-900 mb-4">About the Data</h2>
//           <div className="prose text-gray-600">
//             <p>
//               This dashboard displays ARGO float data from the Indian Ocean covering the period 2010-2013. 
//               The data includes surface temperature and salinity measurements, monthly averaged profiles by depth, 
//               and integrated heat content calculations.
//             </p>
//             <p className="mt-3">
//               Click on any location on the map to explore data for that specific coordinate. 
//               The visualizations will update automatically to show relevant measurements and trends.
//             </p>
//           </div>
//         </div>
//       </div>
//     </div>
//   )
// }


'use client'

import { useState, useEffect } from 'react'
import dynamic from 'next/dynamic'
import { Calendar, Download, Filter, MapPin, Info } from 'lucide-react'
import { TimeSeriesChart } from '../../components/charts/TimeSeriesChart'
import VerticalProfileChart from '../../components/charts/VerticalProfileChart'
import { HeatmapChart } from '../../components/charts/HeatmapChart'
import { FilterPanel } from '../../components/FilterPanel'
import { DataSummaryCard } from '../../components/DataSummaryCard'
import { apiClient } from '../../lib/api-client'
import type { TimeSeriesPoint, VerticalProfilePoint, HeatContentPoint } from '../../lib/api-client'

const OceanMap = dynamic(() => import('../../components/OceanMap'), {
  ssr: false,
  loading: () => <div className="h-96 bg-gray-100 rounded-lg animate-pulse" />,
})

// If you later lift dataset context (from chat ingestion) to a global store or React context,
// you can import and use it here. For now, we keep a placeholder.
// import { useDatasetContext } from '../../lib/dataset-context'

interface DataSummary {
  total_records: number
  date_range: { start: string; end: string }
  spatial_coverage: {
    latitude: { min: number; max: number }
    longitude: { min: number; max: number }
  }
  measurement_counts: Record<string, number>
}

export default function DashboardPage() {
  // const datasetCtx = useDatasetContext() // optional, when available

  const [dataSummary, setDataSummary] = useState<DataSummary | null>(null)
  const [selectedLocation, setSelectedLocation] = useState<{ lat: number; lon: number } | null>(null)
  const [timeSeriesData, setTimeSeriesData] = useState<TimeSeriesPoint[]>([])
  const [profileData, setProfileData] = useState<VerticalProfilePoint[]>([])
  const [heatContentData, setHeatContentData] = useState<HeatContentPoint[]>([])
  const [loading, setLoading] = useState(true)
  const [showFilters, setShowFilters] = useState(false)

  useEffect(() => {
    loadDataSummary()
  }, [])

  useEffect(() => {
    if (selectedLocation) {
      loadLocationData(selectedLocation)
    }
  }, [selectedLocation])

  async function loadDataSummary() {
    try {
      const summary = await apiClient.getDataSummary()
      setDataSummary(summary)

      // Initialize default location (equator, 60E)
      if (summary?.spatial_coverage) {
        setSelectedLocation({ lat: 0, lon: 60 })
      }
    } catch (error) {
      console.error('Failed to load data summary:', error)
    } finally {
      setLoading(false)
    }
  }

  async function loadLocationData(location: { lat: number; lon: number }) {
    setLoading(true)
    try {
      const timeSeries = await apiClient.getSurfaceTimeseries({
        lat: location.lat,
        lon: location.lon,
        start: '2010-01-01',
        end: '2013-12-31',
      })
      setTimeSeriesData(timeSeries)

      const profile = await apiClient.getVerticalProfile({
        lat: location.lat,
        lon: location.lon,
        date: '2012-06-15',
      })
      setProfileData(profile)

      const heatContent = await apiClient.getHeatContent({
        lat: location.lat,
        lon: location.lon,
        start: '2010-01-01',
        end: '2013-12-31',
      })
      setHeatContentData(heatContent)
    } catch (error) {
      console.error('Failed to load location data:', error)
    } finally {
      setLoading(false)
    }
  }

  function handleLocationSelect(lat: number, lon: number) {
    setSelectedLocation({ lat, lon })
  }

  if (loading && !dataSummary) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading dashboard...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">Ocean Data Dashboard</h1>
              <p className="text-gray-600 mt-1">Interactive visualization of ARGO float data</p>
            </div>

            <div className="flex items-center space-x-4">
              <button
                type="button"
                onClick={() => setShowFilters(!showFilters)}
                className="btn-secondary inline-flex items-center"
              >
                <Filter className="h-4 w-4 mr-2" />
                Filters
              </button>
              <button type="button" className="btn-primary inline-flex items-center">
                <Download className="h-4 w-4 mr-2" />
                Export
              </button>
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Optional: Active dataset banner (visible when a datasetCtx is available) */}
        {/* {datasetCtx && (
          <div className="mb-6 rounded-md border bg-white p-3 text-sm text-gray-700 flex items-start gap-2">
            <Info className="h-4 w-4 mt-0.5 text-blue-600" />
            <div>
              <div className="font-medium">Active dataset</div>
              <div>Parquet: {datasetCtx.parquet_path}</div>
              <div>Time: {JSON.stringify(datasetCtx.date_range)} • Bounds: {JSON.stringify(datasetCtx.spatial_bounds)}</div>
            </div>
          </div>
        )} */}

        {/* Data Summary Cards */}
        {dataSummary && (
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
            <DataSummaryCard
              title="Total Records"
              value={dataSummary.total_records.toLocaleString()}
              icon={<Calendar className="h-6 w-6" />}
              trend="+12.5%"
            />
            <DataSummaryCard
              title="Date Range"
              value={`${dataSummary.date_range.start} to ${dataSummary.date_range.end}`}
              icon={<Calendar className="h-6 w-6" />}
            />
            <DataSummaryCard
              title="Spatial Coverage"
              value={`${dataSummary.spatial_coverage.longitude.min}°E – ${dataSummary.spatial_coverage.longitude.max}°E`}
              icon={<MapPin className="h-6 w-6" />}
            />
            <DataSummaryCard
              title="Data Types"
              value={Object.keys(dataSummary.measurement_counts).length.toString()}
              icon={<Filter className="h-6 w-6" />}
            />
          </div>
        )}

        {/* Filter Panel */}
        {showFilters && (
          <div className="mb-8">
            <FilterPanel
              onLocationChange={handleLocationSelect}
              onDateRangeChange={(start, end) => {
                // Hook up if you add date filtering to the API calls
                console.log('Date range:', start, end)
              }}
            />
          </div>
        )}

        {/* Main Content Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Map */}
          <div className="card">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-lg font-semibold text-gray-900">Float Locations</h2>
              {selectedLocation && (
                <div className="text-sm text-gray-600">
                  Selected: {selectedLocation.lat}°N, {selectedLocation.lon}°E
                </div>
              )}
            </div>
            <div className="h-96">
              <OceanMap
                onLocationSelect={handleLocationSelect}
                selectedLocation={selectedLocation}
                floatLocations={[
                  { lat: 0, lon: 60, id: 'float-60E' },
                  { lat: 0, lon: 80, id: 'float-80E' },
                  { lat: 0, lon: 100, id: 'float-100E' },
                ]}
              />
            </div>
          </div>

          {/* Time Series */}
          <div className="card">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">Surface Temperature & Salinity</h2>
            <div className="h-96">
              <TimeSeriesChart data={timeSeriesData} loading={loading} />
            </div>
          </div>

          {/* Vertical Profile */}
          <div className="card">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">Vertical Profile</h2>
            <p className="text-sm text-gray-600 mb-4">Sample date: June 15, 2012</p>
            <div className="h-96">
              <VerticalProfileChart data={profileData} loading={loading} />
            </div>
          </div>

          {/* Heat Content */}
          <div className="card">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">Heat Content Over Time</h2>
            <div className="h-96">
              <HeatmapChart data={heatContentData} loading={loading} />
            </div>
          </div>
        </div>

        {/* About */}
        <div className="mt-8 card">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">About the Data</h2>
          <div className="prose text-gray-600">
            <p>
              This dashboard displays ARGO float data from the Indian Ocean covering the period 2010–2013. The data
              includes surface temperature and salinity measurements, monthly averaged profiles by depth, and integrated
              heat content calculations.
            </p>
            <p className="mt-3">
              Click on any location on the map to explore data for that specific coordinate. The visualizations update
              automatically to show relevant measurements and trends.
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}