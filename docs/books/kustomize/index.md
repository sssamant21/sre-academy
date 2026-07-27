# Kustomize

The Kustomize handbook will document configuration overlays and environment-specific Kubernetes customization.

## Planned chapters

- Bases, overlays, patches, and generators
- Environment promotion and configuration review
- Image updates, labels, annotations, and common transforms
- Validation, diffing, and deployment safety
- Troubleshooting broken overlays

## Starter reliability questions

1. Which fields should differ by environment?
2. How do we verify the rendered manifests before applying them?
3. What signals show an overlay has drifted from the base intent?
