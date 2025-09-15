"""
Pydantic models for API request/response serialization.

Defines the data structures used for API communication between 
frontend and backend components.
"""

from pydantic import BaseModel, Field
from datetime import datetime, date
from typing import List, Optional, Dict, Any
from enum import Enum


class HealthResponse(BaseModel):
    """Health check response model."""
    status: str = Field(..., description="Service status")
    timestamp: datetime = Field(..., description="Response timestamp")
    version: str = Field(..., description="API version")


class DataSummaryResponse(BaseModel):
    """Data summary statistics response."""
    total_records: int = Field(..., description="Total number of data records")
    date_range: Dict[str, str] = Field(..., description="Min and max dates in dataset")
    spatial_coverage: Dict[str, Dict[str, float]] = Field(..., description="Latitude and longitude ranges")
    data_types: List[str] = Field(..., description="Available data types")
    measurement_counts: Dict[str, int] = Field(..., description="Count by measurement type")


class TimeSeriesPoint(BaseModel):
    """Single point in a time series."""
    time: datetime = Field(..., description="Measurement timestamp")
    temperature: Optional[float] = Field(None, description="Temperature in °C")
    salinity: Optional[float] = Field(None, description="Salinity in PSU")
    depth: Optional[float] = Field(None, description="Depth in meters")


class VerticalProfilePoint(BaseModel):
    """Single point in a vertical profile."""
    depth: float = Field(..., description="Depth in meters")
    temperature: Optional[float] = Field(None, description="Temperature in °C")
    salinity: Optional[float] = Field(None, description="Salinity in PSU")
    date: date = Field(..., description="Profile date")


class HeatContentPoint(BaseModel):
    """Heat content measurement point."""
    time: datetime = Field(..., description="Measurement timestamp")
    lat: float = Field(..., description="Latitude")
    lon: float = Field(..., description="Longitude") 
    heat_content: float = Field(..., description="Heat content value")


class ChatRequest(BaseModel):
    """Chat interface request."""
    message: str = Field(..., description="User query or question")
    context: Optional[Dict[str, Any]] = Field(None, description="Additional context")


class ChatResponse(BaseModel):
    """Chat interface response."""
    response: str = Field(..., description="AI-generated response")
    timestamp: datetime = Field(..., description="Response timestamp")
    sources: Optional[List[str]] = Field(None, description="Data sources used in response")
    confidence: Optional[float] = Field(None, description="Response confidence score")


class FloatLocation(BaseModel):
    """ARGO float location information."""
    float_id: str = Field(..., description="Float identifier")
    lat: float = Field(..., description="Current latitude")
    lon: float = Field(..., description="Current longitude")
    last_transmission: datetime = Field(..., description="Last data transmission")
    status: str = Field(..., description="Float operational status")


class DataFilter(BaseModel):
    """Data filtering parameters."""
    lat_range: Optional[Dict[str, float]] = Field(None, description="Latitude range filter")
    lon_range: Optional[Dict[str, float]] = Field(None, description="Longitude range filter")
    date_range: Optional[Dict[str, str]] = Field(None, description="Date range filter")
    depth_range: Optional[Dict[str, float]] = Field(None, description="Depth range filter")
    parameters: Optional[List[str]] = Field(None, description="Specific parameters to retrieve")


class NetCDFIngestRequest(BaseModel):
    """NetCDF file ingestion request."""
    file_path: str = Field(..., description="Path to NetCDF file")
    float_id: Optional[str] = Field(None, description="Associated float ID")
    overwrite_existing: bool = Field(False, description="Whether to overwrite existing data")
    validation_level: str = Field("strict", description="Data validation level")


class NetCDFIngestResponse(BaseModel):
    """NetCDF file ingestion response."""
    status: str = Field(..., description="Ingestion status")
    records_processed: int = Field(..., description="Number of records processed")
    errors: List[str] = Field(default_factory=list, description="Processing errors")
    summary: Dict[str, Any] = Field(..., description="Ingestion summary")