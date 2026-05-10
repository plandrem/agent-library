# Create git worktree

Create a new git worktree under the folder `worktrees/` (create this folder if it does not exist). Use the branch name "$ARGUMENTS". If the branch name is prefixed, e.g. `patrick/my-new-branch`, create a subfolder:

```
worktrees/
  patrick/
    my-new-branch/
      <- repository files ->
```

All work should be done within this worktree unless otherwise specified.

## dotenv files
Use ls -la to check for the existence of a `.env` file in the repository root. if there is such a file, copy that file into the worktree working folder. 