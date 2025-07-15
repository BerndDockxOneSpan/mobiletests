---
applyTo: "**"
---
# Project General Coding Standards
## WORKFLOW GUIDELINES
### 1. Implement New Code
- Write clean, maintainable code with proper documentation
- Implement proper error handling with specific exception types
- Use meaningful variable and function names following established conventions
- Add inline comments for complex business logic

### 2. Implement New Tests
- Write Gherkin-style BDD tests for new features
- Follow naming conventions of the XML files
- Ensure all tests are atomic and focused on a single functionality
- Use consistent step definitions across all tests
- Implement error handling and validation steps in tests
- Use tags for categorization (e.g., @registration, @authentication, @hardware)
- use steps in comment format for clarity

### 4. Commit and Push Changes
- Use clear, descriptive commit messages that include: action verb, component affected, and ticket reference (e.g., 'Add user authentication to login service - PROJ-123')

**Commit Message Template:**
```
PROJ-XXX: [Action verb] [component/feature] [brief description]

- [Specific change 1]
- [Specific change 2]
- [Specific change 3]

Resolves: PROJ-XXX
Tests: [Test coverage details]
```
## MCP SERVER INTEGRATION
### GitHub MCP Server
- Use the MCP server to retrieve and update GitHub issues with proper error handling

**GitHub Integration Protocol:**
- Primary: Use GitHub MCP Server API for all repository operations
- Fallback: Manual GitHub operations via web interface if MCP server unavailable
- Error Recovery: Clear guidance for authentication token refresh
- Data Validation: Verify pull request and issue data integrity before processing

### Sequential Thinking MCP Server
- Use the Sequential thinking MCP server to analyze and break down complex tasks systematically

### Memory MCP Server
- Use the Memory MCP server to store and retrieve project-related information consistently

## REQUIREMENTS ANALYSIS
When working with requirements documents:
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


## LANGUAGE Usage Guidelines
- Use proper grammar and punctuation following American English standards
- Avoid contractions in formal documentation (do not use "don't", "can't", "won't")