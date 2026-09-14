# Contributing

Keep changes small enough to review and verify. This project includes browser automation, third-party APIs, local visualization code, and legacy directories, so unrelated cleanup should not be mixed into functional changes.

## Before opening a pull request

- Do not commit `.env` files, credentials, cookies, generated datasets, or browser profiles.
- Run the affected command locally and describe what you verified.
- Keep third-party API behavior behind clearly named helpers.
- Prefer synthetic fixtures over real user data in tests and examples.
- Preserve the existing CLI workflow unless the change includes migration notes.
- Update documentation when configuration or output format changes.

## Python style

Use Python 3.8+ compatible syntax, four-space indentation, descriptive function names, and `sys.executable` when launching another Python process. Avoid `shell=True` unless shell features are genuinely required.

## Commit messages

Use short, scoped messages such as:

```text
security: remove embedded API credential
fix: validate API menu selection
docs: document check-in component setup
```

## Security-sensitive changes

Follow `SECURITY.md`. Do not paste a live secret into an issue, pull request description, commit message, or test fixture, even when demonstrating that a leak has been fixed.
