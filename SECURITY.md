# Security policy

## Reporting a security issue

Do not publish credentials, session cookies, private datasets, or reproducible account-access details in a public issue.

If you discover an exposed secret:

1. revoke or rotate the credential first;
2. remove it from the current codebase;
3. report the affected path and commit without copying the secret value;
4. review repository history and downstream logs/artifacts for additional exposure.

For other security-sensitive reports, use a private GitHub security advisory when available or contact the repository maintainer through their GitHub profile.

## Credential handling

This repository must not contain live API keys, passwords, Facebook session cookies, access tokens, private keys, or populated `.env` files. Runtime credentials must be supplied through environment variables or a local secret manager.

A credential that has ever been committed to a public repository must be treated as compromised even after the file is edited or deleted.

## Collected data

OSINT output can still be sensitive. Before publishing logs, fixtures, screenshots, or sample datasets, remove personal identifiers that are not required to reproduce the issue. Tests should use synthetic fixtures wherever practical.
