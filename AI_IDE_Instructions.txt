# AI IDE Instructions

## Overview
This document provides guidelines for using the AI IDE (Cursor/Windsurf) effectively. Follow these instructions to maintain code quality and consistency.

## General Principles
- **Always prefer Simple Solutions**: Opt for straightforward solutions whenever possible.
- **Avoid duplication of code**: Check for existing similar code before creating new code.
- **Ensure proper separation between Dev/Test/Prod environments**: Maintain clear boundaries between different environments.

## Code Changes
- **Only make changes that are requested or well understood**: Avoid unnecessary modifications.
- **When fixing issues, do not introduce new patterns or technologies**: Exhaust all existing options first.
- **Keep the code base clean and organized**: Maintain a tidy and well-structured codebase.

## Code Practices
- **Avoid writing scripts and files if possible**: Especially if the script is likely to be run only once.
- **Refactor files over 200-300 lines**: Keep files concise and manageable.
- **Do not use mock data for Dev or Prod**: Only use mock data in test environments.
- **Never add stubbing or fake data patterns**: Avoid these in Dev and Prod environments.

## Environment and Tools
- **Don't overwrite .env files**: Preserve environment configurations.
- **Use specific tech stack**: Python for the back end, HTML/JS for the front end, SQL database (never JSON file storage).

## Testing and Architecture
- **Focus only on code relevant to the task**: Avoid unnecessary code.
- **Write thorough tests for all major functionality**: Ensure comprehensive testing.
- **Avoid major architectural changes unless instructed**: Stick to the existing architecture unless changes are explicitly requested.

## Considerations
- **Consider what other methods might be affected by code changes**: Be mindful of the impact of your changes on other parts of the codebase.

## Configuration for AI Agents in the IDE

To set up the AI IDE (Cursor/Windsurf) for agents, follow these instructions:

1. **Agent Configuration**:
   - Define agent roles and responsibilities within the IDE.
   - Configure agent-specific settings and preferences.
2. **Environment Management**:
   - Assign agents to specific environments (Development, Testing, Production) based on their roles.
   - Ensure agents have access to the necessary environment configurations.
3. **Access Control**:
   - Set up permissions and access levels for agents to ensure security and proper workflow.
4. **Integration with Tools**:
   - Enable agents to use integrated tools and plugins within the IDE for enhanced productivity.
5. **Monitoring and Logging**:
   - Implement monitoring tools to track agent activities and performance.
   - Set up logging to capture agent interactions and changes made within the IDE.

By configuring these aspects, you can optimize the IDE for AI agents, facilitating efficient and secure operations. 