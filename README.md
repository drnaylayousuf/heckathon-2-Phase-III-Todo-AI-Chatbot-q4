# Hackathon Todo - AI-Powered Task Management

A full-stack todo application with AI-powered chatbot capabilities that allows users to manage their tasks through both a traditional web interface and natural language interactions.

## 🚀 Features

- **Full-Stack Web Application** (Phase II)
  - User authentication and authorization with JWT tokens
  - Complete task management (Create, Read, Update, Delete, Complete)
  - Responsive dashboard with filtering, sorting, and search
  - Modern UI with Tailwind CSS

- **AI-Powered Chatbot** (Phase III)
  - Natural language processing for task management
  - MCP tools integration for backend operations
  - Conversational AI using OpenAI Agents SDK

## 🏗️ Architecture

### Tech Stack
- **Frontend**: Next.js 16+, TypeScript, Tailwind CSS
- **Backend**: FastAPI, SQLModel, PostgreSQL
- **Authentication**: JWT-based with custom implementation
- **AI**: OpenAI Agents SDK, MCP SDK
- **Styling**: Tailwind CSS with responsive design

## 🛠️ Development Setup

### Backend Setup
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Install dependencies (requires Python 3.9+):
   ```bash
   pip install -r requirements.txt
   ```

   Or if using Poetry:
   ```bash
   poetry install
   ```

3. Run the development server:
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

3. Run the development server:
   ```bash
   npm run dev
   ```

   The app will be available at http://localhost:3000

## 📋 Specifications

All development follows strict Spec-Driven Development methodology. See the `specs/` directory for complete documentation of:

- System architecture and component design
- Feature requirements and functionality
- API endpoints and data models
- Database schema and relationships
- UI components and page layouts
- MCP tools and AI integration

## 🎯 Target Phases

- **Phase II**: Full-Stack Web Application with authentication and authorization
- **Phase III**: AI-Powered Todo Chatbot with MCP tools integration

## 📁 Environment Variables

### Backend
Create a `.env` file in the backend directory:
```
DATABASE_URL=sqlite:///./todo_app.db  # Or your PostgreSQL connection string
SECRET_KEY=your-super-secret-key-change-in-production
```

### Frontend
Create a `.env.local` file in the frontend directory:
```
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

## 🧪 Testing

### Backend Tests
Run the backend tests:
```bash
cd backend
pytest
```

## 🚀 Deployment

Both frontend and backend applications can be deployed separately:

- **Frontend**: Deploy to Vercel, Netlify, or similar platforms
- **Backend**: Deploy to Heroku, Railway, or similar platforms supporting FastAPI

## 🤝 Contributing

This project follows the Spec-Driven Development methodology. All contributions should:

1. Follow the specifications in the `specs/` directory
2. Maintain the architecture and design patterns established
3. Include appropriate tests for new functionality
4. Follow the styling guidelines (Tailwind CSS)

## 📄 License

This project follows the constitution and guidelines defined in `.specify/memory/constitution.md`.

## 🎯 Implementation Status

✅ **Phase II**: Full-Stack Web Application - COMPLETE
- User authentication and registration
- Task CRUD operations
- Responsive dashboard UI
- API endpoints with JWT authentication

✅ **Phase III**: AI-Powered Chatbot - COMPLETE
- Natural language processing for task management
- MCP tools integration
- Conversational interface
- Backend persistence