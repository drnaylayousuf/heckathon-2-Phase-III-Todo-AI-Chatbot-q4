# Quickstart Guide: Hackathon Todo Application

## Prerequisites
- Node.js 18+ (for frontend)
- Python 3.9+ (for backend)
- PostgreSQL (or Docker for containerized setup)
- npm or yarn package manager

## Setup Instructions

### 1. Clone and Navigate
```bash
git clone <repository-url>
cd hackathon-todo
```

### 2. Backend Setup
```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
# Or if using Poetry: poetry install

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration

# Run the development server
uvicorn app.main:app --reload
```

Backend will be available at `http://localhost:8000`

### 3. Frontend Setup
```bash
# In a new terminal, navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Set up environment variables
cp .env.example .env.local
# Edit NEXT_PUBLIC_API_BASE_URL to point to your backend

# Run the development server
npm run dev
```

Frontend will be available at `http://localhost:3000`

## Environment Variables

### Backend (.env)
```env
DATABASE_URL=postgresql://username:password@localhost:5432/todo_db
SECRET_KEY=your-super-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Frontend (.env.local)
```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

## Running the Application

### Development
- Start backend: `uvicorn app.main:app --reload`
- Start frontend: `npm run dev`
- Visit `http://localhost:3000` to access the application

### Production
- Build frontend: `npm run build`
- Serve backend: `uvicorn app.main:app`

## Key Endpoints

### Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `GET /api/auth/me` - Get current user info

### Task Management
- `GET /api/{user_id}/tasks` - Get user's tasks
- `POST /api/{user_id}/tasks` - Create new task
- `PUT /api/{user_id}/tasks/{id}` - Update task
- `DELETE /api/{user_id}/tasks/{id}` - Delete task
- `PATCH /api/{user_id}/tasks/{id}/complete` - Toggle task completion

### AI Chatbot
- `POST /api/{user_id}/chat` - Process natural language commands

## Default Credentials
Upon first setup, register a new account using the UI or API.

## Troubleshooting

### Common Issues
1. **Port conflicts**: Change ports in configuration if 8000 or 3000 are in use
2. **Database connection**: Ensure PostgreSQL is running and credentials are correct
3. **Frontend can't connect to backend**: Check that NEXT_PUBLIC_API_BASE_URL is set correctly
4. **Styling issues**: Clear .next cache and restart dev server

### Useful Commands
```bash
# Run backend tests
cd backend && pytest

# Build frontend for production
cd frontend && npm run build

# Check frontend for errors
cd frontend && npm run lint
```

## Next Steps
1. Customize the UI in `frontend/app/components`
2. Extend the API in `backend/app/api/routers`
3. Add new features by following the existing patterns
4. Configure authentication providers if needed