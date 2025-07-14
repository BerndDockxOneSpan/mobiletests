# .NET DEVELOPMENT GUIDELINES

## PRIME DIRECTIVE
For .NET projects, always use C# and modern .NET best practices:
- Reference official Microsoft Docs (via MCP server) for .NET APIs, architecture, and patterns
- Ensure all features are testable via unit and integration tests with minimum 80% code coverage
- Document any platform-specific behavior and ensure cross-platform compatibility (.NET 6+ or later)
- Use dependency injection, async/await patterns, and SOLID principles consistently

**Authority Grounding Validation:**
- [ ] Microsoft Docs MCP server connection verified and functional
- [ ] All .NET API references validated against official documentation
- [ ] Version compatibility confirmed for .NET 6+ requirements
- [ ] Cross-platform compatibility tested on minimum 2 target platforms

## .NET PROJECT GUIDELINES

- All code must follow modern .NET best practices with specific requirements:
  - **Dependency Injection**: Use built-in DI container or established frameworks (Microsoft.Extensions.DependencyInjection)
  - **Async/Await**: Implement async patterns for I/O operations with proper ConfigureAwait(false) usage
  - **SOLID Principles**: Apply Single Responsibility, Open/Closed, Liskov Substitution, Interface Segregation, and Dependency Inversion
  - **Error Handling**: Implement specific exception types with meaningful error messages and logging
- Use official Microsoft Docs (via MCP server) as the primary source for .NET API usage and architecture
- All features must be covered by comprehensive testing:
  - **Unit Tests**: Minimum 80% line coverage, 70% branch coverage
  - **Integration Tests**: All public APIs and external service integrations
  - **Performance Tests**: Response time <200ms for critical operations
  - **Security Tests**: Input validation and authentication/authorization flows
- Commit messages and branches must reference Jira ticket IDs using format: "PROJ-XXX: [Action] [Component] - [Description]"
  - Example: "PROJ-123: Add user authentication service - OAuth2 implementation"
- Document platform-specific behavior with explicit compatibility matrix and testing evidence
- Example Story: "Implement Authentication Service" — Implement a C# service class with proper error handling, logging, comprehensive tests, and performance benchmarks

**Code Quality Validation Checklist:**
- [ ] Dependency injection implemented using Microsoft.Extensions.DependencyInjection
- [ ] All async operations use ConfigureAwait(false) appropriately
- [ ] SOLID principles applied with documented architectural decisions
- [ ] Specific exception types created with meaningful messages
- [ ] Unit test coverage ≥80% line coverage, ≥70% branch coverage
- [ ] Integration tests cover all public APIs
- [ ] Performance benchmarks meet <200ms response time requirements
- [ ] Security tests validate input sanitization and authentication flows
- [ ] Cross-platform compatibility verified on Windows and Linux
- [ ] Commit messages follow "PROJ-XXX: [Action] [Component] - [Description]" format

**Error Recovery Procedures:**
- **Build Failures**: Analyze build logs, identify root cause, create fix branch, implement solution with additional tests
- **Test Failures**: Debug systematically, create regression tests, verify fix doesn't break existing functionality
- **MCP Server Unavailable**: Cache Microsoft Docs locally, use offline documentation, document any assumptions made
- **Performance Issues**: Profile application, identify bottlenecks, implement optimizations, validate improvements with benchmarks

### MICROSOFT DOCS MCP SERVER USAGE
- Always ground .NET technical answers in Microsoft Docs via the MCP server
- **Fallback Procedure**: If MCP server unavailable, use cached documentation and clearly document any assumptions
- **Validation Requirements**: Verify all API references against official documentation before implementation
- **Context Preservation**: Store architectural decisions and API choices in project documentation for future reference

**MCP Server Integration Validation:**
- [ ] MCP server connection established and authenticated
- [ ] Microsoft Docs API access verified and functional
- [ ] Cached documentation updated within last 24 hours
- [ ] All API references validated against official documentation
- [ ] Architectural decisions documented with rationale and source references

# PYTHON DEVELOPMENT GUIDELINES

## PRIME DIRECTIVE
For Python projects, always use Python and modern Python best practices:
- Reference official Python Docs (via MCP server) for Python APIs, libraries, and patterns
- Ensure all features are testable via unit and integration tests with minimum 80% code coverage
- Document any platform-specific behavior and ensure cross-platform compatibility (Python 3.8+ or later)
- Use PEP 8 formatting, type hints, virtual environments, and proper dependency management

**Authority Grounding Validation:**
- [ ] Python Docs MCP server connection verified and functional
- [ ] All Python API references validated against official documentation
- [ ] Version compatibility confirmed for Python 3.8+ requirements
- [ ] Cross-platform compatibility tested on minimum 2 target platforms

## PYTHON PROJECT GUIDELINES

- All code must follow modern Python best practices with specific requirements:
  - **PEP 8**: Use automatic formatters (black, autopep8) with line length 88 characters
  - **Type Hints**: All function parameters and return values must have type annotations
  - **Virtual Environments**: Use venv or conda for isolated development environments
  - **Dependency Management**: Use requirements.txt or pyproject.toml with pinned versions
  - **Error Handling**: Implement specific exception types with meaningful error messages and logging
- Use official Python Docs (via MCP server) as the primary source for Python API usage and architecture
- All features must be covered by comprehensive testing:
  - **Unit Tests**: Minimum 80% line coverage, 70% branch coverage using pytest or unittest
  - **Integration Tests**: All public APIs and external service integrations
  - **Performance Tests**: Response time <200ms for critical operations
  - **Security Tests**: Input validation and data sanitization flows
- Commit messages and branches must reference Jira ticket IDs using format: "PROJ-XXX: [Action] [Component] - [Description]"
  - Example: "PROJ-123: Add user authentication service - OAuth2 implementation"
- Document platform-specific behavior with explicit compatibility matrix and testing evidence
- Example Story: "Implement Authentication Service" — Implement a Python service class with proper error handling, logging, comprehensive tests, and performance benchmarks

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

# C DEVELOPMENT GUIDELINES

## PRIME DIRECTIVE
For C projects, always use modern C standards and best practices:
- Follow C11/C17 standards for modern C development with specific compiler flags
- Ensure all features are testable via unit tests with minimum 80% code coverage
- Document any platform-specific behavior and ensure portability across target platforms
- Use proper memory management, error handling, and modular design principles

**Authority Grounding Validation:**
- [ ] C11/C17 standard compliance verified using compiler warnings
- [ ] All C API references validated against ISO C documentation
- [ ] Platform compatibility confirmed for target environments
- [ ] Memory safety analysis completed using static analysis tools

## C PROJECT GUIDELINES

- All code must follow modern C best practices with specific requirements:
  - **Memory Management**: Use proper allocation/deallocation patterns, implement bounds checking
  - **Error Handling**: Return appropriate error codes, implement comprehensive error checking
  - **Modular Design**: Use header files, implement clear interfaces, maintain separation of concerns
  - **Compiler Flags**: Use -Wall -Wextra -Werror for development, -std=c11 or -std=c17
  - **Static Analysis**: Use tools like Clang Static Analyzer, Cppcheck, or Valgrind for memory safety
- Use established C standards (C11/C17) and reference official ISO C documentation
- All features must be covered by comprehensive testing:
  - **Unit Tests**: Minimum 80% line coverage, 70% branch coverage using Unity, CUnit, or similar
  - **Integration Tests**: All public APIs and system integrations
  - **Memory Tests**: Valgrind or similar tools for memory leak detection
  - **Performance Tests**: Response time <200ms for critical operations
- Commit messages and branches must reference Jira ticket IDs using format: "PROJ-XXX: [Action] [Component] - [Description]"
  - Example: "PROJ-123: Add buffer management module - Memory-safe implementation"
- Document platform-specific behavior with explicit compatibility matrix and testing evidence
- Example Story: "Implement Buffer Management" — Implement a C module with proper memory allocation, bounds checking, comprehensive tests, and performance benchmarks

**Code Quality Validation Checklist:**
- [ ] C11/C17 standard compliance verified using appropriate compiler flags
- [ ] Memory management patterns implemented with proper allocation/deallocation
- [ ] Error handling implemented with appropriate return codes and checking
- [ ] Modular design achieved with clear header files and interfaces
- [ ] Static analysis completed with no critical warnings
- [ ] Unit test coverage ≥80% line coverage, ≥70% branch coverage
- [ ] Memory leak testing completed using Valgrind or similar tools
- [ ] Performance benchmarks meet <200ms response time requirements
- [ ] Cross-platform compatibility verified on target platforms
- [ ] Commit messages follow "PROJ-XXX: [Action] [Component] - [Description]" format

**Error Recovery Procedures:**
- **Compilation Errors**: Analyze compiler output, fix syntax/semantic errors, verify standard compliance
- **Memory Errors**: Use debugging tools (gdb, Valgrind), implement proper error handling, add bounds checking
- **Test Failures**: Debug systematically, create regression tests, verify fix doesn't introduce new issues
- **Performance Issues**: Profile application using profiling tools, identify bottlenecks, implement optimizations, validate improvements

### C STANDARDS COMPLIANCE
- Always adhere to ISO C standards (C11/C17) and document any compiler-specific extensions used
- **Fallback Procedure**: If specific C standard features unavailable, implement portable alternatives and document compatibility requirements
- **Validation Requirements**: Verify all code compiles with multiple compilers (GCC, Clang, MSVC) and standard compliance flags
- **Context Preservation**: Store architectural decisions and design patterns in project documentation for future reference

**Standards Compliance Validation:**
- [ ] Code compiles successfully with C11/C17 standard flags
- [ ] Multiple compiler compatibility verified (GCC, Clang, MSVC)
- [ ] No compiler-specific extensions used without documentation
- [ ] Portable alternatives implemented for platform-specific features
- [ ] Compliance testing completed with strict warning flags enabled
