# Helm

!!! note "Preserved reference"
    Helm is now documented inside the Enterprise Kubernetes handbook. New content should be added to `books/kubernetes/helm/` in the navigation.

The Helm reference covers reliable package management for Kubernetes applications.

## Planned chapters

- Chart structure, values, and templating basics
- Release lifecycle, upgrades, rollbacks, and history
- Dependency management and chart repositories
- Secrets, environment configuration, and promotion safety
- Testing, linting, and operational runbooks

## Starter reliability questions

1. How do we validate chart changes before deployment?
2. What rollback path exists for a failed release?
3. Which values are environment-specific and risk-sensitive?
