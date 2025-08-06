# AI Development Specifications and Unit of Work

This directory contains specifications and guidelines intended to assist AI tools (like GitHub Copilot) in understanding the project architecture, conventions, and development plans.

## Documentation Structure

- [Project Overview](./project-overview.md) - High-level description of the project goals and architecture
- [Session Prompts](./session-prompts) - Breakdown of development phases into focused agent sessions
  - [Agent Session Templates](./session-prompts/agent-session-templates.md) - Templates for structuring agent sessions
  - [Stage 1 phased work outline](./session-prompts/stage1/stage1-phased-work-outline.md) - Overview of the first stage of development
  - [Stage 1 Sessions](./session-prompts/stage1) - Detailed prompts for the first stage of development
    - [Phase 1](./session-prompts/stage1/st1-phase-1.md) - Environment Setup and Server Foundation
    - [Phase 2](./session-prompts/stage1/st1-phase-2.md) - Core Tools Implementation with Integrated Error Handling
    - [Phase 3](./session-prompts/stage1/st1-phase-3.md) - MCP Inspector Testing and Debugging
    - [Phase 4](./session-prompts/stage1/st1-phase-4.md) - Real-World Integration Setup
    - [Phase 5](./session-prompts/stage1/st1-phase-5.md) - Documentation and Production Readiness

## How to Use These Docs

When working with AI assistants, reference these documents by mentioning them explicitly:

```text
Based on our project overview in docs/ai/project-overview.md, help me...
```
