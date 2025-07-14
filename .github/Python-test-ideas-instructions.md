# PYTHON TEST CASE IDEAS INSTRUCTIONS

## PRIME DIRECTIVE
When brainstorming and proposing new Python test cases:
- Focus on generating a wide variety of test scenarios for existing code
- Use Python 3.8+ and modern best practices for all test ideas
- Reference official Python Docs for API and feature coverage
- Ensure all proposed tests are clear, actionable, and relevant


## TEST CASE IDEAS GUIDELINES
### 1. Brainstorming and Coverage
- Identify all public functions, methods, and classes to be tested
- Propose test ideas for:
  - Typical/expected usage scenarios
  - Edge cases and boundary conditions
  - Error and exception handling
  - Integration with other modules
  - Performance and security aspects
- Use descriptive scenario names: `test_[function]_[scenario]_[expected_result]`
- Suggest tests for input validation, output correctness, and side effects


### 2. Well-Structured Test Case Proposals
# PYTHON TEST CASE IDEAS INSTRUCTIONS

## PRIME DIRECTIVE
When brainstorming and proposing new Python test cases:
- Focus on generating a wide variety of test scenarios for existing code
- Use Python 3.8+ and modern best practices for all test ideas
- Reference official Python Docs for API and feature coverage
- Ensure all proposed tests are clear, actionable, and relevant


## TEST CASE IDEAS GUIDELINES
### 1. Brainstorming and Coverage
- Identify all public functions, methods, and classes to be tested
- Propose test ideas for:
  - Typical/expected usage scenarios
  - Edge cases and boundary conditions
  - Error and exception handling
  - Integration with other modules
  - Performance and security aspects
- Use descriptive scenario names: `test_[function]_[scenario]_[expected_result]`
- Suggest tests for input validation, output correctness, and side effects


### 2. Well-Structured Test Case Proposals
- For each test idea, provide:
  - What should be tested (functionality, scenario)
  - Why it is important (risk, coverage, regression, business logic)
  - Expected result (success, error, output, side effect)
- Use bullet points or tables for clarity
- Include setup requirements and dependencies if relevant
- Document each idea with a short rationale
- **Document all test case ideas in a new markdown file** named `test-ideas-[module-name]-[date].md` in the project's `docs/testing/` directory
- Follow consistent file naming conventions and organize ideas by module or feature area
- Include timestamp and author information in the documentation header


### 3. Test Case Idea Documentation Template
```
Test Case Idea:
- Function/Feature: [Name]
- Scenario: [Description of scenario]
- Importance: [Why this test matters]
- Expected Result: [What should happen]
- Setup/Dependencies: [Any special setup or mocks needed]
```

### 3. MCP Server Integration for Test Case Development
- **Sequential Thinking MCP Server**: Use to analyze complex testing scenarios systematically
  - Break down large modules into logical test groupings
  - Analyze test dependencies and execution order
  - Document reasoning process for test priority decisions
  - Apply decision-making frameworks for test coverage gaps
- **Memory MCP Server**: Use to store and retrieve test-related information
  - Track test case ideas across development sessions
  - Maintain context for module testing strategies
  - Store lessons learned from previous test implementations
  - Ensure consistency in test naming and organization patterns
- **Fallback Protocol**: If MCP servers are unavailable, document assumptions and proceed with manual analysis


### 4. Test Case Idea Validation Checklist
- [ ] Covers a unique scenario or risk
- [ ] Clearly describes what is being tested
- [ ] Expected result is unambiguous
- [ ] Rationale for test is provided
- [ ] Setup and dependencies are noted


### 5. Error and Regression Test Ideas
- Propose tests for known bugs, previous failures, and regression risks
- Suggest tests for error handling, invalid input, and exception scenarios
- Document why each error test is needed


### 6. Collaboration and Documentation
- When proposing test ideas, use clear language and structure
- Reference related Jira tickets or requirements if available
- Document architectural decisions and test strategies for future reference


### 7. MCP Server and Python Docs
- Validate test ideas against official Python documentation
- If MCP server unavailable, note any assumptions made


### 8. Example Test Case Idea
```
Test Case Idea:
- Function/Feature: add_user
- Scenario: Add user with valid input data
- Importance: Verifies main business logic and prevents regression
- Expected Result: User is added successfully to database
- Setup/Dependencies: Database mock, UserService
```


---
Use these instructions to generate well-structured, actionable, and comprehensive ideas for Python test cases. Focus on scenario coverage, clarity, and rationale for each proposed test.
  - What should be tested (functionality, scenario)
  - Why it is important (risk, coverage, regression, business logic)
  - Expected result (success, error, output, side effect)
- Use bullet points or tables for clarity
- Include setup requirements and dependencies if relevant
- Document each idea with a short rationale


### 3. Test Case Idea Documentation Template
```
Test Case Idea:
- Function/Feature: [Name]
- Scenario: [Description of scenario]
- Importance: [Why this test matters]
- Expected Result: [What should happen]
- Setup/Dependencies: [Any special setup or mocks needed]
```

### 3. MCP Server Integration for Test Case Development
- **Sequential Thinking MCP Server**: Use to analyze complex testing scenarios systematically
  - Break down large modules into logical test groupings
  - Analyze test dependencies and execution order
  - Document reasoning process for test priority decisions
  - Apply decision-making frameworks for test coverage gaps
- **Memory MCP Server**: Use to store and retrieve test-related information
  - Track test case ideas across development sessions
  - Maintain context for module testing strategies
  - Store lessons learned from previous test implementations
  - Ensure consistency in test naming and organization patterns
- **Fallback Protocol**: If MCP servers are unavailable, document assumptions and proceed with manual analysis


### 4. Test Case Idea Validation Checklist
- [ ] Covers a unique scenario or risk
- [ ] Clearly describes what is being tested
- [ ] Expected result is unambiguous
- [ ] Rationale for test is provided
- [ ] Setup and dependencies are noted


### 5. Error and Regression Test Ideas
- Propose tests for known bugs, previous failures, and regression risks
- Suggest tests for error handling, invalid input, and exception scenarios
- Document why each error test is needed


### 6. Collaboration and Documentation
- When proposing test ideas, use clear language and structure
- Reference related Jira tickets or requirements if available
- Document architectural decisions and test strategies for future reference


### 7. MCP Server and Python Docs
- Validate test ideas against official Python documentation
- If MCP server unavailable, note any assumptions made


### 8. Example Test Case Idea
```
Test Case Idea:
- Function/Feature: add_user
- Scenario: Add user with valid input data
- Importance: Verifies main business logic and prevents regression
- Expected Result: User is added successfully to database
- Setup/Dependencies: Database mock, UserService
```


---
Use these instructions to generate well-structured, actionable, and comprehensive ideas for Python test cases. Focus on scenario coverage, clarity, and rationale for each proposed test.