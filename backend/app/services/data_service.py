"""
Data service layer for ARGO float data operations.

Handles data retrieval from database or CSV fallback, with caching
and query optimization for common oceanographic data patterns.
"""

import pandas as pd
import numpy as np
from datetime import datetime, date
from typing import List, Optional, Dict, Any
import os
import logging
from pathlib import Path

from ..models.schemas import (
    DataSummaryResponse, TimeSeriesPoint, VerticalProfilePoint, HeatContentPoint
)

logger = logging.getLogger(__name__)


class DataService:
    """Service class for oceanographic data operations."""
    
    def __init__(self):
        self.data_path = Path(__file__).parent.parent.parent / "seed_data"
        self._surface_cache = None
        self._monthly_cache = None
        self._heat_cache = None
        self._load_csv_data()
    
    def _load_csv_data(self):
        """Load CSV data files into memory for fast access."""
        try:
            # Load surface timeseries data
            surface_file = self.data_path / "surface_timeseries.csv"
            if surface_file.exists():
                self._surface_cache = pd.read_csv(surface_file)
                self._surface_cache['time'] = pd.to_datetime(self._surface_cache['time'])
                logger.info(f"Loaded {len(self._surface_cache)} surface records")
            
            # Load monthly averages
            monthly_file = self.data_path / "monthly_averages.csv"
            if monthly_file.exists():
                self._monthly_cache = pd.read_csv(monthly_file)
                self._monthly_cache['time'] = pd.to_datetime(self._monthly_cache['time'])
                # Handle missing values
                self._monthly_cache = self._monthly_cache.replace('', np.nan)
                logger.info(f"Loaded {len(self._monthly_cache)} monthly records")
            
            # Load heat content data
            heat_file = self.data_path / "heat_content.csv"
            if heat_file.exists():
                self._heat_cache = pd.read_csv(heat_file)
                self._heat_cache['time'] = pd.to_datetime(self._heat_cache['time'])
                logger.info(f"Loaded {len(self._heat_cache)} heat content records")
                
        except Exception as e:
            logger.error(f"Error loading CSV data: {e}")
            raise
    
    async def get_data_summary(self) -> DataSummaryResponse:
        """Generate comprehensive summary of available data."""
        try:
            total_records = 0
            measurement_counts = {}
            all_dates = []
            lats, lons = [], []
            
            # Process surface data
            if self._surface_cache is not None:
                surface_count = len(self._surface_cache)
                total_records += surface_count
                measurement_counts['surface_timeseries'] = surface_count
                all_dates.extend(self._surface_cache['time'].tolist())
            
            # Process monthly averages
            if self._monthly_cache is not None:
                monthly_count = len(self._monthly_cache.dropna())
                total_records += monthly_count
                measurement_counts['monthly_averages'] = monthly_count
                all_dates.extend(self._monthly_cache['time'].tolist())
                lats.extend(self._monthly_cache['lat'].dropna().tolist())
                lons.extend(self._monthly_cache['lon'].dropna().tolist())
            
            # Process heat content
            if self._heat_cache is not None:
                heat_count = len(self._heat_cache)
                total_records += heat_count
                measurement_counts['heat_content'] = heat_count
                all_dates.extend(self._heat_cache['time'].tolist())
                lats.extend(self._heat_cache['lat'].tolist())
                lons.extend(self._heat_cache['lon'].tolist())
            
            # Calculate ranges
            date_range = {
                "start": min(all_dates).strftime("%Y-%m-%d") if all_dates else None,
                "end": max(all_dates).strftime("%Y-%m-%d") if all_dates else None
            }
            
            spatial_coverage = {
                "latitude": {
                    "min": float(min(lats)) if lats else None,
                    "max": float(max(lats)) if lats else None
                },
                "longitude": {
                    "min": float(min(lons)) if lons else None, 
                    "max": float(max(lons)) if lons else None
                }
            }
            
            data_types = ["temperature", "salinity", "heat_content", "depth_profiles"]
            
            return DataSummaryResponse(
                total_records=total_records,
                date_range=date_range,
                spatial_coverage=spatial_coverage,
                data_types=data_types,
                measurement_counts=measurement_counts
            )
            
        except Exception as e:
            logger.error(f"Error generating data summary: {e}")
            raise
    
    async def get_surface_timeseries(
        self, 
        lat: float, 
        lon: float, 
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        depth: Optional[float] = None
    ) -> List[TimeSeriesPoint]:
        """Retrieve surface or depth-specific timeseries data."""
        try:
            # For surface data (no depth specified), use surface_timeseries.csv
            if depth is None or depth <= 10.0:
                if self._surface_cache is None:
                    return []
                
                df = self._surface_cache.copy()
                
                # Apply date filters
                if start_date:
                    df = df[df['time'] >= start_date]
                if end_date:
                    df = df[df['time'] <= end_date]
                
                # Convert to response format
                return [
                    TimeSeriesPoint(
                        time=row['time'],
                        temperature=row.get('temperature'),
                        salinity=row.get('salinity'),
                        depth=0.0
                    )
                    for _, row in df.iterrows()
                ]
            
            # For depth-specific data, use monthly_averages.csv
            if self._monthly_cache is None:
                return []
            
            # Filter by location (find closest match)
            df = self._monthly_cache.copy()
            
            # Simple nearest neighbor for location matching
            df['lat_diff'] = abs(df['lat'] - lat)
            df['lon_diff'] = abs(df['lon'] - lon)
            df['location_dist'] = df['lat_diff'] + df['lon_diff']
            
            # Get data for closest location
            closest_location = df.loc[df['location_dist'].idxmin()]
            location_mask = (df['lat'] == closest_location['lat']) & (df['lon'] == closest_location['lon'])
            df = df[location_mask]
            
            # Filter by depth if specified
            if depth is not None:
                # Find closest depth
                df['depth_diff'] = abs(df['depth'] - depth)
                closest_depth = df.loc[df['depth_diff'].idxmin()]['depth']
                df = df[df['depth'] == closest_depth]
            
            # Apply date filters
            if start_date:
                df = df[df['time'] >= start_date]
            if end_date:
                df = df[df['time'] <= end_date]
            
            # Remove rows with missing data
            df = df.dropna(subset=['temperature', 'salinity'])
            
            return [
                TimeSeriesPoint(
                    time=row['time'],
                    temperature=row.get('temperature'),
                    salinity=row.get('salinity'),
                    depth=row.get('depth', depth)
                )
                for _, row in df.iterrows()
            ]
            
        except Exception as e:
            logger.error(f"Error retrieving surface timeseries: {e}")
            return []
    
    async def get_vertical_profile(
        self, 
        lat: float, 
        lon: float, 
        date: date
    ) -> List[VerticalProfilePoint]:
        """Get vertical profile for specific location and date."""
        try:
            if self._monthly_cache is None:
                return []
            
            df = self._monthly_cache.copy()
            
            # Find closest location
            df['lat_diff'] = abs(df['lat'] - lat)
            df['lon_diff'] = abs(df['lon'] - lon)
            df['location_dist'] = df['lat_diff'] + df['lon_diff']
            
            closest_location = df.loc[df['location_dist'].idxmin()]
            location_mask = (df['lat'] == closest_location['lat']) & (df['lon'] == closest_location['lon'])
            df = df[location_mask]
            
            # Find closest date
            target_date = pd.to_datetime(date)
            df['date_diff'] = abs(df['time'] - target_date)
            closest_date = df.loc[df['date_diff'].idxmin()]['time']
            df = df[df['time'] == closest_date]
            
            # Remove rows with missing data
            df = df.dropna(subset=['temperature', 'salinity', 'depth'])
            
            # Sort by depth
            df = df.sort_values('depth')
            
            return [
                VerticalProfilePoint(
                    depth=row['depth'],
                    temperature=row.get('temperature'),
                    salinity=row.get('salinity'),
                    Date=closest_date.date()
                )
                for _, row in df.iterrows()
            ]
            
        except Exception as e:
            logger.error(f"Error retrieving vertical profile: {e}")
            return []
    
    async def get_heat_content(
        self, 
        lat: float, 
        lon: float,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[HeatContentPoint]:
        """Retrieve heat content timeseries for location."""
        try:
            if self._heat_cache is None:
                return []
            
            df = self._heat_cache.copy()
            
            # Filter by location (exact match or closest)
            location_mask = (df['lat'] == lat) & (df['lon'] == lon)
            
            if not location_mask.any():
                # Find closest location if exact match not found
                df['lat_diff'] = abs(df['lat'] - lat)
                df['lon_diff'] = abs(df['lon'] - lon)
                df['location_dist'] = df['lat_diff'] + df['lon_diff']
                
                closest_location = df.loc[df['location_dist'].idxmin()]
                location_mask = (df['lat'] == closest_location['lat']) & (df['lon'] == closest_location['lon'])
            
            df = df[location_mask]
            
            # Apply date filters
            if start_date:
                df = df[df['time'] >= start_date]
            if end_date:
                df = df[df['time'] <= end_date]
            
            # Sort by time
            df = df.sort_values('time')
            
            return [
                HeatContentPoint(
                    time=row['time'],
                    lat=row['lat'],
                    lon=row['lon'],
                    heat_content=row['heat_content']
                )
                for _, row in df.iterrows()
                if not pd.isna(row['heat_content']) and row['heat_content'] != 0.0
            ]
            
        except Exception as e:
            logger.error(f"Error retrieving heat content: {e}")
            return []