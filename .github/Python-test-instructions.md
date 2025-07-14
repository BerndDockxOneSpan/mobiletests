# PYTHON TEST CREATION INSTRUCTIONS
## PRIME DIRECTIVE
When creating new tests for existing Python code:
- Always use Python 3.8+ and follow modern Python best practices
- Reference official Python Docs for API usage and patterns
- Ensure all new code is testable and covered by unit and integration tests
- Use PEP 8 formatting, type hints, and proper dependency management

## TEST CREATION GUIDELINES
### 1. Test Coverage and Structure
- Write unit tests for all public functions, methods, and classes
- Achieve minimum 80% line coverage and 70% branch coverage
- Use pytest or unittest for all test suites
- Structure tests in dedicated test files (e.g., `test_module.py`)
- Use clear, descriptive test names: `test_[function]_[scenario]_[expected_result]`
- Organize tests by feature, edge case, error scenario, and integration

### 2. Test Implementation Best Practices
- Use PEP 8 formatting and automatic formatters (black, autopep8)
- Add type hints to all test functions and fixtures
- Use fixtures for setup/teardown and reusable test data
- Mock external dependencies to isolate unit tests
- Use assert statements with clear error messages
- Document each test with a docstring explaining purpose, scenario, and expected outcome

### 3. Test Documentation Template
```
def test_function_scenario_expected_result():
    """
    Test Purpose: [What is being tested]
    Test Scenario: [Specific scenario/conditions]
    Expected Outcome: [What should happen]
    Setup Requirements: [Any special setup needed]
    Dependencies: [External dependencies or mocks used]
    """
    # ...test code...
```

### 4. Validation and Quality Checklist
- [ ] PEP 8 compliance verified (flake8, pylint)
- [ ] Type hints present in all test functions
- [ ] Test coverage ≥80% line, ≥70% branch
- [ ] All public APIs and error scenarios tested
- [ ] Edge cases and boundary conditions covered
- [ ] Test documentation complete and clear
- [ ] Tests run successfully on Windows and Linux
- [ ] No sensitive data or credentials in test code

### 5. Error Recovery and Debugging
- For failing tests, debug systematically and add regression tests
- Use descriptive error messages and logging for failures
- Document any assumptions or limitations in test code

### 6. Commit and Branching
- Use clear commit messages: `PROJ-XXX: [Action] [Component] - [Description]`
- Reference Jira ticket IDs in commit messages
- Use feature/bugfix branch naming conventions

### 7. MCP Server and Documentation
- Validate Python API usage against official documentation
- Document architectural decisions and test strategies
- If MCP server unavailable, use cached docs and note assumptions

### 8. Example Test Case
```
def test_add_user_valid_input():
    """
    Test Purpose: Verify user addition with valid input
    Test Scenario: Add user with correct data
    Expected Outcome: User is added successfully
    Setup Requirements: Database mock
    Dependencies: UserService, database mock
    """
    # ...test code...
```

---
Follow these instructions to ensure all new tests for existing Python code are maintainable, well-documented, and provide reliable coverage for your project.
**Code Quality Validation Checklist:**
- [ ] PEP 8 compliance verified using automated linting tools (flake8, pylint)
- [ ] Type hints added to all function parameters and return values
- [ ] Virtual environment created and activated for development
- [ ] Dependencies pinned in requirements.txt or pyproject.toml
- [ ] Specific exception types created with meaningful messages
- [ ] Unit test coverage ≥80% line coverage, ≥70% branch coverage
- [ ] Integration tests cover all public APIs
- [ ] Performance benchmarks meet <200ms response time requirements
- [ ] Security tests validate input sanitization and data handling
- [ ] Cross-platform compatibility verified on Windows and Linux
- [ ] Commit messages follow "PROJ-XXX: [Action] [Component] - [Description]" format

**Error Recovery Procedures:**
- **Import Errors**: Check virtual environment activation, verify dependency installation, validate Python version compatibility
- **Test Failures**: Debug systematically, create regression tests, verify fix doesn't break existing functionality
- **MCP Server Unavailable**: Cache Python Docs locally, use offline documentation, document any assumptions made
- **Performance Issues**: Profile application using cProfile, identify bottlenecks, implement optimizations, validate improvements with benchmarks

### PYTHON DOCS MCP SERVER USAGE
- Always ground Python technical answers in official Python Docs via the MCP server
- **Fallback Procedure**: If MCP server unavailable, use cached documentation and clearly document any assumptions
- **Validation Requirements**: Verify all API references against official documentation before implementation
- **Context Preservation**: Store architectural decisions and library choices in project documentation for future reference

**MCP Server Integration Validation:**
- [ ] MCP server connection established and authenticated
- [ ] Python Docs API access verified and functional
- [ ] Cached documentation updated within last 24 hours
- [ ] All API references validated against official documentation
- [ ] Architectural decisions documented with rationale and source references