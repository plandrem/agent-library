# Run monolithic-first code execution workflow

## Variables:

SPEC_FILE = $ARGUMENTS

## Summary of Workflow

1. Read SPEC_FILE

2. Pass SPEC_FILE to TEST_ARCHITECT. Output = comprehensive test plan file with TEST_CASES covering all functionality

3. Pass TEST_ARCHITECT test plan to REVIEWER. Output = approval or feedback for test cases

If rejected, return feedback to TEST_ARCHITECT. Repeat until approved.

3a. Pause to ask USER to review the TEST_ARCHITECT's proposal. If approved, proceed to 4. If rejected, return feedback to TEST_ARCHITECT. Repeat until approved.

4. Pass approved TEST_CASES to TEST_ENGINEER. Output = complete test file implementation.

4a. Pass TEST_ENGINEER test implementation to REVIEWER. Output = approval or feedback for test implementation.

If rejected, return feedback to TEST_ENGINEER. Repeat until approved.

5. Pass approved TEST_CASES and test file to CODE_ENGINEER. Output = **COMPLETE MONOLITHIC IMPLEMENTATION** in a single file containing all required functionality.

6. Pass SPEC_FILE, TEST_CASES, and MONOLITHIC CODE to REVIEWER. Output = approval or feedback for monolithic implementation

If rejected, return feedback to CODE_ENGINEER. Repeat until approved.

7. Pass approved monolithic code to REFACTOR_AGENT. Output = atomic filesystem structure with functionally equivalent code.

8. Pass refactored code to REVIEWER. Output = approval or feedback for refactored atomic structure

If rejected, return feedback to REFACTOR_AGENT. Repeat until approved.

9. Inform the user that changes are ready for review. Address any questions or feedback from the user until told to proceed.

10. Commit all changes to the current git branch and push if there is a remote repository.

**WORKFLOW COMPLETE** - Single pass implementation with no iteration.

## Why this process?

This monolithic-first approach allows complete functionality to be implemented and tested in one comprehensive file before being refactored into the optimal atomic structure. This eliminates the complexity of iterative development while ensuring all requirements are fully met.

## Notes on running the process

- If any of your agents are unclear on their instructions, raise the question to the user. This is **especially** true if there are decisions around code functionality, handling undefined cases, user experience...
- All functionality must be implemented before any refactoring begins

## Version Control

Before running the process, create a new local branch with name `monolithic_implementation/{feature_name}`. Commit all files created by the agents to this branch after each major phase has completed their task. Use minimal commit messages, and NEVER include any suggestion that Claude or Anthropic is involved in the commit. Good examples would include:

- {feature_name}: add test plan
- {feature_name}: add test implementation  
- {feature_name}: add monolithic implementation
- {feature_name}: add refactored atomic structure

Merge the branch into the main branch when the complete workflow is finished.