# MCP Tools Specification

## Overview
MCP (Model Context Protocol) tools provide the interface between the AI chatbot and the backend task management system.

## Available Tools

### add_task
- **Purpose**: Create a new task
- **Input Parameters**:
  - `title` (string, required): Task title
  - `description` (string, optional): Task description
  - `priority` (string, optional): Priority level ('low', 'medium', 'high')
  - `dueDate` (string, optional): Due date in ISO 8601 format
- **Returns**: Task object with ID and creation timestamp
- **Errors**: Invalid input, authentication failure

### list_tasks
- **Purpose**: Retrieve all tasks for the authenticated user
- **Input Parameters**:
  - `status` (string, optional): Filter by status ('pending', 'in-progress', 'completed')
  - `priority` (string, optional): Filter by priority ('low', 'medium', 'high')
  - `sortBy` (string, optional): Sort by field ('title', 'dueDate', 'priority', 'createdAt')
  - `order` (string, optional): Sort order ('asc', 'desc')
- **Returns**: Array of task objects
- **Errors**: Authentication failure

### update_task
- **Purpose**: Update an existing task
- **Input Parameters**:
  - `taskId` (string, required): ID of the task to update
  - `title` (string, optional): New task title
  - `description` (string, optional): New task description
  - `priority` (string, optional): New priority level
  - `dueDate` (string, optional): New due date
  - `status` (string, optional): New status
- **Returns**: Updated task object
- **Errors**: Task not found, invalid input, authentication failure

### delete_task
- **Purpose**: Delete a specific task
- **Input Parameters**:
  - `taskId` (string, required): ID of the task to delete
- **Returns**: Success confirmation
- **Errors**: Task not found, authentication failure

### complete_task
- **Purpose**: Mark a task as completed or incomplete
- **Input Parameters**:
  - `taskId` (string, required): ID of the task to update
  - `completed` (boolean, required): Completion status
- **Returns**: Updated task object
- **Errors**: Task not found, authentication failure

## Error Handling
- Authentication failures return appropriate error codes
- Invalid parameters return validation errors
- Resource not found returns 404 equivalent
- All errors include descriptive messages

## Security Requirements
- All tools require authentication context
- User isolation enforced for all operations
- Input validation on all parameters
- Proper error masking to prevent information disclosure