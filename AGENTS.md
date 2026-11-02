# Agent Rules

## Environment

- Use the workspace `.venv`, `venv`, or `env`; never install globally.
- Preserve `.env` and other secret/config files. Never expose, commit, delete, rename, or overwrite them.

## Changes

- Follow existing project patterns and configuration.
- Make focused, type-safe changes; handle errors explicitly.
- Update directly related tests and documentation.

## Verification

- Run the smallest relevant formatter, linter, type check, or test if there is any available.

