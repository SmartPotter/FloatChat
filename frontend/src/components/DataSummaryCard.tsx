import { ReactNode } from 'react'
import { TrendingUp, TrendingDown } from 'lucide-react'

interface DataSummaryCardProps {
  title: string
  value: string
  icon: ReactNode
  trend?: string
  trendDirection?: 'up' | 'down'
  description?: string
}

export function DataSummaryCard({
  title,
  value,
  icon,
  trend,
  trendDirection,
  description
}: DataSummaryCardProps) {
  return (
    <div className="card bg-white">
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <div className="flex items-center space-x-2 mb-1">
            <div className="text-primary-600">
              {icon}
            </div>
            <h3 className="text-sm font-medium text-gray-600">{title}</h3>
          </div>
          
          <div className="mb-1">
            <p className="text-2xl font-bold text-gray-900">{value}</p>
          </div>

          {description && (
            <p className="text-xs text-gray-500 mb-2">{description}</p>
          )}

          {trend && (
            <div className="flex items-center space-x-1">
              {trendDirection === 'up' ? (
                <TrendingUp className="h-3 w-3 text-green-500" />
              ) : trendDirection === 'down' ? (
                <TrendingDown className="h-3 w-3 text-red-500" />
              ) : null}
              <span className={`text-xs font-medium ${
                trendDirection === 'up' ? 'text-green-600' :
                trendDirection === 'down' ? 'text-red-600' : 
                'text-gray-600'
              }`}>
                {trend}
              </span>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}