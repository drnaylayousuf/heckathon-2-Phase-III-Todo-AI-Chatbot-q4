# Hackathon Todo - Architecture Specification

## System Overview
The application follows a modern full-stack architecture with separate backend and frontend services, integrated with AI capabilities through OpenAI Agents and MCP tools.

## Component Architecture

### Backend Service
- **Framework**: FastAPI for high-performance API development
- **ORM**: SQLModel for database operations
- **Database**: Neon Serverless PostgreSQL for scalability
- **Authentication**: Better Auth with JWT tokens
- **API Layer**: RESTful endpoints with proper authentication middleware

### Frontend Service
- **Framework**: Next.js 16+ with App Router
- **Language**: TypeScript for type safety
- **Styling**: Tailwind CSS for responsive design
- **Authentication**: Better Auth integration
- **State Management**: Client-side state with proper error handling

### AI Chatbot Service
- **Framework**: OpenAI Agents SDK
- **Communication**: MCP tools for task operations
- **Memory**: Database-backed conversation storage
- **Interface**: Natural language processing for task management

## Data Flow Architecture
1. User authenticates via Better Auth
2. JWT token is passed with all API requests
3. Frontend communicates with backend via REST API
4. AI chatbot uses MCP tools to manipulate tasks
5. All operations are secured with user isolation

## Security Architecture
- JWT-based authentication and authorization
- User data isolation through middleware
- Input validation and sanitization
- Secure API endpoint access controls