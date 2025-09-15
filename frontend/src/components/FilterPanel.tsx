'use client'

import { useState } from 'react'
import { X, Calendar, MapPin } from 'lucide-react'

interface FilterPanelProps {
  onLocationChange: (lat: number, lon: number) => void
  onDateRangeChange: (start: string, end: string) => void
  onClose?: () => void
}

export function FilterPanel({
  onLocationChange,
  onDateRangeChange,
  onClose
}: FilterPanelProps) {
  const [latitude, setLatitude] = useState('0')
  const [longitude, setLongitude] = useState('60')
  const [startDate, setStartDate] = useState('2010-01-01')
  const [endDate, setEndDate] = useState('2013-12-31')

  const handleLocationUpdate = () => {
    const lat = parseFloat(latitude)
    const lon = parseFloat(longitude)
    
    if (!isNaN(lat) && !isNaN(lon)) {
      onLocationChange(lat, lon)
    }
  }

  const handleDateRangeUpdate = () => {
    if (startDate && endDate) {
      onDateRangeChange(startDate, endDate)
    }
  }

  const presetLocations = [
    { name: '60°E Equator', lat: 0, lon: 60 },
    { name: '80°E Equator', lat: 0, lon: 80 },
    { name: '100°E Equator', lat: 0, lon: 100 }
  ]

  return (
    <div className="card bg-white">
      <div className="flex justify-between items-center mb-6">
        <h3 className="text-lg font-semibold text-gray-900">Data Filters</h3>
        {onClose && (
          <button
            type="button"
            onClick={onClose}
            className="p-1 hover:bg-gray-100 rounded-lg transition-colors"
          >
            <X className="h-5 w-5 text-gray-500" />
          </button>
        )}
      </div>

      <div className="space-y-6">
        {/* Location Filter */}
        <div>
          <div className="flex items-center space-x-2 mb-3">
            <MapPin className="h-4 w-4 text-primary-600" />
            <label className="text-sm font-medium text-gray-700">
              Location
            </label>
          </div>
          
          <div className="grid grid-cols-2 gap-3 mb-3">
            <div>
              <label className="block text-xs text-gray-600 mb-1">Latitude</label>
              <input
                type="number"
                value={latitude}
                onChange={(e) => setLatitude(e.target.value)}
                onBlur={handleLocationUpdate}
                step="0.1"
                min="-90"
                max="90"
                className="input-field text-sm"
                placeholder="0.0"
              />
            </div>
            <div>
              <label className="block text-xs text-gray-600 mb-1">Longitude</label>
              <input
                type="number"
                value={longitude}
                onChange={(e) => setLongitude(e.target.value)}
                onBlur={handleLocationUpdate}
                step="0.1"
                min="-180"
                max="180"
                className="input-field text-sm"
                placeholder="60.0"
              />
            </div>
          </div>

          {/* Preset locations */}
          <div className="flex flex-wrap gap-2">
            {presetLocations.map((preset) => (
              <button
                type="button"
                key={preset.name}
                onClick={(e) => {
                  e.preventDefault()
                  setLatitude(preset.lat.toString())
                  setLongitude(preset.lon.toString())
                  onLocationChange(preset.lat, preset.lon)
                }}
                className="text-xs bg-primary-50 text-primary-700 px-2 py-1 rounded-md hover:bg-primary-100 transition-colors"
              >
                {preset.name}
              </button>
            ))}
          </div>
        </div>

        {/* Date Range Filter */}
        <div>
          <div className="flex items-center space-x-2 mb-3">
            <Calendar className="h-4 w-4 text-primary-600" />
            <label className="text-sm font-medium text-gray-700">
              Date Range
            </label>
          </div>
          
          <div className="grid grid-cols-2 gap-3 mb-3">
            <div>
              <label className="block text-xs text-gray-600 mb-1">Start Date</label>
              <input
                type="date"
                value={startDate}
                onChange={(e) => setStartDate(e.target.value)}
                onBlur={handleDateRangeUpdate}
                min="2010-01-01"
                max="2013-12-31"
                className="input-field text-sm"
              />
            </div>
            <div>
              <label className="block text-xs text-gray-600 mb-1">End Date</label>
              <input
                type="date"
                value={endDate}
                onChange={(e) => setEndDate(e.target.value)}
                onBlur={handleDateRangeUpdate}
                min="2010-01-01"
                max="2013-12-31"
                className="input-field text-sm"
              />
            </div>
          </div>

          {/* Preset date ranges */}
          <div className="flex flex-wrap gap-2">
            <button
              type="button"
              onClick={() => {
                setStartDate('2010-01-01')
                setEndDate('2010-12-31')
                onDateRangeChange('2010-01-01', '2010-12-31')
              }}
              className="text-xs bg-ocean-50 text-ocean-700 px-2 py-1 rounded-md hover:bg-ocean-100 transition-colors"
            >
              2010
            </button>
            <button
              type="button"
              onClick={(e) => {
                e.preventDefault()
                setStartDate('2012-01-01')
                setEndDate('2012-12-31')
                onDateRangeChange('2012-01-01', '2012-12-31')
              }}
              className="text-xs bg-ocean-50 text-ocean-700 px-2 py-1 rounded-md hover:bg-ocean-100 transition-colors"
            >
              2012
            </button>
            <button
              type='button'
              onClick={(e) => {
                e.preventDefault()
                setStartDate('2010-01-01')
                setEndDate('2013-12-31')
                onDateRangeChange('2010-01-01', '2013-12-31')
              }}
              className="text-xs bg-ocean-50 text-ocean-700 px-2 py-1 rounded-md hover:bg-ocean-100 transition-colors"
            >
              Full Range
            </button>
          </div>
        </div>

        {/* Apply Filters Button */}
        <div className="pt-4 border-t">
          <button
            type="button"
            onClick={() => {
              handleLocationUpdate()
              handleDateRangeUpdate()
            }}
            className="btn-primary w-full"
          >
            Apply Filters
          </button>
        </div>
      </div>
    </div>
  )
}