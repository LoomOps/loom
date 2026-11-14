# diagnostics — Rust transition plan

Status: proposed; no Loom Rust implementation or deployment is performed by this document.

Baseline: `4d93ab9bdcb5750f3d0be161925e834984492f89` (Loom alpha.60).

## Decision and sequence

- Target: Retained private collector initially; Rust sanitized error producers.
- Sequence: 1 error envelope; every phase acceptance.
- Existing feature dependencies: none.

## Current source and authority

Private bounded local error collection; no remote telemetry. The implemented contract is in the linked source and [diagnostics feature specification](../../features/diagnostics.md).

| File | Planning treatment |
|---|---|
| [dashboard/diagnostics.py](../../../dashboard/diagnostics.py) | Inspect domain/consumer boundary; port only the selected core responsibility |
| [ops/compose.diagnostics.yaml](../../../ops/compose.diagnostics.yaml) | Inspect domain/consumer boundary; port only the selected core responsibility |

## Retained code and external dependencies

Keep the current bounded collector, diagnostics volume ownership and optional independent client collection. Do not introduce telemetry upload or a new operational gate.

## Compatibility invariants

- Collection failures never block authentication, Jobs or responses. No secret/request/exception-message capture and no automatic upload.
- Preserve existing IDs, authentication, configured roots, sealed bytes and operational history unless an explicit separate schema change is approved.
- Keep missing, null, false, zero, unknown, stale and unavailable distinctions required by this block.
- Development checks are evidence, not extra Job or agent-ACK execution gates.

## Detailed implementation work

1. Freeze diagnostic incident UUID and public error locator fields used across Ops, Dashboard and clients.
2. Create a Rust error taxonomy separating input/scope/conflict/unavailable/internal errors; public errors use product-defined messages rather than Debug/source exception text.
3. Send only the current allowlisted bounded diagnostic fields to the protected collector/file boundary.
4. Preserve local retention, file modes, size limits and unavailable-collector behavior. Log failures must not break authentication, Jobs or responses.
5. Check every new Rust process and bridge for accidental stdout/stderr exposure of tokens, request bodies, environment, SQL parameters or private paths.
6. Keep engine/build identity in diagnostics accurate without embedding host configuration or operational snapshots in release source.
7. Test matching opaque locators across Rust API and retained Dashboard/Loom Use/Pale decoding.
8. Validate collector packaging/mount permissions with the immutable Rust image and a disposable installation.

## Acceptance matrix

| Scenario | Required observable result |
|---|---|
| Malformed input contains a token-like secret | Public response/log contains no rejected value or raw exception. |
| Collector is missing, full or unwritable | Primary request behavior remains correct. |
| Upstream error includes a malformed incident ID | Discard it; preserve only validated opaque UUIDs. |
| Rust binary panics or bridge loses a reply | Sanitized failure plus accurate uncertainty; no automatic replay. |
| Diagnostic body exceeds limits | Bound collection and retention without blocking work. |
| Build identity differs from selected source | Report accurate provenance rather than borrowing another process's version. |

### Existing regression sources

- [tests/dashboard/test_diagnostics.py](../../../tests/dashboard/test_diagnostics.py)

Existing Python-internal tests need boundary adaptation when their implementation moves. Passing the old implementation alone does not establish Rust parity. Add state/trace and crash cases from this matrix; keep actual external acceptance separately identified.

## State, cutover and rollback

Retain the collector and private mount. Add sanitized Rust producers first and verify failure isolation; rollback never requires uploading or publishing private evidence.

## Main risk and design review

Rust error chains and convenient Debug logging can leak more than the existing sanitized Python boundary. Error improvements must not become a telemetry expansion.

## Contracts and documentation to review

- [dashboard/diagnostics.py](../../../dashboard/diagnostics.py)

Change rule: Review every caller, image packaging, private volume ownership and independent Loom Use collector schema before changing collection fields.

Before implementation, apply the cross-block [compatibility contract](../COMPATIBILITY.md), [sequence and ownership rules](../README.md), and [whole-tree review findings](../REVIEW.md). Update the implementation source, public schema/guide, consumers and installation packaging together when an accepted contract changes.

## Exit criteria

- The implemented responsibilities and deliberately retained Python/external boundaries are explicit.
- Every acceptance row has a reproducible test or is named as an unverified external acceptance boundary.
- Affected consumers pass against the selected Rust implementation, including its error and restart paths.
- Preservation and rollback checks use the same state format/identities; no second writer or duplicated external action is introduced.
- Feature mappings and source-qualified verification evidence match the exact candidate build.
- No production activation, user-thread inference, credential rotation or research execution is inferred from source/test completion.
