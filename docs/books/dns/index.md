# DNS

!!! note "Preserved reference"
    DNS is now documented inside the Networking handbook. New content should be added to `books/networking/dns/` in the navigation.

The DNS reference covers reliable name resolution and traffic discovery practices.

## Planned chapters

- Records, zones, resolvers, and delegation
- TTLs, caching, propagation, and failover
- Split-horizon DNS and private zones
- Monitoring, validation, and troubleshooting
- Operational runbooks for DNS incidents

## Starter reliability questions

1. Which records are critical for production traffic?
2. How do TTLs affect incident response and rollback?
3. How do we detect resolver or delegation failures?
