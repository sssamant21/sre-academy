# Service Mesh

!!! note "Preserved reference"
    Service mesh guidance is now documented inside the Networking handbook. New content should be added to `books/networking/service-mesh/` topics in the navigation.

The Service Mesh reference covers Istio-focused service-to-service traffic management and reliability practices.

## Planned chapters

- Mesh architecture, sidecars, gateways, and control planes
- Traffic policies, retries, timeouts, and circuit breaking
- mTLS, identity, authorization, and policy
- Observability, tracing, and traffic debugging
- Operational runbooks for mesh incidents

## Starter reliability questions

1. Which services depend on mesh traffic policies?
2. How do we detect proxy, certificate, or control plane failures?
3. What is the rollback path for a bad mesh configuration?
