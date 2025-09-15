# FloatChat - ARGO Float Data Explorer

A production-ready AI-powered conversational interface and dashboard for ARGO float data (Indian Ocean PoC).

## Project Structure

```
floatchat/
├── frontend/           # Next.js frontend application
├── backend/           # FastAPI backend application
├── docker-compose.yml # Docker setup for development
└── README.md         # This file
```

## Quick Start

### Prerequisites
- Node.js 18+ and npm
- Python 3.9+
- Docker (optional)

### Setup

1. **Install Dependencies**
```bash
# Frontend
cd frontend && npm install

# Backend
cd ../backend && pip install -r requirements.txt
```

2. **Environment Configuration**
```bash
# Copy example environment files
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env.local
```

3. **Seed Data Setup**
Place the provided CSV files in `backend/seed_data/`:
- `heat_content.csv`
- `monthly_averages.csv` 
- `surface_timeseries.csv`

4. **Run the Application**

Option A - Development servers:
```bash
# Terminal 1: Backend
cd backend && uvicorn app.main:app --reload --port 8000

# Terminal 2: Frontend  
cd frontend && npm run dev
```

Option B - Docker:
```bash
docker-compose up -d
```

## Demo Chat Prompts

1. **"What is the average temperature at 60°E longitude in 2012?"**
   - Expected: Analysis of temperature data for that location and time period

2. **"How does heat content vary between 60°E and 80°E?"**  
   - Expected: Comparison of heat content values across longitudes

3. **"Show me the salinity trends in the surface waters"**
   - Expected: Analysis of surface salinity patterns over time

## Development

### Frontend Structure
- `/dashboard` - Interactive map and charts
- `/chat` - Conversational AI interface  
- Reusable components for charts and data visualization

### Backend Structure
- `/api/health` - Service health check
- `/api/data-summary` - Dataset overview statistics
- `/api/surface-timeseries` - Time series data queries
- `/api/vertical-profile` - Depth profile data
- `/api/heat-content` - Heat content time series
- `/api/chat` - AI chat interface
- `/api/ingest-netcdf` - NetCDF ingestion stub

### Adding NetCDF Support

The NetCDF ingestion pipeline is scaffolded in `backend/ingest/netcdf_to_parquet.py`. 
Key TODOs for implementation:

1. Replace xarray pseudocode with actual NetCDF parsing
2. Implement Parquet/database storage logic
3. Add proper error handling and validation
4. Configure file upload endpoints

### LLM Configuration

Set environment variables in `backend/.env`:
- `OPENAI_API_KEY` - For OpenAI GPT integration
- `EMBED_MODEL` - Embedding model selection
- `VECTOR_DB_PATH` - Vector database storage path

Without OpenAI key, the system falls back to deterministic responses based on retrieved data context.

## Architecture Notes

- **Frontend**: Next.js 14 with App Router, TypeScript, Tailwind CSS
- **Backend**: FastAPI with SQLAlchemy, Pydantic models
- **Database**: PostgreSQL (with CSV fallback for development)
- **Maps**: Leaflet integration for interactive visualization
- **Charts**: Recharts for time series and profile visualization
- **AI**: RAG pipeline with Chroma vector store and OpenAI integration

## Contributing

1. Follow the existing code structure and naming conventions
2. Add tests for new features
3. Update documentation for API changes
4. Use TypeScript for all frontend code
5. Follow Python typing hints in backend code

## License

MIT License - see LICENSE file for details.