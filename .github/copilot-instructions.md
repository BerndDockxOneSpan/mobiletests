---
applyTo: "**"
---
#  DEVELOPMENT GUIDELINES
## PRIME DIRECTIVE
Features are writtin in Gherkin syntax, the steps are implemented in Python.

# Writing Good Gherkin
> The Golden Gherkin Rule: Treat other readers as you would want to be treated. **Write Gherkin so that people who don’t know the feature will understand it.**

Proper Behavior
---------------
The biggest mistake BDD beginners make is writing Gherkin without a behavior-driven mindset. 
They often write feature files as if they are writing “traditional” _procedure-driven_ functional tests: step-by-step instructions with actions and expected results. 
HP ALM, [qTest](https://www.qasymphony.com/software-testing-tools/qtest-manager/test-case-management/), [AccelaTest](https://accelatest.com/), and many other test repository tools store tests in this format. 
These procedure-driven tests are often _imperative_ and trace a path through the system that covers multiple behaviors. 
As a result, they may be unnecessarily long, which can delay failure investigation, increase maintenance costs, and create confusion.

For example, let’s consider a test that searches for images of pandas on Google. 
Below would be a reasonable test procedure:
```
1.  Open a web browser.
    1.  Web browser opens successfully.
2.  Navigate to https://www.google.com/.
    1.  The web page loads successfully and the Google image is visible.
3.  Enter “panda” in the search bar.
    1.  Links related to “panda” are shown on the results page.
4.  Click on the “Images” link at the top of the results page.
    1.  Images related to “panda” are shown on the results page.
```
I’ve seen many newbies translate a test like this into Gherkin like the following:

```
# BAD EXAMPLE! Do not copy.
Feature: Google Searching

  Scenario: Google Image search shows pictures
    Given the user opens a web browser
    And the user navigates to "https://www.google.com/"
    When the user enters "panda" into the search bar
    Then links related to "panda" are shown on the results page
    When the user clicks on the "Images" link at the top of the results page
    Then images related to "panda" are shown on the results page
```


This scenario is terribly wrong. 
All that happened was that the author put BDD buzzwords in front of each step of the traditional test. 
This is _not_ behavior-driven, it is still procedure-driven.

The first two steps are purely setup: they just go to Google, and they are strongly imperative. 
Since they don’t focus on the desired behavior, they can be reduced to one declarative step: “Given a web browser is at the Google home page.”
This new step is friendlier to read.

After the Given step, there are two When-Then pairs. 
This is syntactically incorrect: **Given-When-Then steps must appear in order and cannot repeat**. 
A Given may not follow a When or Then, and a When may not follow a Then. 
The reason is simple: **any single When-Then pair denotes an individual behavior**. 
This makes it easy to see how, in the test above, there are actually two behaviors covered: 
(1) searching from the search bar, and 
(2) performing an image search. 
In Gherkin, **one scenario covers one behavior**. 
Thus, there should be two scenarios instead of one. 
Any time you want to write more than one When-Then pair, write separate scenarios instead. 
(Note: Some BDD frameworks may allow disordered steps, but it would nevertheless be anti-behavioral.)

This splitting technique also reveals unnecessary behavior coverage. 
For instance, the first behavior to search from the search bar may be covered in another feature file. 
I once saw a scenario with about 30 When-Then pairs, and many were duplicate behaviors.

Do not be tempted to arbitrarily reassign step types to make scenarios follow strict Given-When-Then ordering. 
**Respect the integrity of the step types**: 
Givens set up initial state, 
Whens perform an action, and 
Thens verify outcomes. 
In the example above, the first Then step _could_ have been turned into a When step, but that would be incorrect because it makes an assertion. 
Step types are meant to be guide rails for writing good behavior scenarios.

The correct feature file would look something like this:

```
Feature: Google Searching

  Scenario: Search from the search bar
    Given a web browser is at the Google home page
    When the user enters "panda" into the search bar
    Then links related to "panda" are shown on the results page

  Scenario: Image search
    Given Google search results for "panda" are shown
    When the user clicks on the "Images" link at the top of the results page
    Then images related to "panda" are shown on the results page
```


The second behavior arguably needs the first behavior to run first because the second needs to start at the search result page. 
However, since that is merely setup for the behavior of image searching and is not part of it, the Given step in the second scenario can basically declare (_declaratively_) that the “panda” search must already be done. 
Of course, this means that the “panda” search would be run redundantly at test time, but the separation of scenarios guarantees behavior-level independence.

> The Cardinal Rule of BDD: **One Scenario, One Behavior!**

Remember, behavior scenarios are more than tests – they also represent requirements and acceptance criteria. **Good Gherkin comes from good behavior**.

Phrasing Steps
--------------
basic rules to maintain consistent phrasing and maximum reusability

**Write all steps in third-person point of view**

**Write steps as a subject-predicate action phrase** :

**use present tense for all step types**

Given steps are meant to establish an initial state, _not_ exercise a behavior. 

Choices, Choices
----------------
**However, Gherkin does not have an “Or” step**. When automated, every step is executed sequentially.

In order to cover multiple variations of the same behavior, **use Scenario Outline sections to cover multiple variations of the same behavior**, as shown below:

```
Feature: SNES Mario Controls

  Scenario Outline: Mario jumps
    Given a level is started
    When the player pushes the "<letter>" button
    Then Mario jumps straight up
    
    Examples: Buttons
      | letter |
      | A      |
      | B      |
```


The Known Unknowns
------------------
To handle the known unknowns, **write scenarios defensively so that changes in the underlying data do not cause test runs to fail**. 

Furthermore, to be truly behavior-driven, **think about data not as test data but as examples of behavior**.

Consider the following example from the previous post:

**step definitions can hide data in the automation** when it doesn’t need to be exposed. 
Step definitions may also pass data to future steps in the automation. 
For example, consider another Google search scenario:

```
Feature: Google Searching

  Scenario: Search result linking
    Given Google search results for "panda" are shown
    When the user clicks the first result link
    Then the page for the chosen result link is displayed
```
Notice how the When step does not explicitly name the value of the result link – it simply says to click the first one. 
The value of the first link may change over time, but there will always be a first link. 
The Then step must know something about the chosen link in order to successfully verify the outcome, but it can simply reference it as “the chosen result link”. 
Behind the scenes, in the step definitions, the When step can store the value of the chosen link in a variable and pass the variable forward to the Then step.

Handling Test Data
------------------
Some types of test data should be handled directly within the Gherkin, but other types should not. 
Remember that BDD is _specification by example_ – scenarios should be descriptive of the behaviors they cover, and any data written into the Gherkin should support that descriptive nature.

Less is More
------------
**Scenarios should be short and sweet**. 
I typically recommend that scenarios should have a single-digit step count (<10). 
Long scenarios are hard to understand, and they are often indicative of poor practices. 
One such problem is writing _imperative_ steps instead of _declarative_ steps. 

Declarative steps state _what_ action should happen without providing all of the information for how it will happen. 
They are behavior-driven because they express action at a higher level. 
All of the imperative steps in the example above could be written in one line: “When the user enters ‘panda’ at the search bar.” 
The scrolling and keystroking is implied, and it will ultimately be handled by the automation in the step definition. 
**When trying to reduce step count, ask yourself if your steps can be written more declaratively**.

Another reason for lengthy scenarios is scenario outline abuse. 
Scenario outlines make it all too easy to add unnecessary rows and columns to their Examples tables. 
Unnecessary rows waste test execution time. 
Extra columns indicate complexity. 
Both should be avoided. 
Below are questions to ask yourself when facing an oversized scenario outline:

*   Does each row represent an equivalence class of variations?
    *   For example, searching for “elephant” in addition to “panda” does not add much test value.
*   Does every combination of inputs need to be covered?
    *   _N_ columns with _M_ inputs each generates _MN_ possible combinations.
    *   Consider making each input appear only once, regardless of combination.
*   Do any columns represent separate behaviors?
    *   This may be true if columns are never referenced together in the same step.
    *   If so, consider splitting apart the scenario outline by column.
*   Does the feature file reader need to explicitly know all of the data?
    *   Consider hiding some of the data in step definitions.
    *   Some data may be derivable from other data.

These questions are meant to be sanity checks, not hard-and-fast rules. 
The main point is that **scenario outlines should focus on one behavior and use only the necessary variations**.

Style and Structure
-------------------
Below are a number of tidbits for good style and structure:

1.  Focus a feature on customer needs.
2.  Limit one feature per feature file. This makes it easy to find features.
3.  Limit the number of scenarios per feature. Nobody wants a thousand-line feature file. A good measure is a dozen scenarios per feature.
4.  Limit the number of steps per scenario to less than ten.
5.  Limit the character length of each step. Common limits are 80-120 characters.
6.  Use proper spelling.
7.  Use proper grammar.
8.  Capitalize Gherkin keywords.
9.  Capitalize the first word in titles.
10.  Do not capitalize words in the step phrases unless they are proper nouns.
11.  Do not use punctuation (specifically periods and commas) at the end of step phrases.
12.  Use single spaces between words.
13.  Indent the content beneath every section header.
14.  Separate features and scenarios by two blank lines.
15.  Separate examples tables by 1 blank line.
16.  Do not separate steps within a scenario by blank lines.
17.  Space table delimiter pipes (“|”) evenly.
18.  Adopt a standard set of tag names. Avoid duplicates.
19.  Write all tag names in lowercase, and use hyphens (“-“) to separate words.
20.  Limit the length of tag names.



## PYTHON  GUIDELINES
- All code must follow modern Python best practices with specific requirements:
  - **Type Hints**: All function parameters and return values must have type annotations
  - **Virtual Environments**: Use venv or conda for isolated development environments
  - **Dependency Management**: Use requirements.txt or pyproject.toml with pinned versions
  - **Error Handling**: Implement specific exception types with meaningful error messages and logging

**Error Recovery Procedures:**
- **Import Errors**: Check virtual environment activation, verify dependency installation, validate Python version compatibility
- **Test Failures**: Debug systematically, create regression tests, verify fix doesn't break existing functionality

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