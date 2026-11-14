# api — Rust transition plan

Status: proposed; no Loom Rust implementation or deployment is performed by this document.

Baseline: `4d93ab9bdcb5750f3d0be161925e834984492f89` (Loom alpha.60).

## Decision and sequence

- Target: Rust domain routing and eventually loom-ops HTTP/MCP surface; retain external authentication/validation bridges until parity.
- Sequence: 1 public contract capture; 6 endpoint cutover.
- Existing feature dependencies: identity, queue, execution, recovery, results, extensions, catalog, diagnostics.

## Current source and authority

Public HTTP/MCP contracts and request routing. The implemented contract is in the linked source and [api feature specification](../../features/api.md).

| File | Planning treatment |
|---|---|
| [ops/job_contract.py](../../../ops/job_contract.py) | Inspect domain/consumer boundary; port only the selected core responsibility |
| [ops/mcp_docs.py](../../../ops/mcp_docs.py) | Inspect domain/consumer boundary; port only the selected core responsibility |
| [ops/mcp_groups.py](../../../ops/mcp_groups.py) | Inspect domain/consumer boundary; port only the selected core responsibility |
| [ops/ops.py](../../../ops/ops.py) | Inspect domain/consumer boundary; port only the selected core responsibility |
| [ops/serve.py](../../../ops/serve.py) | Inspect domain/consumer boundary; port only the selected core responsibility |

## Retained code and external dependencies

Keep all Dashboard consumers and Loom Use alpha.9 compatibility initially. Retain the established Python JSON Schema validator behind a narrow private boundary until draft/format/error parity is demonstrated.

## Compatibility invariants

- HTTP and the six MCP groups invoke the same operations. Distinguish request acceptance from successful execution.
- Preserve existing IDs, authentication, configured roots, sealed bytes and operational history unless an explicit separate schema change is approved.
- Keep missing, null, false, zero, unknown, stale and unavailable distinctions required by this block.
- Development checks are evidence, not extra Job or agent-ACK execution gates.

## Detailed implementation work

1. Capture tools/list, system.describe, guide indexes and every action schema from mcp_groups.py, job_contract.py and mcp_docs.py for each scope combination.
2. Split ops.py by responsibility on paper before moving functions: submit/query/HTTP routing, worker, finish, schema initialization and process execution belong to different internal Rust modules.
3. Define typed request envelopes with strict new-request validation while preserving unknown fields in retained historical/sealed JSON. Preserve omitted-versus-null and boolean-versus-integer behavior.
4. Implement one domain operation dispatcher used by grouped HTTP and the six MCP groups. Never duplicate Job mutation logic in an HTTP handler or SDK wrapper.
5. Preserve JSON-RPC IDs, notifications, initialization/version negotiation, SSE/JSON response forms and grouped /api/actions behavior. Map domain conflicts and access errors to the existing public error categories.
6. Keep Dashboard relay route allowlists separate from Ops routes; do not expose an unrestricted API proxy when replacing the backend.
7. Run black-box requests against isolated Python and Rust services and compare normalized results, rejected inputs and durable effects. Exclude generated IDs/timestamps only with documented normalization.
8. Advertise the same public API revision only if all existing observable contracts pass. Use a new revision for any deliberately accepted incompatible change rather than silently changing fields.

## Acceptance matrix

| Scenario | Required observable result |
|---|---|
| Same stable submit key after a recovery edit | Return the original Job using revision-zero request/default semantics. |
| Unknown action, extra argument or wrong scalar type | Match current validation/error behavior. |
| HTTP and MCP equivalent mutation | Produce the same durable transition and error classification. |
| JSON-RPC notification without an ID | Preserve notification semantics; no fabricated result. |
| Caller with read scope only | Discover permitted schemas without mutation capabilities. |
| Large discovery payload | Retain bounded summaries and exact-detail retrieval; fit the pinned client transport limit. |

### Existing regression sources

- [tests/ops/test_api_contract.py](../../../tests/ops/test_api_contract.py)
- [tests/ops/test_mcp_docs.py](../../../tests/ops/test_mcp_docs.py)
- [tests/ops/test_job_contract.py](../../../tests/ops/test_job_contract.py)
- [tests/ops/test_generic_agent.py](../../../tests/ops/test_generic_agent.py)
- [tests/ops/test_initialization.py](../../../tests/ops/test_initialization.py)
- [tests/ops/test_job_lifecycle.py](../../../tests/ops/test_job_lifecycle.py)

Existing Python-internal tests need boundary adaptation when their implementation moves. Passing the old implementation alone does not establish Rust parity. Add state/trace and crash cases from this matrix; keep actual external acceptance separately identified.

## State, cutover and rollback

Switch the authoritative endpoint only after domain and client parity. Preserve URLs, trust configuration and guide/client pins; route an isolated test instance to Rust before any production proposal.

## Main risk and design review

A Rust HTTP framework does not reproduce application/MCP semantics automatically. Several static action lists in overview documentation lag the executable registry.

## Contracts and documentation to review

- [ops/job_contract.py](../../../ops/job_contract.py)
- [ops/mcp_groups.py](../../../ops/mcp_groups.py)
- [ops/mcp_docs.py](../../../ops/mcp_docs.py)

Change rule: When public inputs or responses change, check schemas, examples, API revision, guides and Dashboard consumers. Since ops.py contains multiple feature entry points, narrow impact to the affected functions.

Before implementation, apply the cross-block [compatibility contract](../COMPATIBILITY.md), [sequence and ownership rules](../README.md), and [whole-tree review findings](../REVIEW.md). Update the implementation source, public schema/guide, consumers and installation packaging together when an accepted contract changes.

## Exit criteria

- The implemented responsibilities and deliberately retained Python/external boundaries are explicit.
- Every acceptance row has a reproducible test or is named as an unverified external acceptance boundary.
- Affected consumers pass against the selected Rust implementation, including its error and restart paths.
- Preservation and rollback checks use the same state format/identities; no second writer or duplicated external action is introduced.
- Feature mappings and source-qualified verification evidence match the exact candidate build.
- No production activation, user-thread inference, credential rotation or research execution is inferred from source/test completion.
