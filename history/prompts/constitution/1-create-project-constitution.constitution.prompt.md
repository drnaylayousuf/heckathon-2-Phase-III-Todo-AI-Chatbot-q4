---
id: 1
title: "Create project constitution and specs"
stage: "constitution"
date: "2026-01-20"
surface: "agent"
model: "Claude Sonnet 4.5"
feature: "none"
branch: "master"
user: "user"
command: "/sp.constitution"
labels: ["constitution", "specs", "setup"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - ".specify/memory/constitution.md"
  - "specs/overview.md"
  - "specs/architecture.md"
  - "specs/features/task-crud.md"
  - "specs/features/authentication.md"
  - "specs/features/chatbot.md"
  - "specs/api/rest-endpoints.md"
  - "specs/api/mcp-tools.md"
  - "specs/database/schema.md"
  - "specs/ui/components.md"
  - "specs/ui/pages.md"
  - "README.md"
tests: []
---

# Prompt
```
You are Claude Code acting as a senior AI system architect and product engineer.

Your task is to fully design and implement **Phase II and Phase III of the Hackathon II: Evolution of Todo** using **strict Spec-Driven Development** with **Spec-Kit Plus**.

🚫 You must NOT ask me to write code manually.
✅ You must iteratively refine and follow specifications until the implementation is correct.
✅ You must generate production-quality code, UI, and architecture.

────────────────────────────────────────
📌 GLOBAL RULES
────────────────────────────────────────
1. You MUST read and follow:
   - Root `CLAUDE.md`
   - `.spec-kit/config.yaml`
   - All specs inside `/specs`
2. If a required spec does not exist, CREATE it first before coding.
3. Implementation must strictly follow the specs.
4. All UI must be modern, clean, responsive, and visually polished.
5. Use Tailwind CSS for styling.
6. Use accessible UX patterns (loading states, empty states, error states).
7. Ensure the app is fully functional end-to-end.

────────────────────────────────────────
🎯 TARGET PHASES
────────────────────────────────────────

## Phase II – Full-Stack Web Application
## Phase III – AI-Powered Todo Chatbot

────────────────────────────────────────
🧱 REQUIRED MONOREPO STRUCTURE
────────────────────────────────────────
hackathon-todo/
├── .spec-kit/
├── specs/
│   ├── overview.md
│   ├── architecture.md
│   ├── features/
│   │   ├── task-crud.md
│   │   ├── authentication.md
│   │   ├── chatbot.md
│   ├── api/
│   │   ├── rest-endpoints.md
│   │   ├── mcp-tools.md
│   ├── database/
│   │   └── schema.md
│   ├── ui/
│   │   ├── components.md
│   │   ├── pages.md
├── frontend/
├── backend/
├── README.md
├── CLAUDE.md

────────────────────────────────────────
🧠 PHASE II REQUIREMENTS (FULLY IMPLEMENT)
────────────────────────────────────────

### Backend (FastAPI)
- JWT authentication via Better Auth
- SQLModel ORM
- Neon Serverless PostgreSQL
- Secure REST API:
  - GET /api/{user_id}/tasks
  - POST /api/{user_id}/tasks
  - PUT /api/{user_id}/tasks/{id}
  - DELETE /api/{user_id}/tasks/{id}
  - PATCH /api/{user_id}/tasks/{id}/complete
- Middleware to:
  - Verify JWT
  - Enforce user isolation
- Clean project structure
- Proper error handling
- Database migrations

### Frontend (Next.js App Router)
- Next.js 16+
- TypeScript
- Tailwind CSS
- Better Auth integration
- JWT attached to all API requests
- Pages:
  - Login
  - Register
  - Dashboard
- Dashboard Features:
  - Add / edit / delete todos
  - Mark complete
  - Search
  - Filter (status, priority)
  - Sort (date, priority, title)
- UI/UX:
  - Clean modern SaaS design
  - Mobile-responsive
  - Empty state UI
  - Loading skeletons
  - Toast notifications

────────────────────────────────────────
🤖 PHASE III REQUIREMENTS (FULLY IMPLEMENT)
────────────────────────────────────────

### AI Chatbot
- OpenAI ChatKit frontend
- Stateless chat backend
- OpenAI Agents SDK
- Official MCP SDK
- Database-backed conversation memory

### MCP Tools (STRICT)
- add_task
- list_tasks
- update_task
- delete_task
- complete_task

### Chat Behavior
- Natural language understanding:
  - “Add a task to buy groceries”
  - “What’s pending?”
  - “Mark task 3 complete”
  - “Delete the meeting task”
- Agent must:
  - Select correct MCP tool
  - Chain tools if needed
  - Confirm actions
  - Handle errors gracefully

### Chat Endpoint
POST /api/{user_id}/chat
- Stateless
- Conversation stored in DB
- Resumable after restart

────────────────────────────────────────
🎨 UI / UX REQUIREMENTS (VERY IMPORTANT)
────────────────────────────────────────
- Professional SaaS-grade UI
- Tailwind-based design system
- Consistent spacing & typography
- Chat UI similar to modern AI apps
- Smooth animations & transitions
- Dark mode support (optional bonus)

────────────────────────────────────────
📚 SPEC-FIRST WORKFLOW (MANDATORY)
────────────────────────────────────────
1. Review existing specs
2. Create missing specs
3. Validate specs completeness
4. Implement backend
5. Implement frontend
6. Implement chatbot + MCP
7. Verify everything works together
8. Fix spec mismatches if needed

────────────────────────────────────────
📦 FINAL OUTPUT EXPECTATIONS
────────────────────────────────────────
- Fully working Phase II & III
- Clean GitHub-ready repository
- Production-ready UI
- AI chatbot managing todos via MCP
- Stateless backend
- Spec-driven history preserved

🚀 Begin by reviewing specs and creating any missing ones before implementation.
```

# Response
Created the project constitution and all required specification files following the user's requirements for the Hackathon Todo project. The constitution establishes core principles for Spec-Driven Development, production-quality code, full-stack integration, modern UI/UX, AI-first architecture, and security-first approach.

Specifications created include:
- Project overview and architecture
- Feature specs for task CRUD, authentication, and chatbot
- API specs for REST endpoints and MCP tools
- Database schema specification
- UI component and page specifications

All specifications follow the strict Spec-Driven Development methodology as required, providing a solid foundation for implementing both Phase II (Full-Stack Web Application) and Phase III (AI-Powered Todo Chatbot).