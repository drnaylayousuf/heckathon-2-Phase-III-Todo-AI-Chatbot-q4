# Hackathon Todo Web Application

This is a full-stack todo application with AI-powered chatbot capabilities featuring:
- **Frontend**: Next.js 16+, TypeScript, Tailwind CSS
- **Backend**: FastAPI, SQLModel, PostgreSQL
- **Authentication**: JWT-based with custom implementation
- **AI**: Google Gemini API for natural language task management

## Running Locally

### Backend Setup
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables by creating `.env`:
   ```
   DATABASE_URL=postgresql://username:password@host:port/database_name
   SECRET_KEY=your-super-secret-key-change-in-production
   GEMINI_API_KEY=your-gemini-api-key-here
   ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000,http://127.0.0.1:3000,http://127.0.0.1:8000
   ```

4. Run the development server:
   ```bash
   uvicorn app.main:app --reload
   ```
   The API will be available at http://localhost:8000

### Frontend Setup
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Set up environment variables by creating `.env.local`:
   ```
   NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8000
   ```

4. Run the development server:
   ```bash
   npm run dev
   ```
   The app will be available at http://localhost:3000

## Deploying to Hugging Face Spaces

The application is configured for Hugging Face Spaces deployment with a Dockerfile in the root directory.

### Important Configuration for Hugging Face:
1. Add the following environment variables in your Hugging Face Space settings:
   - `DATABASE_URL`: Your Neon PostgreSQL connection string
   - `SECRET_KEY`: A strong secret key for JWT tokens
   - `GEMINI_API_KEY`: Your Google Gemini API key (optional, but recommended)

2. The application will automatically use port 7860 when deployed to Hugging Face.

3. The Dockerfile is optimized for Hugging Face Spaces with proper database connection settings and startup procedures.

### Troubleshooting Hugging Face Deployment:
- If you see "Building..." for a long time, check the logs for:
  - Missing environment variables
  - Database connection issues
  - API key configuration
- Ensure your database connection string is properly formatted
- Verify that your API keys are correctly set in the Space settings
- The frontend will automatically detect the deployment environment and use the correct API URL

## Key Features
1. **Full-Stack Web Application**:
   - User authentication and authorization with JWT tokens
   - Complete task management (Create, Read, Update, Delete, Complete)
   - Responsive dashboard with filtering, sorting, and search

2. **AI-Powered Chatbot**:
   - Natural language processing for task management
   - Conversational AI using Google Gemini API
   - Direct task commands like "Add a task to buy groceries" or "Show my tasks"

3. **Production Ready**:
   - Proper logging and error handling
   - CORS configuration for frontend/backend separation
   - Database connection pooling
   - Rate limiting considerations

## Connection Handling
The application intelligently detects the environment and adjusts API calls accordingly:
- When running locally (`localhost`), it connects to `http://127.0.0.1:8000`
- When deployed to Hugging Face, it connects to the appropriate space URL
- Environment variables can override the default behavior
