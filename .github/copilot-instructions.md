---
applyTo: "**"
---
# Project General Coding Standards

## WORKFLOW GUIDELINES

### 1. Fetch Jira Tasks
Use the Atlassian MCP Server to retrieve Jira tasks. If MCP server is unavailable, request task list from user. If user cannot provide tasks, create placeholder tasks based on project scope and request prioritization guidance.
- Prioritize tasks based on business value (High/Medium/Low impact) and dependencies (blocking/blocked relationships)
- Ensure tasks are well-defined with clear acceptance criteria (SMART: Specific, Measurable, Achievable, Relevant, Time-bound)
- Break down large tasks (>8 hours estimated effort) into smaller, manageable sub-tasks (<4 hours each)
- Use consistent labels for categorization: bug, feature, enhancement, tech-debt, documentation
- Assign tasks to appropriate team members based on expertise match (>70% skill alignment) and current workload (<80% capacity)

**Validation Checklist:**
- [ ] Task list retrieved from Atlassian MCP Server or user
- [ ] All tasks have SMART acceptance criteria
- [ ] Large tasks broken down to <4 hour sub-tasks
- [ ] Consistent labeling applied (bug, feature, enhancement, tech-debt, documentation)
- [ ] Team assignments based on expertise (>70% match) and capacity (<80% utilization)

**Fallback Procedure:**
If Atlassian MCP Server is unavailable:
1. Request task list from user in format: "Task ID | Priority | Description | Acceptance Criteria | Estimated Hours"
2. If user cannot provide tasks, create placeholder tasks based on project scope:
   - Analyze project documentation for key deliverables
   - Create high-level Epics for major functional areas
   - Request user prioritization and approval before proceeding

### 2. Determine Most Logical Next Task
Based on completed tasks and yet-to-be-completed tasks, using systematic decision matrix:
- Analyze dependencies and blockers using dependency graph visualization
- Consider team member availability (current sprint capacity) and expertise (skill matrix alignment)
- Ensure alignment with project goals and timelines using milestone tracking
- Communicate task priorities clearly using standard format: Priority Level (High/Medium/Low), Business Impact (Critical/Important/Nice-to-have), Dependencies (Blocking X tasks), Estimated Effort (hours), Completion Timeline (target date)

**Decision Matrix Criteria:**
1. **Dependency Score** (0-10): Higher score for tasks with fewer dependencies
2. **Business Value Score** (0-10): Critical=10, Important=7, Nice-to-have=3
3. **Team Readiness Score** (0-10): Based on expertise match and availability
4. **Risk Score** (0-10): Lower score for higher risk tasks
5. **Total Score**: Sum of all criteria, highest score = next task

**Communication Template:**
```
NEXT TASK RECOMMENDATION:
- Task: [Task ID - Description]
- Priority Level: [High/Medium/Low]
- Business Impact: [Critical/Important/Nice-to-have]
- Dependencies: [Blocking X tasks, Blocked by Y tasks]
- Estimated Effort: [X hours]
- Completion Timeline: [Target date]
- Decision Score: [Total from decision matrix]
- Rationale: [Brief explanation of selection]
```

### 3. Implement New Code
- Fetch latest code from the repository using `git pull origin main`
- Follow coding standards and best practices per language-specific guidelines (PEP 8 for Python, Microsoft .NET Guidelines for C#, C11/C17 standards for C)
- Write clean, maintainable code with proper documentation
- Implement proper error handling with specific exception types
- Use meaningful variable and function names following established conventions
- Add inline comments for complex business logic
- Ensure backward compatibility when modifying existing APIs

**Code Quality Checklist:**
- [ ] Latest code fetched from repository
- [ ] Language-specific coding standards followed
- [ ] Error handling implemented with specific exceptions
- [ ] Meaningful names used for variables and functions
- [ ] Complex logic documented with inline comments
- [ ] Backward compatibility maintained for existing APIs
- [ ] Code reviewed for performance implications

### 4. Implement New Tests
- Write unit tests for new code using Test-Driven Development (TDD) principles where applicable
- Ensure test coverage meets project standards: minimum 80% line coverage for unit tests, 70% branch coverage, all public methods must have corresponding tests
- Use mocking and stubbing where appropriate to isolate tests from external dependencies (databases, APIs, file systems)
- Follow naming conventions for test cases: test_[method]_[scenario]_[expected_result] format
- Write comprehensive documentation for tests explaining their purpose, test scenarios, expected outcomes, and any special setup requirements

**Test Categories Required:**
1. **Unit Tests**: Test individual methods/functions in isolation
2. **Integration Tests**: Test component interactions
3. **Edge Case Tests**: Test boundary conditions and error scenarios
4. **Performance Tests**: Test performance requirements where applicable

**Test Documentation Template:**
```
/**
 * Test Purpose: [What is being tested]
 * Test Scenario: [Specific scenario/conditions]
 * Expected Outcome: [What should happen]
 * Setup Requirements: [Any special setup needed]
 * Dependencies: [External dependencies or mocks used]
 */
```

**Test Coverage Validation:**
- [ ] Minimum 80% line coverage achieved
- [ ] Minimum 70% branch coverage achieved
- [ ] All public methods have corresponding tests
- [ ] Edge cases and error scenarios tested
- [ ] Test documentation complete and clear

### 5. Run Tests
- Execute all tests to ensure code quality using automated test runners
- Use continuous integration tools to automate testing with build pipeline integration
- Address any failing tests immediately: identify root cause, create fix branch, implement fix with additional test, verify fix resolves issue, document resolution in ticket
- Ensure all tests pass before proceeding to next step (mandatory quality gate)
- Document test results and any issues encountered with timestamps, test environment details, and resolution steps
- If tests fail, debug and fix issues before proceeding using systematic debugging approach
- If tests pass, proceed to the next step with test execution summary
- If tests are not applicable, ask for confirmation to skip to the next step with documented justification

**Test Execution Protocol:**
1. **Pre-execution Check**: Verify test environment is properly configured
2. **Execute Tests**: Run full test suite with verbose output
3. **Result Analysis**: Review test results for failures, warnings, and performance issues
4. **Failure Resolution**: For each failing test:
   - Identify root cause using systematic debugging
   - Create dedicated fix branch: `bugfix/PROJ-XXX-test-failure-description`
   - Implement fix with additional regression test
   - Verify fix resolves issue without breaking other tests
   - Document resolution in associated Jira ticket
5. **Documentation**: Record test execution summary with:
   - Timestamp and environment details
   - Total tests run, passed, failed, skipped
   - Coverage metrics achieved
   - Performance benchmarks (if applicable)
   - Any issues encountered and resolutions

**Quality Gate Enforcement:**
- [ ] All tests executed successfully
- [ ] Test coverage thresholds met (80% line, 70% branch)
- [ ] No failing tests remaining
- [ ] Test execution documented with results
- [ ] Any issues resolved and documented

### 6. Commit and Push Changes
- Use clear, descriptive commit messages that include: action verb, component affected, and ticket reference (e.g., 'Add user authentication to login service - PROJ-123')
- Reference Jira ticket IDs in commit messages using format: "PROJ-XXX: [Description]"
- Ensure code is pushed to the correct branch following naming convention: feature/PROJ-XXX-brief-description
- Follow branching strategy (e.g., feature branches, hotfix branches) with proper branch protection rules
- Ensure all changes are properly documented in the commit history with atomic commits and descriptive messages

**Commit Message Template:**
```
PROJ-XXX: [Action verb] [component/feature] [brief description]

- [Specific change 1]
- [Specific change 2]
- [Specific change 3]

Resolves: PROJ-XXX
Tests: [Test coverage details]
```

**Branch Naming Conventions:**
- Feature branches: `feature/PROJ-XXX-brief-description`
- Bugfix branches: `bugfix/PROJ-XXX-issue-description`
- Hotfix branches: `hotfix/PROJ-XXX-critical-fix`
- Release branches: `release/vX.Y.Z`

**Pre-commit Validation:**
- [ ] Commit message follows template format
- [ ] Jira ticket ID referenced correctly
- [ ] Branch name follows naming convention
- [ ] All changes are atomic and related
- [ ] No sensitive information included in commit
- [ ] Commit description explains the "why" not just the "what"

### 7. Update Jira Task
- Update task status and progress in Jira using appropriate workflow transitions
- Add comprehensive comments and documentation including:
  - Summary of work completed
  - Technical implementation details
  - Testing results and coverage metrics
  - Any issues encountered and resolutions
  - Links to code changes and pull requests
- Link related tasks and issues using proper Jira relationships (blocks, depends on, relates to, duplicates)
- Ensure all acceptance criteria are validated and met before closing tasks
- If the task is blocked, communicate with the team to resolve issues and document blocking reasons

**Jira Update Template:**
```
Work Completed:
- [Detailed description of implementation]
- [Key technical decisions made]

Testing Results:
- Test Coverage: X% line coverage, Y% branch coverage
- Tests Added: [Number and type of tests]
- Performance Impact: [Any performance considerations]

Code Changes:
- Branch: feature/PROJ-XXX-description
- Commit: [commit hash]
- Files Modified: [key files changed]

Next Steps:
- [Any follow-up work needed]
- [Dependencies for other tasks]
```

**Status Transition Validation:**
- [ ] All acceptance criteria verified and checked off
- [ ] Code review completed (if required)
- [ ] Tests passing and coverage thresholds met
- [ ] Documentation updated
- [ ] No blocking issues remaining
- [ ] Proper status transition applied (In Progress → Code Review → Testing → Done)

### 8. Repeat Process
- Continuously monitor progress and adjust plans as needed
- Return to step 1 for next iteration

## MCP SERVER INTEGRATION

### Atlassian MCP Server
- Use the MCP server to retrieve and update Jira tasks with proper error handling
- Ensure proper authentication and connection handling with retry logic
- Implement exponential backoff for rate limiting scenarios (initial delay: 1 second, max delay: 60 seconds)
- Cache task data locally when possible to handle network connectivity issues
- Validate API responses and handle authentication failures gracefully

**Connection Management:**
- Primary: Use Atlassian MCP Server API
- Fallback: Manual task entry if MCP server unavailable
- Error Recovery: Clear re-authentication guidance provided to user
- Data Validation: Verify task data integrity before processing

**Validation Checklist:**
- [ ] MCP server connection established and authenticated
- [ ] Task data retrieved successfully with all required fields
- [ ] API response validation passed (status codes, data structure)
- [ ] Retry logic implemented for rate limiting (max 5 retries)
- [ ] Local cache updated with retrieved task data
- [ ] Authentication token refresh capability verified

### GitHub MCP Server
- Use the MCP server to retrieve and update GitHub issues with proper error handling
- Ensure all code changes are properly documented in GitHub issues using standardized templates
- Use the MCP server to manage pull requests and code reviews with automatic validation
- Implement retry logic for GitHub API rate limits (maximum 5 retries with exponential backoff)

**GitHub Integration Protocol:**
- Primary: Use GitHub MCP Server API for all repository operations
- Fallback: Manual GitHub operations via web interface if MCP server unavailable
- Error Recovery: Clear guidance for authentication token refresh
- Data Validation: Verify pull request and issue data integrity before processing

**GitHub Update Template:**
```
Issue/PR Update:
- Status: [Open/In Progress/Under Review/Closed]
- Branch: [branch name]
- Commits: [commit hashes]
- Files Changed: [list of modified files]
- Test Results: [coverage and status]
- Review Status: [pending/approved/changes requested]
```

**GitHub Validation Requirements:**
- [ ] Pull request created with mandatory fields (title, description, reviewers)
- [ ] All commits reference corresponding Jira tickets
- [ ] Branch naming convention followed (feature/PROJ-XXX-description)
- [ ] Required CI/CD checks passing before merge approval
- [ ] Code review completed by minimum 2 team members
- [ ] Documentation updated for all public API changes

### Sequential Thinking MCP Server
- Use the Sequential thinking MCP server to analyze and break down complex tasks systematically
- Leverage for requirement analysis and task decomposition with structured thought processes
- Apply decision-making frameworks for complex problem-solving scenarios
- Document reasoning process for future reference and team learning

**Sequential Thinking Protocol:**
- Use for complex analysis requiring multi-step reasoning
- Document thought process with clear logical progression
- Validate conclusions against original requirements
- Share reasoning with team for knowledge transfer

**Analysis Validation:**
- [ ] Problem broken down into logical, sequential steps
- [ ] Each step builds on previous conclusions
- [ ] Alternative approaches considered and documented
- [ ] Final recommendation supported by clear reasoning chain
- [ ] Analysis shared with team for validation and learning

### Memory MCP Server
- Use the Memory MCP server to store and retrieve project-related information consistently
- Maintain context across development sessions using structured knowledge graphs
- Track project decisions, assumptions, and lessons learned
- Ensure information persistence and retrieval accuracy

**Memory Management Protocol:**
- Store key project decisions with rationale and context
- Maintain entity relationships for complex project structures
- Regular validation of stored information accuracy
- Clear data retention and archiving policies

**Information Validation:**
- [ ] Critical project decisions stored with full context
- [ ] Entity relationships accurately mapped and maintained
- [ ] Information retrieval tested and verified for accuracy
- [ ] Data retention policies documented and implemented
- [ ] Knowledge transfer mechanisms established for team access

## REQUIREMENTS ANALYSIS & TICKET CREATION

When working with requirements documents:
- Analyze requirements systematically and create comprehensive Jira tickets
- Break down complex features into manageable, trackable work items
- Ensure all project deliverables are properly documented and planned
- Be conversational and explain your analysis process while working

### DOCUMENT ANALYSIS PHASE

When analyzing requirements documents:
1. **ALWAYS** start by reading and understanding the entire document structure
2. Identify key functional areas and features using systematic categorization
3. Extract user stories and acceptance criteria with specific validation rules
4. Note technical specifications and constraints with impact assessment
5. Identify dependencies between different features using dependency mapping

**Document Analysis Checklist:**
- [ ] Document structure completely understood and mapped
- [ ] All functional areas identified and categorized
- [ ] User stories extracted with measurable acceptance criteria
- [ ] Technical specifications documented with feasibility assessment
- [ ] Dependencies mapped with critical path analysis
- [ ] Risk assessment completed for each functional area
- [ ] Stakeholder requirements validated and confirmed

**Analysis Template:**
```
DOCUMENT ANALYSIS SUMMARY:
- Document: [name and version]
- Total Functional Areas: [number]
- User Stories Identified: [number]
- Technical Constraints: [list key constraints]
- Dependencies: [critical dependencies]
- Risk Level: [High/Medium/Low]
- Estimated Complexity: [story points]
- Recommended Epic Count: [5-7 Epics]
```

### JIRA & GITHUB INTEGRATION

For each identified requirement:
- Create Epic for major functional areas
- Break down Epics into Stories for user-facing features
- Create Tasks for technical implementation work
- Add Bugs for known issues or constraints
- Include Sub-tasks for detailed implementation steps

Include all relevant details in each ticket:
- **Title**: Clear and descriptive
- **Description**: Detailed explanation of the requirement
- **Acceptance Criteria**: Specific conditions for completion
- **Definition of Done**: Criteria for ticket completion
- **Labels**: Use consistent labels for categorization (e.g., feature, bug, enhancement)
- **Components**: Assign to relevant project components
- **Priority**: Set appropriate priority levels (e.g., high, medium, low)
- **Assignee**: Assign to the appropriate team member

**Integration Requirements**:
- All work items must be traceable to Jira tickets
- Commit messages and branches must reference Jira ticket IDs
- Use branch naming conventions that align with Jira ticket numbers (e.g., `feature/PROJ-123-feature-name`)

## PROJECT PLANNING & TICKET STRUCTURING

### MANDATORY PLANNING PHASE

When creating project plans from requirements:
1. **ALWAYS** start by creating a comprehensive project breakdown
2. Your plan **MUST** include:
   - Epic definitions for major functional areas (maximum 5-7 Epics per project)
   - Story mapping for user journeys (detailed user persona flows)
   - Technical task identification (specific implementation components)
   - Dependency mapping between tickets (visual dependency graph with critical path)
   - Estimated effort and priority levels (story points using Fibonacci sequence: 1, 2, 3, 5, 8, 13)
   - Acceptance criteria for each ticket (SMART format: Specific, Measurable, Achievable, Relevant, Time-bound)

**Planning Validation Checklist:**
- [ ] Project breakdown covers all requirement areas (100% coverage verified)
- [ ] Epic count within recommended range (5-7 Epics)
- [ ] All user journeys mapped with clear entry/exit points
- [ ] Technical components identified with specific technologies
- [ ] Dependency graph shows critical path and bottlenecks
- [ ] Effort estimates use Fibonacci sequence consistently
- [ ] All acceptance criteria follow SMART format

3. Format your plan as:

```
## PROJECT BREAKDOWN PLAN
Requirements Source: [document name]
Total Epics: [number] (recommended: 5-7)
Total Stories: [number] (recommended: 15-25 per Epic)
Total Tasks: [number] (recommended: 3-5 per Story)
Estimated Timeline: [duration] (based on team velocity and capacity)
Risk Assessment: [High/Medium/Low] (based on technical complexity and dependencies)
Critical Path: [Epic1 → Epic2 → Epic3] (sequence of blocking dependencies)
```

**Plan Approval Requirements:**
- [ ] User explicitly approves Epic structure before proceeding
- [ ] Timeline aligns with business milestones and deadlines
- [ ] Resource allocation matches team capacity (<80% utilization)
- [ ] Risk mitigation strategies identified for High-risk items

### TICKET CREATION PROCESS

- Focus on one Epic at a time with its related Stories/Tasks (prevents context switching and ensures completeness)
- Create clear, actionable ticket titles using format: "[Component] [Action] [Brief Description]" (e.g., "Authentication Service: Implement OAuth2 integration")
- Include comprehensive acceptance criteria and definition of done with measurable outcomes
- Add relevant labels, components, and priority levels using standardized taxonomy
- Link related tickets appropriately (blocks, depends on, relates to, duplicates) with explicit relationship descriptions

**Ticket Quality Standards:**
- [ ] Title follows naming convention: "[Component] [Action] [Brief Description]"
- [ ] Description includes context, requirements, and constraints
- [ ] Acceptance criteria are measurable and testable
- [ ] Definition of done includes code review, testing, and documentation requirements
- [ ] Effort estimation provided using Fibonacci sequence
- [ ] Priority level assigned (Critical/High/Medium/Low)
- [ ] Component and labels applied consistently
- [ ] Dependencies explicitly documented with rationale

### Ticket Creation Sequence

1. **[Epic Name]** - Purpose: [business value]
   - Stories: [list of user stories]
   - Tasks: [technical implementation items]
2. **[Next Epic]** - Purpose: [business value]
3. Do you approve this ticket structure? I'll proceed with creating tickets after your confirmation.
4. **WAIT** for explicit user confirmation before creating ANY tickets

### EXECUTION PHASE

- After each ticket creation, clearly indicate progress using standard format:
  `"✅ Created [Epic/Story/Task] [#] of [total]. Coverage: [X%] complete. Ready for next ticket?"`
- If you discover additional requirements during analysis:
  - **STOP** immediately and document the discovery
  - Update the project breakdown plan with new requirements
  - Recalculate effort estimates and timeline impact
  - Get explicit user approval before continuing with expanded scope
- Maintain requirement coverage tracking to ensure 100% coverage before completion

**Progress Tracking Template:**
```
PROGRESS UPDATE:
- Phase: [Epic Name] - [Story/Task Name]
- Completed: [X] of [Total] tickets ([Y%] complete)
- Requirements Coverage: [Z%] of original requirements addressed
- New Requirements Discovered: [Number] (impact: [High/Medium/Low])
- Timeline Impact: [+/- X days] from original estimate
- Next Action: [Continue/Update Plan/Seek Approval]
```

**Progress Tracking Template:**
```
PROGRESS UPDATE:
- Phase: [Epic Name] - [Story/Task Name]
- Completed: [X] of [Total] tickets ([Y%] complete)
- Requirements Coverage: [Z%] of original requirements addressed
- New Requirements Discovered: [Number] (impact: [High/Medium/Low])
- Timeline Impact: [+/- X days] from original estimate
- Next Action: [Continue/Update Plan/Seek Approval]
```

### AGILE METHODOLOGY GUIDANCE

When structuring tickets:
- Ensure Stories follow INVEST principles (Independent, Negotiable, Valuable, Estimable, Small, Testable)
- Break down large Stories into smaller, manageable pieces
- Consider technical debt and maintenance tasks
- Always include user acceptance testing criteria
- Plan for documentation and training deliverables

### REQUIREMENTS TRACEABILITY

- For complex requirements documents, maintain traceability mapping
- Link each ticket back to specific sections in the requirements document
- Track coverage to ensure no requirements are missed
- Plan for requirements validation and testing

## ERROR HANDLING & BEST PRACTICES

### Common Error Scenarios
- **MCP Server Unavailable**: Fallback to manual task management with documented process
- **API Rate Limits**: Implement retry logic with exponential backoff (initial delay: 1 second, max delay: 60 seconds, max retries: 5)
- **Network Issues**: Cache critical data locally when possible and implement offline mode capabilities
- **Authentication Failures**: Provide clear guidance for re-authentication with step-by-step instructions

**Error Resolution Protocol:**
1. **Immediate Response**: Log error details with timestamp and context
2. **Fallback Activation**: Switch to appropriate fallback procedure within 30 seconds
3. **User Notification**: Communicate status and expected resolution time
4. **Recovery Validation**: Verify fallback system functionality
5. **Documentation**: Record incident details and resolution steps

**Error Handling Validation:**
- [ ] All error scenarios have documented fallback procedures
- [ ] Retry logic implemented with exponential backoff
- [ ] User notifications provide clear status and next steps
- [ ] Error logs capture sufficient detail for debugging
- [ ] Recovery procedures tested and validated

### Code Quality Standards
- Follow language-specific style guides (PEP 8 for Python, Microsoft .NET Guidelines for C#, C11/C17 standards for C)
- Implement proper error handling and logging with specific exception types and error codes
- Use consistent naming conventions following established patterns (camelCase for JavaScript, snake_case for Python, PascalCase for C#)
- Document complex business logic with inline comments explaining the "why" not just the "what"
- Ensure backward compatibility when possible by versioning APIs and maintaining deprecated method support

**Code Quality Validation:**
- [ ] Style guide compliance verified using automated linting tools
- [ ] Error handling implemented with specific exception types
- [ ] Naming conventions consistently applied across codebase
- [ ] Complex logic documented with business context
- [ ] Backward compatibility verified through regression testing
- [ ] Code review completed by minimum 2 team members

### Performance Considerations
- Optimize database queries and API calls by implementing query optimization, indexing strategies, and connection pooling
- Implement caching strategies where appropriate using Redis or in-memory caching for frequently accessed data
- Monitor resource usage and performance metrics with specific thresholds (CPU <80%, Memory <90%, Response time <200ms)
- Use lazy loading for large datasets to minimize initial load times and memory usage

**Performance Validation:**
- [ ] Database query performance analyzed and optimized
- [ ] Caching strategy implemented for frequently accessed data
- [ ] Resource usage monitoring configured with alerting thresholds
- [ ] Lazy loading implemented for large datasets
- [ ] Performance benchmarks established and regularly tested
- [ ] Load testing completed for expected traffic patterns

## SPACING CORRECTION GUIDELINES

### IDENTIFYING ISSUES
- Look for concatenated words without spaces in text, code blocks, and inline formatting using systematic scanning
- Pay special attention to section titles, instructions, and tables with focus on readability impact
- Use consistent spacing rules to ensure readability following established style guide standards
- Identify missing spaces between words, punctuation, and formatting elements

**Issue Detection Protocol:**
1. **Systematic Scanning**: Review document section by section from top to bottom
2. **Pattern Recognition**: Look for common concatenation patterns (word+word, word+punctuation)
3. **Formatting Review**: Check code blocks, tables, and bullet points for spacing consistency
4. **Style Guide Compliance**: Verify adherence to established spacing standards

**Detection Validation:**
- [ ] Complete document scanned for spacing issues
- [ ] Section titles and headings reviewed for proper spacing
- [ ] Code blocks and inline formatting checked for consistency
- [ ] Tables and lists validated for spacing compliance
- [ ] Style guide standards applied consistently

### CORRECTION PROCESS
1. Start with section titles and headings (highest impact on readability)
2. Move to instructions and inline text (medium impact on comprehension)
3. Correct tables and lists last (formatting consistency)
4. Ensure all changes maintain the original formatting style and document structure
5. Validate corrections improve readability without altering meaning

**Correction Validation:**
- [ ] Section titles and headings corrected with proper spacing
- [ ] Inline text and instructions reviewed and corrected
- [ ] Tables and lists formatted consistently
- [ ] Original document structure and formatting preserved
- [ ] All corrections verified to improve readability

### VALIDATION
- After each edit, verify that spacing corrections improve readability using readability metrics
- Check for unintended changes to formatting or content by comparing before and after versions
- Confirm that the document adheres to the project's style guide using automated validation tools
- Test document rendering across different platforms and devices for consistency

**Final Validation Checklist:**
- [ ] Readability improvements verified through testing
- [ ] No unintended formatting changes introduced
- [ ] Style guide compliance verified using validation tools
- [ ] Document rendering tested across multiple platforms
- [ ] All corrections documented for future reference

## LANGUAGE Usage Guidelines
### PRIME DIRECTIVE
always use american english
- Use clear, concise language with active voice for improved clarity and directness
- Avoid jargon and technical terms unless necessary; when used, provide clear definitions
- Use active voice for clarity and directness in all communications
- Ensure consistent terminology throughout the document using established glossary

**Language Standards Validation:**
- [ ] American English spelling and grammar rules applied consistently
- [ ] Active voice used throughout documentation
- [ ] Technical terms defined when first introduced
- [ ] Terminology consistency verified using project glossary
- [ ] Clarity improvements implemented and validated

### LANGUAGE USAGE
- Use proper grammar and punctuation following American English standards
- Avoid contractions in formal documentation (do not use "don't", "can't", "won't")
- Use bullet points and numbered lists for clarity and improved information organization
- Ensure proper capitalization for section titles and headings using Title Case standards
- Use consistent terminology for technical terms and concepts with defined meanings
- Avoid using slang or colloquial expressions that may cause confusion in professional contexts

**Language Quality Validation:**
- [ ] Grammar and punctuation checked using automated tools
- [ ] Contractions removed from formal documentation
- [ ] Bullet points and numbered lists used appropriately for organization
- [ ] Section titles and headings follow Title Case standards
- [ ] Technical terminology used consistently with defined meanings
- [ ] Slang and colloquial expressions eliminated from professional documentation
- [ ] Language clarity and professionalism verified through review
