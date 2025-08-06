### Foundation Session Template

Below is a template for a foundational session prompts that sets up the groundwork for a project. It helps in defining the high-level goals, current context, and specific deliverables needed to kickstart development.
This template can be used by AI agents to scaffold together focused session prompts on an already defined scope of work, broken down into phases.

---

# PROJECT FOUNDATION SESSION

## High-Level Goal

[Describe what you're trying to achieve, not what you're trying to build]

## Current Context

- Project type: [web app/mobile app/API/library/tool]
- Technology stack: [primary languages/frameworks]
- Development stage: [greenfield/existing codebase/refactoring]
- Team size: [solo/small team/large team]

## Session Scope

Create foundational architecture and core utilities for [specific area]

## Specific Deliverables

1. [Component/module name] - [specific responsibility]
2. [Component/module name] - [specific responsibility]
3. Basic project structure and configuration
4. Initial test framework setup

## Constraints

- Follow [architectural pattern] approach
- Maintain compatibility with [existing systems]
- Implement [specific design principles]
- Use [coding standards/style guides]

## Success Criteria

- [ ] All components have single, clear responsibilities
- [ ] Basic tests pass for new components
- [ ] Project structure follows established conventions
- [ ] Documentation exists for new components

## Open Questions

- [List any unresolved decisions or concerns]

What questions do you have before we get started?

---

### Feature Development Session Template

---

# FEATURE DEVELOPMENT SESSION

## Feature Overview

Implement [feature name] that enables users to [user capability]

## User Story Context

As a [user type], I want to [action] so that [benefit]

## Technical Scope

- Modify/create: [specific files or modules]
- Integrate with: [existing systems/APIs]
- Data requirements: [storage/processing needs]
- UI/UX requirements: [interface specifications]

## Implementation Strategy

1. [Core logic/business rules]
2. [Data layer changes]
3. [API/service integration]
4. [User interface components]
5. [Testing and validation]

## Dependencies

- Requires completion of: [previous features/components]
- Assumes availability of: [external services/data]
- Must coordinate with: [other development work]

## Non-Functional Requirements

- Performance: [specific metrics or constraints]
- Security: [authentication/authorization needs]
- Scalability: [expected load/growth]
- Accessibility: [compliance requirements]

## Definition of Done

- [ ] Feature works as specified in user story
- [ ] All edge cases handled appropriately
- [ ] Unit and integration tests pass
- [ ] Performance meets specified criteria
- [ ] Documentation updated
- [ ] Security review completed (if applicable)

## Open Questions

- [List any unresolved decisions or concerns]

What questions do you have about the implementation approach?

---

### Refactoring Session Template

---

# REFACTORING SESSION

## Refactoring Objective

Improve [specific aspect] of [component/system] to [desired outcome]

## Current Pain Points

- [Specific problem 1]: [impact on development/users]
- [Specific problem 2]: [impact on development/users]
- [Specific problem 3]: [impact on development/users]

## Target Architecture

- Extract [functionality] into [new component] for [reason]
- Consolidate [scattered logic] into [unified approach] for [benefit]
- Replace [current approach] with [new pattern] to achieve [goal]

## Safety Constraints

- Maintain 100% backward compatibility for [public APIs]
- Preserve existing test coverage levels
- No changes to database schema during this session
- Existing functionality must continue working unchanged

## Refactoring Steps

1. [Preparatory work] - [validation method]
2. [Core extraction/modification] - [testing approach]
3. [Integration updates] - [compatibility verification]
4. [Cleanup and optimization] - [final validation]

## Risk Mitigation

- Create backup branch before starting
- Run full test suite after each major step
- Validate performance hasn't degraded
- Check for unintended dependency changes

## Success Metrics

- [ ] Code complexity reduced (measurable via [metric])
- [ ] All existing tests pass
- [ ] New architecture supports planned future changes
- [ ] No performance regression detected
- [ ] Documentation reflects new structure

## Open Questions

- [List any unresolved decisions or concerns]

What concerns do you have about this refactoring approach?

---

### Integration Session Template

---

# INTEGRATION SESSION

## Integration Goal

Connect [system A] with [system B] to enable [specific capability]

## Systems Overview

**System A ([name])**:

- Purpose: [primary function]
- Key interfaces: [APIs/methods available]
- Data formats: [inputs/outputs]
- Authentication: [security requirements]

**System B ([name])**:

- Purpose: [primary function]
- Key interfaces: [APIs/methods available]
- Data formats: [inputs/outputs]
- Authentication: [security requirements]

## Integration Requirements

- Data flow: [direction and frequency]
- Error handling: [retry policies, fallback behaviors]
- Performance: [latency/throughput requirements]
- Monitoring: [logging/alerting needs]

## Technical Approach

1. [Interface definition/adapter creation]
2. [Data transformation logic]
3. [Error handling implementation]
4. [Testing strategy for integration points]

## Dependencies and Assumptions

- [System A] provides [specific capabilities]
- [System B] accepts [specific data formats]
- Network connectivity allows [communication patterns]
- Authentication credentials available for [required access]

## Testing Strategy

- Unit tests for [transformation logic]
- Integration tests for [end-to-end flows]
- Error scenario testing for [failure modes]
- Performance testing for [load requirements]

## Rollback Plan

- [Specific steps to undo integration if issues arise]
- [Monitoring indicators that suggest rollback needed]
- [Communication plan for stakeholders]

## Open Questions

- [List any unresolved decisions or concerns]
  
What questions do you have about the integration approach or requirements?

---
