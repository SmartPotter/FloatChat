'use client'

import { useEffect, useState } from 'react'
import { MapContainer, TileLayer, Marker, Popup, useMapEvents } from 'react-leaflet'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'

// Fix for default markers in Next.js
delete (L.Icon.Default.prototype as any)._getIconUrl
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-shadow.png',
})

interface FloatLocation {
  lat: number
  lon: number
  id: string
}

interface OceanMapProps {
  onLocationSelect: (lat: number, lon: number) => void
  selectedLocation?: { lat: number; lon: number } | null
  floatLocations: FloatLocation[]
  height?: string
}

// Custom marker icons
const floatIcon = new L.Icon({
  iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-blue.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41]
})

const selectedIcon = new L.Icon({
  iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41]
})

function MapEvents({ onLocationSelect }: { onLocationSelect: (lat: number, lon: number) => void }) {
  useMapEvents({
    click: (e) => {
      const { lat, lng } = e.latlng
      onLocationSelect(lat, lng)
    }
  })
  return null
}

export default function OceanMap({
  onLocationSelect,
  selectedLocation,
  floatLocations,
  height = '400px'
}: OceanMapProps) {
  const [isClient, setIsClient] = useState(false)

  useEffect(() => {
    setIsClient(true)
  }, [])

  if (!isClient) {
    return <div className="bg-gray-100 rounded-lg animate-pulse" style={{ height }} />
  }

  // Center on Indian Ocean
  const center: [number, number] = [0, 80] // Equator, 80°E
  const zoom = 4

  return (
    <MapContainer
      center={center}
      zoom={zoom}
      style={{ height, width: '100%' }}
      className="rounded-lg"
    >
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      
      <MapEvents onLocationSelect={onLocationSelect} />
      
      {/* Float location markers */}
      {floatLocations.map((location) => {
        const isSelected = selectedLocation && 
          selectedLocation.lat === location.lat && 
          selectedLocation.lon === location.lon
        
        return (
          <Marker
            key={location.id}
            position={[location.lat, location.lon]}
            icon={isSelected ? selectedIcon : floatIcon}
            eventHandlers={{
              click: () => onLocationSelect(location.lat, location.lon)
            }}
          >
            <Popup>
              <div className="text-sm">
                <strong>ARGO Float Location</strong>
                <br />
                Latitude: {location.lat}°
                <br />
                Longitude: {location.lon}°
                <br />
                <em>Click to load data for this location</em>
              </div>
            </Popup>
          </Marker>
        )
      })}

      {/* Selected location marker (if different from float locations) */}
      {selectedLocation && 
       !floatLocations.some(loc => 
         loc.lat === selectedLocation.lat && loc.lon === selectedLocation.lon
       ) && (
        <Marker
          position={[selectedLocation.lat, selectedLocation.lon]}
          icon={selectedIcon}
        >
          <Popup>
            <div className="text-sm">
              <strong>Selected Location</strong>
              <br />
              Latitude: {selectedLocation.lat.toFixed(2)}°
              <br />
              Longitude: {selectedLocation.lon.toFixed(2)}°
            </div>
          </Popup>
        </Marker>
      )}
    </MapContainer>
  )
}