# AGENT.md - Fragfrag Perfume Recognition API

## Project Overview
FastAPI-based perfume recognition system that uses Google Gemini AI to identify perfume bottles from images.

## Architecture
- **Framework**: FastAPI with Python 3.12
- **AI Service**: Google Gemini 1.5 Flash for image analysis
- **Database**: Supabase (configured but not actively used)
- **File Structure**: Standard FastAPI layout with separation of concerns

## Key Components

### Core Files
- `app/main.py` - FastAPI application entry point
- `app/core/config.py` - Environment settings management
- `app/api/router.py` - API routing configuration
- `app/api/routes/perfumes.py` - Perfume identification endpoints

### Services
- `app/services/recognition.py` - Primary Gemini AI integration
- `app/services/vision.py` - Alternative vision service (duplicate functionality)
- `app/services/supabase.py` - Database service (configured)

## API Endpoints
- `POST /api/v1/perfumes/identify` - Upload image for perfume recognition
- `GET /api/v1/perfumes/{perfume_id}` - Get perfume metadata
- `GET /` - Health check endpoint

## Environment Variables
Required in `.env` file:
- `SUPABASE_URL` - Supabase database URL
- `SUPABASE_KEY` - Supabase API key
- `AI_API_KEY` - Google Gemini API key

## Development Commands
```bash
# Start development server
uvicorn app.main:app --reload

# Run tests (when implemented)
pytest

# Install dependencies
pip install -r requirements.txt
```

## Code Conventions
- Spanish comments and error messages
- Async/await pattern throughout
- Pydantic for settings management
- FastAPI dependency injection

## Current Issues
- Duplicate vision services (`recognition.py` and `vision.py`)
- Missing requirements.txt content
- Supabase integration not fully implemented
- No test coverage

## Future Enhancements
- Bottle recognition expansion beyond perfumes
- Database integration for perfume metadata
- Image preprocessing and optimization
- API rate limiting and authentication