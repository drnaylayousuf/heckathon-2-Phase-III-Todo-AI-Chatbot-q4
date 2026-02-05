# Todo App Backend for Hugging Face Spaces

This is the backend service for the Todo App with AI Chatbot, designed to run on Hugging Face Spaces.

## Configuration for Hugging Face Spaces

The backend is already configured to work with Hugging Face Spaces:

- **Entry Point**: `app.py` (in the root directory)
- **Dependencies**: Listed in `backend/requirements.txt`
- **Database**: Connected to Neon PostgreSQL database
- **CORS**: Configured to allow your Vercel frontend

## Required Environment Variables

Make sure to set these in your Hugging Face Space settings:

- `DATABASE_URL`: Your Neon PostgreSQL database URL
- `SECRET_KEY`: A secure secret key for JWT tokens
- `GEMINI_API_KEY`: Your Google Gemini API key

## Endpoints

- `GET /` - Root endpoint
- `GET /api/health` - Health check
- `GET /test` - Test endpoint
- `POST /api/register` - User registration
- `POST /api/login` - User login
- `GET /api/me` - Get current user info
- `GET/POST/PUT/DELETE /api/{user_id}/tasks` - Task management
- `POST /api/{user_id}/chat` - AI chat functionality

## Troubleshooting

If your space shows "Preparing Space" for a long time:

1. Check the Space logs for error messages
2. Verify your environment variables are set correctly
3. Ensure your Neon database is accessible
4. Check that all dependencies in requirements.txt are available