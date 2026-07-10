# Install

```console
pnpm add -D @commitlint/cli @commitlint/config-conventional
```

# Configuration
Configure commitlint to use conventional config
```console
module.exports = { extends: ['@commitlint/config-conventional'] };
```

# Add hook
To use commitlint you need to setup commit-msg hook

```console
pnpm add --save-dev husky
# husky@v9
pnpm husky init
# husky@v8 or lower
pnpm husky install
# Add commit message linting to commit-msg hook
echo "pnpm dlx commitlint --edit \$1" > .husky/commit-msg
```

# Test simple usage
For a first simple usage test of commitlint you can do the following:
```console
pnpm commitlint --from HEAD~1 --to HEAD --verbose
```
This will check your last commit and return an error if invalid or a positive output if valid.
# Test the hook
You can test the hook by simply committing. You should see something like this if everything works
## Invalid commit
```console
git commit -m "foo: this will fail"
#  husky > commit-msg
No staged files match any of provided globs.
⧗   --- input ---
foo: this will fail
✖   type must be one of [build, chore, ci, docs, feat, fix, perf, refactor, revert, style, test] [type-enum]

✖   found 1 problems, 0 warnings
ⓘ   Get help: https://github.com/conventional-changelog/commitlint/#what-is-commitlint

husky - commit-msg script failed (code 1)
```
## Valid commit
```console
git commit -m "chore: lint on commitmsg"
# husky > pre-commit
No staged files match any of provided globs.
# husky > commit-msg
```
# References

- Commitlint: 
https://commitlint.js.org/guides/local-setup.html
- Conventional Commits:
https://www.conventionalcommits.org/en/v1.0.0/