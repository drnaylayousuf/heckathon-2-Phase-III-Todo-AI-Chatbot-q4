# REST API Endpoints Specification

## Overview
The REST API provides secure endpoints for all task management operations with JWT-based authentication and user isolation.

## Authentication Endpoints
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User authentication
- `POST /api/auth/logout` - Session termination
- `GET /api/auth/me` - Current user information

## Task Management Endpoints

### All Endpoints Require JWT Authentication
All task endpoints require a valid JWT token in the Authorization header: `Authorization: Bearer <token>`

### User-Specific Endpoints
All endpoints enforce user isolation through middleware that extracts user ID from JWT token.

- `GET /api/{user_id}/tasks` - Retrieve all tasks for authenticated user
  - Query parameters: `status`, `priority`, `sort`, `search`
  - Response: Array of task objects

- `POST /api/{user_id}/tasks` - Create a new task for authenticated user
  - Request body: `{title: string, description?: string, priority?: 'low'|'medium'|'high', dueDate?: string}`
  - Response: Created task object with ID and timestamps

- `PUT /api/{user_id}/tasks/{id}` - Update an existing task
  - Request body: Partial task object with fields to update
  - Response: Updated task object

- `DELETE /api/{user_id}/tasks/{id}` - Delete a specific task
  - Response: Success confirmation

- `PATCH /api/{user_id}/tasks/{id}/complete` - Mark task as complete/incomplete
  - Request body: `{completed: boolean}`
  - Response: Updated task object

## Chat Endpoint
- `POST /api/{user_id}/chat` - Process natural language chat request
  - Request body: `{message: string}`
  - Response: `{response: string, conversationId: string}`

## Error Responses
All endpoints return standardized error responses:
- `400 Bad Request`: Invalid input data
- `401 Unauthorized`: Missing or invalid JWT token
- `403 Forbidden`: User attempting to access another user's data
- `404 Not Found`: Requested resource doesn't exist
- `500 Internal Server Error`: Unexpected server error

## Request/Response Format
- Content-Type: `application/json`
- All dates in ISO 8601 format
- All responses follow consistent structure