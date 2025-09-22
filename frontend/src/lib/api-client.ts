// /**
//  * API client for FloatChat backend services.
//  * 
//  * Provides typed interfaces for all backend API endpoints with proper
//  * error handling and response transformation.
//  */

// const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

// // Type definitions for API responses
// export interface DataSummary {
//   total_records: number
//   date_range: { start: string; end: string }
//   spatial_coverage: {
//     latitude: { min: number; max: number }
//     longitude: { min: number; max: number }
//   }
//   data_types: string[]
//   measurement_counts: Record<string, number>
// }

// export interface TimeSeriesPoint {
//   time: string
//   temperature?: number
//   salinity?: number
//   depth?: number
// }

// export interface VerticalProfilePoint {
//   depth: number
//   temperature?: number
//   salinity?: number
//   date: string
// }

// export interface HeatContentPoint {
//   time: string
//   lat: number
//   lon: number
//   heat_content: number
// }

// export interface ChatRequest {
//   message: string
//   context?: Record<string, any>
// }

// export interface ChatResponse {
//   response: string
//   timestamp: string
//   sources?: string[]
//   confidence?: number
// }

// // API query parameters
// export interface TimeSeriesParams {
//   lat: number
//   lon: number
//   start?: string
//   end?: string
//   depth?: number
// }

// export interface VerticalProfileParams {
//   lat: number
//   lon: number
//   date: string
// }

// export interface HeatContentParams {
//   lat: number
//   lon: number
//   start?: string
//   end?: string
// }

// class APIError extends Error {
//   constructor(
//     message: string,
//     public status: number,
//     public response?: any
//   ) {
//     super(message)
//     this.name = 'APIError'
//   }
// }

// class APIClient {
//   private baseURL: string

//   constructor(baseURL: string = API_BASE_URL) {
//     this.baseURL = baseURL
//   }

//   private async request<T>(
//     endpoint: string,
//     options: RequestInit = {}
//   ): Promise<T> {
//     const url = `${this.baseURL}${endpoint}`
    
//     const defaultHeaders = {
//       'Content-Type': 'application/json',
//       ...options.headers,
//     }

//     try {
//       const response = await fetch(url, {
//         ...options,
//         headers: defaultHeaders,
//       })

//       if (!response.ok) {
//         let errorMessage = `HTTP ${response.status}: ${response.statusText}`
//         let errorData

//         try {
//           errorData = await response.json()
//           if (errorData.detail) {
//             errorMessage = errorData.detail
//           }
//         } catch {
//           // Response is not JSON, use status text
//         }

//         throw new APIError(errorMessage, response.status, errorData)
//       }

//       // Handle empty responses (like 204 No Content)
//       if (response.status === 204 || response.headers.get('content-length') === '0') {
//         return {} as T
//       }

//       const data = await response.json()
//       return data as T
//     } catch (error) {
//       if (error instanceof APIError) {
//         throw error
//       }

//       // Network or other errors
//       throw new APIError(
//         error instanceof Error ? error.message : 'Network error',
//         0
//       )
//     }
//   }

//   // Health check
//   async healthCheck(): Promise<{ status: string; timestamp: string; version: string }> {
//     return this.request('/api/health')
//   }

//   // Data summary
//   async getDataSummary(): Promise<DataSummary> {
//     return this.request('/api/data-summary')
//   }

//   // Surface timeseries data
//   async getSurfaceTimeseries(params: TimeSeriesParams): Promise<TimeSeriesPoint[]> {
//     const searchParams = new URLSearchParams({
//       lat: params.lat.toString(),
//       lon: params.lon.toString(),
//     })

//     if (params.start) searchParams.append('start', params.start)
//     if (params.end) searchParams.append('end', params.end)
//     if (params.depth !== undefined) searchParams.append('depth', params.depth.toString())

//     return this.request(`/api/surface-timeseries?${searchParams}`)
//   }

//   // Vertical profile data
//   async getVerticalProfile(params: VerticalProfileParams): Promise<VerticalProfilePoint[]> {
//     const searchParams = new URLSearchParams({
//       lat: params.lat.toString(),
//       lon: params.lon.toString(),
//       date: params.date,
//     })

//     return this.request(`/api/vertical-profile?${searchParams}`)
//   }

//   // Heat content data
//   async getHeatContent(params: HeatContentParams): Promise<HeatContentPoint[]> {
//     const searchParams = new URLSearchParams({
//       lat: params.lat.toString(),
//       lon: params.lon.toString(),
//     })

//     if (params.start) searchParams.append('start', params.start)
//     if (params.end) searchParams.append('end', params.end)

//     return this.request(`/api/heat-content?${searchParams}`)
//   }

//   // Chat interface
//   async chatWithData(request: ChatRequest): Promise<ChatResponse> {
//     return this.request('/api/chat', {
//       method: 'POST',
//       body: JSON.stringify(request),
//     })
//   }

//   // NetCDF ingestion (stub)
//   async ingestNetCDF(): Promise<{ status: string; message: string }> {
//     return this.request('/api/ingest-netcdf', {
//       method: 'POST',
//     })
//   }
// }

// // Export singleton instance
// export const apiClient = new APIClient()

// // Export error class for error handling in components
// export { APIError }

// // Utility functions for error handling
// export const handleAPIError = (error: unknown): string => {
//   if (error instanceof APIError) {
//     return error.message
//   }
//   if (error instanceof Error) {
//     return error.message
//   }
//   return 'An unexpected error occurred'
// }

// // Helper function to check API availability
// export const checkAPIHealth = async (): Promise<boolean> => {
//   try {
//     await apiClient.healthCheck()
//     return true
//   } catch {
//     return false
//   }
// }

/**
 * API client for FloatChat backend services.
 *
 * Provides typed interfaces for all backend API endpoints with proper
 * error handling and response transformation.
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

// ---------------------- Types ----------------------

export interface DataSummary {
  total_records: number
  date_range: { start: string; end: string }
  spatial_coverage: {
    latitude: { min: number; max: number }
    longitude: { min: number; max: number }
  }
  data_types: string[]
  measurement_counts: Record<string, number>
}

export interface TimeSeriesPoint {
  time: string
  temperature?: number
  salinity?: number
  depth?: number
}

export interface VerticalProfilePoint {
  depth: number
  temperature?: number
  salinity?: number
  date: string
}

export interface HeatContentPoint {
  time: string
  lat: number
  lon: number
  heat_content: number
}

export interface ChatRequest {
  message: string
  context?: Record<string, any>
}

export interface ChatResponse {
  response: string
  timestamp: string
  sources?: string[]
  confidence?: number
}

export interface TimeSeriesParams {
  lat: number
  lon: number
  start?: string
  end?: string
  depth?: number
}

export interface VerticalProfileParams {
  lat: number
  lon: number
  date: string
}

export interface HeatContentParams {
  lat: number
  lon: number
  start?: string
  end?: string
}

export interface IngestResult {
  success: boolean
  records: number
  output_file: string | null
  metadata: {
    variables?: string[]
    dims?: Record<string, number>
    date_range?: { start: string; end: string }
    spatial_bounds?: { lat_min: number; lat_max: number; lon_min: number; lon_max: number }
    has_depth?: boolean
  }
  errors?: string[]
  file_path: string
}

// ---------------------- Error ----------------------

class APIError extends Error {
  constructor(
    message: string,
    public status: number,
    public response?: any
  ) {
    super(message)
    this.name = 'APIError'
  }
}

// ---------------------- Client ----------------------

class APIClient {
  private baseURL: string

  constructor(baseURL: string = API_BASE_URL) {
    this.baseURL = baseURL
  }

  private async request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
    const url = `${this.baseURL}${endpoint}`

    // Do NOT force JSON headers for FormData requests
    const isFormData =
      typeof FormData !== 'undefined' && options.body instanceof FormData

    const headers: HeadersInit = isFormData
      ? (options.headers as HeadersInit) || {}
      : {
          'Content-Type': 'application/json',
          ...(options.headers as HeadersInit),
        }

    try {
      const response = await fetch(url, {
        ...options,
        headers,
      })

      if (!response.ok) {
        let errorMessage = `HTTP ${response.status}: ${response.statusText}`
        let errorData: any = undefined

        try {
          // Try to parse JSON error
          errorData = await response.json()
          if (errorData?.detail) {
            errorMessage = typeof errorData.detail === 'string'
              ? errorData.detail
              : JSON.stringify(errorData.detail)
          }
        } catch {
          // Non-JSON error
          try {
            const text = await response.text()
            if (text) errorMessage = text
          } catch {
            // ignore
          }
        }

        throw new APIError(errorMessage, response.status, errorData)
      }

      // No content
      if (response.status === 204) return {} as T

      const contentType = response.headers.get('content-type') || ''
      if (contentType.includes('application/json')) {
        return (await response.json()) as T
      }
      // Fallback: text or empty
      const text = await response.text()
      return (text ? (JSON.parse(text) as T) : ({} as T))
    } catch (error) {
      if (error instanceof APIError) throw error
      throw new APIError(error instanceof Error ? error.message : 'Network error', 0)
    }
  }

  // ---------- Health ----------
  async healthCheck(): Promise<{ status: string; timestamp: string; version: string }> {
    return this.request('/api/health')
  }

  // ---------- Data summary ----------
  async getDataSummary(): Promise<DataSummary> {
    return this.request('/api/data-summary')
  }

  // ---------- Surface time series ----------
  async getSurfaceTimeseries(params: TimeSeriesParams): Promise<TimeSeriesPoint[]> {
    const searchParams = new URLSearchParams({
      lat: params.lat.toString(),
      lon: params.lon.toString(),
    })
    if (params.start) searchParams.append('start', params.start)
    if (params.end) searchParams.append('end', params.end)
    if (params.depth !== undefined) searchParams.append('depth', params.depth.toString())
    return this.request(`/api/surface-timeseries?${searchParams.toString()}`)
  }

  // ---------- Vertical profile ----------
  async getVerticalProfile(params: VerticalProfileParams): Promise<VerticalProfilePoint[]> {
    const searchParams = new URLSearchParams({
      lat: params.lat.toString(),
      lon: params.lon.toString(),
      date: params.date,
    })
    return this.request(`/api/vertical-profile?${searchParams.toString()}`)
  }

  // ---------- Heat content ----------
  async getHeatContent(params: HeatContentParams): Promise<HeatContentPoint[]> {
    const searchParams = new URLSearchParams({
      lat: params.lat.toString(),
      lon: params.lon.toString(),
    })
    if (params.start) searchParams.append('start', params.start)
    if (params.end) searchParams.append('end', params.end)
    return this.request(`/api/heat-content?${searchParams.toString()}`)
  }

  // ---------- Chat ----------
  async chatWithData(request: ChatRequest): Promise<ChatResponse> {
    return this.request('/api/chat', {
      method: 'POST',
      body: JSON.stringify(request),
    })
  }

  // ---------- NetCDF ingestion (by server path) ----------
  async ingestNetcdfByPath(filePath: string): Promise<IngestResult> {
    const fd = new FormData()
    fd.append('file_path', filePath)
    return this.request('/api/ingest-netcdf', {
      method: 'POST',
      body: fd, // FormData → no JSON headers
    })
  }

  // ---------- NetCDF ingestion (upload file) ----------
  async ingestNetcdfUpload(file: File): Promise<IngestResult> {
    const fd = new FormData()
    fd.append('file', file)
    return this.request('/api/ingest-netcdf', {
      method: 'POST',
      body: fd, // FormData → no JSON headers
    })
  }
}

// Singleton instance
export const apiClient = new APIClient()

// Export error class
export { APIError }

// Utility functions
export const handleAPIError = (error: unknown): string => {
  if (error instanceof APIError) return error.message
  if (error instanceof Error) return error.message
  return 'An unexpected error occurred'
}

export const checkAPIHealth = async (): Promise<boolean> => {
  try {
    await apiClient.healthCheck()
    return true
  } catch {
    return false
  }
}