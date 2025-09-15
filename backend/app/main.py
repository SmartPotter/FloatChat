"""
FloatChat FastAPI Application

Main application entry point for the ARGO float data API service.
Provides endpoints for data retrieval, analysis, and conversational AI interface.
"""

from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import List, Optional, Dict, Any
import pandas as pd
import os
from datetime import datetime, date
import logging

from .models.database import get_db, SessionLocal
from .models.schemas import (
    HealthResponse, DataSummaryResponse, TimeSeriesPoint,
    VerticalProfilePoint, HeatContentPoint, ChatRequest, ChatResponse
)
from .services.data_service import DataService
from .llm.llm_service import LLMService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="FloatChat API",
    description="AI-powered ARGO float data exploration API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://frontend:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
data_service = DataService()
llm_service = LLMService()


@app.get("/api/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint to verify API availability."""
    return HealthResponse(
        status="ok",
        timestamp=datetime.now(),
        version="1.0.0"
    )


@app.get("/api/data-summary", response_model=DataSummaryResponse)
async def get_data_summary():
    """
    Get summary statistics and metadata about the available dataset.
    Returns data counts, time ranges, and spatial coverage.
    """
    try:
        summary = await data_service.get_data_summary()
        return summary
    except Exception as e:
        logger.error(f"Error getting data summary: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve data summary")


@app.get("/api/surface-timeseries", response_model=List[TimeSeriesPoint])
async def get_surface_timeseries(
    lat: float = Query(..., description="Latitude coordinate"),
    lon: float = Query(..., description="Longitude coordinate"), 
    start: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    depth: Optional[float] = Query(None, description="Depth filter in meters")
):
    """
    Retrieve surface or depth-specific time series data for a location.
    Returns temperature and salinity measurements over time.
    """
    try:
        # Parse date parameters
        start_date = datetime.fromisoformat(start) if start else None
        end_date = datetime.fromisoformat(end) if end else None
        
        timeseries = await data_service.get_surface_timeseries(
            lat=lat, lon=lon, start_date=start_date, end_date=end_date, depth=depth
        )
        return timeseries
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid date format: {e}")
    except Exception as e:
        logger.error(f"Error getting surface timeseries: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve timeseries data")


@app.get("/api/vertical-profile", response_model=List[VerticalProfilePoint])
async def get_vertical_profile(
    lat: float = Query(..., description="Latitude coordinate"),
    lon: float = Query(..., description="Longitude coordinate"),
    date: str = Query(..., description="Date (YYYY-MM-DD)")
):
    """
    Get vertical profile data (temperature and salinity by depth) for a specific location and date.
    """
    try:
        profile_date = datetime.fromisoformat(date).date()
        profile = await data_service.get_vertical_profile(lat=lat, lon=lon, date=profile_date)
        return profile
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid date format: {e}")
    except Exception as e:
        logger.error(f"Error getting vertical profile: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve profile data")


@app.get("/api/heat-content", response_model=List[HeatContentPoint])
async def get_heat_content(
    lat: float = Query(..., description="Latitude coordinate"),
    lon: float = Query(..., description="Longitude coordinate"),
    start: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end: Optional[str] = Query(None, description="End date (YYYY-MM-DD)")
):
    """
    Retrieve heat content time series for a specific location.
    Heat content represents the thermal energy stored in the water column.
    """
    try:
        start_date = datetime.fromisoformat(start) if start else None
        end_date = datetime.fromisoformat(end) if end else None
        
        heat_content = await data_service.get_heat_content(
            lat=lat, lon=lon, start_date=start_date, end_date=end_date
        )
        return heat_content
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid date format: {e}")
    except Exception as e:
        logger.error(f"Error getting heat content: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve heat content data")


@app.post("/api/chat", response_model=ChatResponse)
async def chat_with_data(request: ChatRequest):
    """
    Conversational AI interface for querying and analyzing ARGO float data.
    Uses RAG (Retrieval Augmented Generation) to provide context-aware responses.
    """
    try:
        response = await llm_service.answer_query(request.message)
        return ChatResponse(
            response=response,
            timestamp=datetime.now()
        )
    except Exception as e:
        logger.error(f"Error in chat interface: {e}")
        raise HTTPException(status_code=500, detail="Failed to process chat request")


@app.post("/api/ingest-netcdf")
async def ingest_netcdf_data():
    """
    Stub endpoint for NetCDF data ingestion.
    
    TODO: Implement file upload handling and NetCDF processing.
    This endpoint will handle:
    1. File upload validation
    2. NetCDF parsing with xarray
    3. Data transformation and validation
    4. Database/Parquet storage
    5. Metadata indexing for retrieval
    """
    # This is a placeholder implementation
    return JSONResponse(
        content={
            "status": "not_implemented", 
            "message": "NetCDF ingestion pipeline not yet implemented. See backend/ingest/netcdf_to_parquet.py for implementation scaffold."
        },
        status_code=501
    )


# Error handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={"detail": "Endpoint not found"}
    )


@app.exception_handler(500)
async def internal_error_handler(request, exc):
    logger.error(f"Internal server error: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)