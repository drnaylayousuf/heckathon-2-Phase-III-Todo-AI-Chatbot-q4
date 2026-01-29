---
id: 5
title: "Task generation"
stage: "tasks"
date: "2026-01-20"
surface: "agent"
model: "Claude Sonnet 4.5"
feature: "evolve-todo-app"
branch: "master"
user: "user"
command: "/sp.tasks"
labels: ["tasks", "planning", "implementation"]
links:
  spec: "../../specs/001-evolve-todo-app/spec.md"
  plan: "../../specs/master/plan.md"
  ticket: null
  adr: null
  pr: null
files:
  - "specs/001-evolve-todo-app/tasks.md"
tests: []
---

# Prompt
```
Perfect — this is the FINAL "FULL TASK PROMPT" that sits above /sp.specify, /sp.plan, and /sp.execute, aligned with:

✅ Constitution (global rules + authority)

✅ Spec-Driven Development

✅ Your Phase II + Phase III scope

✅ UI/UX + Tailwind enforcement

✅ Spec-Kit Plus + Claude Code best practices

This is the one prompt you use when you want Claude Code to understand the entire mission end-to-end.

🧠 FULL TASK PROMPT

(Constitution → Specify → Plan → Execute)

Paste this once at the start of your Claude Code session
Then you will run /sp.specify, /sp.plan, /sp.execute sequentially

FULL TASK PROMPT — HACKATHON TODO (PHASE II + III)

You are Claude Code, operating under Spec-Kit Plus, bound by the following CONSTITUTION, SPECIFICATION RULES, and EXECUTION DISCIPLINE.

You are acting simultaneously as:

Senior System Architect

Senior Frontend Engineer (Next.js + Tailwind)

Senior Backend Engineer (FastAPI + SQLModel)

AI Agent Engineer (OpenAI Agents SDK + MCP)

Product Designer (SaaS-grade UI/UX)

Your mission is to fully design, specify, plan, and implement:

Hackathon II: Evolution of Todo — Phase II & Phase III

🏛️ CONSTITUTION (ABSOLUTE LAW)

Spec-Driven Development is mandatory

Specs are the source of truth

Code must follow specs, never the opposite

No manual coding by the user

No assumptions outside specs

If something is missing → create or update a spec

If something conflicts → fix the spec first

UI/UX quality is non-negotiable

Tailwind misconfiguration blocks all progress

Violation of any constitutional rule is a failure.

📚 AUTHORITATIVE DOCUMENTS (READ FIRST)

You MUST read and obey:

CLAUDE.md

.spec-kit/config.yaml

ALL files inside /specs, including:

/specs/ui/styling.md (CRITICAL)

🎯 PROJECT SCOPE (LOCKED)
Phase II — Full-Stack Web Application

FastAPI backend

JWT auth (Better Auth)

SQLModel + Neon PostgreSQL

Secure REST API

Next.js 16 App Router frontend

Tailwind CSS

SaaS-grade dashboard UI

Phase III — AI-Powered Todo Chatbot

OpenAI Agents SDK

Official MCP SDK

Stateless chat backend

Database-backed conversation memory

MCP tools controlling todos

No scope creep. No partial delivery.

🎨 UI / UX & TAILWIND CONSTITUTION (BLOCKING)

You MUST enforce ALL of the following:

✅ Create postcss.config.js with Tailwind plugin

✅ Configure tailwind.config.ts

✅ Tailwind content paths include:

app/**

components/**

lib/**

frontend/**

✅ Import CSS ONLY in app/layout.tsx

✅ Define ALL custom CSS in globals.css

✅ Clear .next cache if styles don’t apply

✅ Use "use client" for:

interactive components

dynamic styling

animations

❌ No inline styles
❌ No CSS imports in components
❌ No unstyled or broken UI

If Tailwind is not working, you MUST stop and fix it.

🧩 MCP & AI AGENT LAW

AI must ONLY act via MCP tools

AI must NEVER hallucinate

AI must confirm actions

AI must handle ambiguity

Stateless execution is mandatory

MCP tools are authoritative over all task state.

🧭 REQUIRED WORKFLOW (STRICT ORDER)

You MUST follow this lifecycle exactly:

1️⃣ /sp.specify

Validate all existing specs

Create missing specs

Update conflicting specs

Lock scope and behavior

2️⃣ /sp.plan

Produce a detailed execution plan

Include UI/Tailwind initialization FIRST

No code allowed

3️⃣ /sp.execute

Implement strictly according to specs + plan

Backend → Frontend → Chatbot → Integration

Fix issues by updating specs if needed

Skipping a step is forbidden.

📦 FINAL ACCEPTANCE CRITERIA

You are finished ONLY when:

✅ Phase II fully works end-to-end

✅ Phase III chatbot manages todos correctly

✅ MCP tools are used correctly

✅ UI matches SaaS quality bar

✅ Tailwind rules are enforced

✅ App is hackathon-ready

✅ Specs reflect reality
```

# Response
Generated comprehensive task list for implementing the Hackathon Todo application following the specified phases:

- Phase 1: Setup tasks for project initialization
- Phase 2: Foundational tasks including Tailwind CSS configuration, database models, and API schemas
- Phase 3: US1 - User Authentication and Task Management (P1 priority)
- Phase 4: US2 - AI-Powered Task Management via Chat (P2 priority)
- Phase 5: US3 - Polished UI/UX with Tailwind Styling (P3 priority)
- Phase 6: Integration & Verification

The tasks are organized by user story to enable independent implementation and testing. Each task follows the required checklist format with sequential IDs, story labels where appropriate, and specific file paths. The implementation strategy focuses on delivering an MVP with US1 functionality first, followed by incremental additions of US2 and US3 features.

The task list includes 79 specific implementation tasks across all phases of the project, with dependencies clearly defined between user stories and parallel execution opportunities identified.