# Execute tasks in parallel

You are going to create a number of agents who will each perform the same task on a different git worktree. Follow these steps exactly:

1. Create a new worktree for each worker using the structure `<project root>/trees/<feature name>_<agent_number>`
2. Copy any critical files that are not tracked within the repository into the appropriate location in the worktree folders. The goal is to preserve the path structure of the original repo.
3. Provide the task instructions to each agent
4. Launch the agents
5. Provide a summary of the approach and outcome for each agent

## Task Instructions:

```
1. Review README.md (if present) and use git ls-tree to review the file structure for this project.
2. $ARGUMENTS
3. Document your entire process in file RESULTS.md (this file must never be commited to git).
```

## Number of workers to create: 
$ARGUMENTS