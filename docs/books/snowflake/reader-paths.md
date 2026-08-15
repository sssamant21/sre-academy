# Snowflake Enterprise Handbook Reader Paths

Version: v1.1.0  
Status: In development  
Last reviewed: 2026-08-15

Use these paths to reach a practical outcome without reading all 20 chapters sequentially. Chapter numbers link to the existing production handbook.

## Choose by role

| Role | Recommended sequence | Intended outcome |
|---|---|---|
| Enterprise architect | [1](chapter-01/README.md) → [2](chapter-02/README.md) → [8](chapter-08/README.md) → [12](chapter-12/README.md) → [19](chapter-19/README.md) → [20](chapter-20/README.md) | Establish platform boundaries, governance and reference architecture |
| DBA or platform administrator | [6](chapter-06/README.md) → [8](chapter-08/README.md) → [9](chapter-09/README.md) → [10](chapter-10/README.md) → [11](chapter-11/README.md) → [17](chapter-17/README.md) | Operate warehouses, access, monitoring, cost and incidents |
| SRE or production engineer | [6](chapter-06/README.md) → [9](chapter-09/README.md) → [11](chapter-11/README.md) → [13](chapter-13/README.md) → [16](chapter-16/README.md) → [18](chapter-18/README.md) | Build observable services and repeatable incident response |
| Performance engineer | [3](chapter-03/README.md) → [4](chapter-04/README.md) → [5](chapter-05/README.md) → [7](chapter-07/README.md) → [14](chapter-14/README.md) | Diagnose scan, execution, concurrency and SQL bottlenecks |
| Security engineer | [1](chapter-01/README.md) → [8](chapter-08/README.md) → [12](chapter-12/README.md) → [17](chapter-17/README.md) → [20](chapter-20/README.md) | Design identity, least privilege, governance and deployment controls |
| FinOps engineer | [5](chapter-05/README.md) → [6](chapter-06/README.md) → [9](chapter-09/README.md) → [10](chapter-10/README.md) → [15](chapter-15/README.md) | Attribute consumption, detect waste and govern spend |
| Application or data engineer | [1](chapter-01/README.md) → [2](chapter-02/README.md) → [4](chapter-04/README.md) → [5](chapter-05/README.md) → [11](chapter-11/README.md) → [14](chapter-14/README.md) | Develop efficient, supportable Snowflake workloads |

## Choose by objective

- **Investigate a slow query:** Chapters [4](chapter-04/README.md), [5](chapter-05/README.md), [7](chapter-07/README.md) and the [query-profile lab](labs/query-profile-and-pruning.md).
- **Resolve warehouse queuing:** Chapters [6](chapter-06/README.md), [9](chapter-09/README.md) and the [warehouse-queuing runbook](runbooks/warehouse-queuing.md).
- **Control unexpected spend:** Chapters [9](chapter-09/README.md), [10](chapter-10/README.md) and the [credit-spike runbook](runbooks/unexpected-credit-consumption.md).
- **Prepare for production:** Chapters [8](chapter-08/README.md), [11](chapter-11/README.md), [17](chapter-17/README.md), [19](chapter-19/README.md) and [20](chapter-20/README.md).
- **Build platform automation:** Chapters [12](chapter-12/README.md), [18](chapter-18/README.md) and [19](chapter-19/README.md).

## Learning levels

1. **Foundation:** Chapters 1–4, then complete the query-profile lab.
2. **Operations:** Chapters 6, 8–11 and the two initial runbooks.
3. **Advanced engineering:** Chapters 12–20, with emphasis determined by role.

The paths are recommendations, not prerequisites. Follow the chapter links when a lab or runbook identifies a concept that needs deeper context.
