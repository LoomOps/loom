# catalog — Rust transition plan

Status: proposed; no Loom Rust implementation or deployment is performed by this document.

Baseline: `4d93ab9bdcb5750f3d0be161925e834984492f89` (Loom alpha.60).

## Decision and sequence

- Target: Rust catalog/history/Job projection domain; unchanged Dashboard UI.
- Sequence: 3 read-only projection parity; 5 overlay writes.
- Existing feature dependencies: identity, results, queue.

## Current source and authority

Catalog, preserved records and file access. The implemented contract is in the linked source and [catalog feature specification](../../features/catalog.md).

| File | Planning treatment |
|---|---|
| [ops/dashboard_read.py](../../../ops/dashboard_read.py) | Inspect domain/consumer boundary; port only the selected core responsibility |
| [ops/history_store.py](../../../ops/history_store.py) | Inspect domain/consumer boundary; port only the selected core responsibility |
| [ops/job_history.py](../../../ops/job_history.py) | Inspect domain/consumer boundary; port only the selected core responsibility |
| [ops/research.py](../../../ops/research.py) | Inspect domain/consumer boundary; port only the selected core responsibility |

## Retained code and external dependencies

Keep workspace rendering, producer metadata, historical payloads and independent reconciliation evidence. This port does not implement the separately discussed general-purpose reconciler.

## Compatibility invariants

- Distinguish historical originals from current display overlays. Never assume missing files are valid artifacts.
- Preserve existing IDs, authentication, configured roots, sealed bytes and operational history unless an explicit separate schema change is approved.
- Keep missing, null, false, zero, unknown, stale and unavailable distinctions required by this block.
- Development checks are evidence, not extra Job or agent-ACK execution gates.

## Detailed implementation work

1. Capture the current combined projection of native records, historical snapshots, execution Profiles, Runtime/Dependency catalogs and real queue consumers.
2. Port historical record lookup without modifying recorded availability, original locations or payloads; current availability remains an additive observation.
3. Port research/main/support/operations overlays, explicit consolidation and workflow aggregates while retaining direct access to every constituent execution.
4. Preserve logical Job elapsed timelines, unioned execution intervals, internal steps and Attempt counts as different quantities.
5. Port bounded file/media lookup using registered locators and current grant/identity checks, including partial/stale/unverified distinctions.
6. Preserve projection revision hashing and deterministic ordering sufficiently for refresh behavior and cached view invalidation.
7. Compare normalized full catalog and direct detail responses against preserved synthetic snapshot fixtures, including old schemas and inaccessible files.
8. Exercise unchanged browser routes for list and detail; API-only success is insufficient for Activity, queue summaries and lazy metadata.

## Acceptance matrix

| Scenario | Required observable result |
|---|---|
| Historical file has a verified relocated copy | Show current evidence without rewriting the historical original. |
| Source ref has no attached locator | not_connected is distinct from deletion. |
| Canonical Job groups 13 prior executions | Keep individual Attempts and the complete verified timeline. |
| Research view hides operations fixtures | Queue resources and direct evidence remain accessible. |
| Dataset count zero versus N/A versus absent | Preserve all three meanings in list and detail. |
| File exceeds preview/hash threshold | Return the existing bounded/unverified state, not a false pass. |

### Existing regression sources

- [tests/ops/test_job_history.py](../../../tests/ops/test_job_history.py)
- [tests/ops/test_dashboard_resources.py](../../../tests/ops/test_dashboard_resources.py)
- [tests/ops/test_file_preview.py](../../../tests/ops/test_file_preview.py)
- [tests/ops/test_history_availability.py](../../../tests/ops/test_history_availability.py)
- [tests/ops/test_job_lifecycle.py](../../../tests/ops/test_job_lifecycle.py)

Existing Python-internal tests need boundary adaptation when their implementation moves. Passing the old implementation alone does not establish Rust parity. Add state/trace and crash cases from this matrix; keep actual external acceptance separately identified.

## State, cutover and rollback

Start with read-only shadow comparisons, never reindex or reconnect operational records during planning/parity. Historical rows and bytes are rollback invariants; future locator-binding features require a separate approved contract.

## Main risk and design review

A cleaner-looking catalog must not manufacture completion, execution history, ownership or semantic validity. Projection changes can break the UI even when core Job execution works.

## Contracts and documentation to review

- [ops/dashboard_read.py](../../../ops/dashboard_read.py)
- [ops/history_store.py](../../../ops/history_store.py)

Change rule: When projections change, check revision refresh, detail queries, file MIME/size/path boundaries and the UI. Review the full installation doctor and step exit criteria when this feature changes; a local health response does not establish user-facing readiness.

Before implementation, apply the cross-block [compatibility contract](../COMPATIBILITY.md), [sequence and ownership rules](../README.md), and [whole-tree review findings](../REVIEW.md). Update the implementation source, public schema/guide, consumers and installation packaging together when an accepted contract changes.

## Exit criteria

- The implemented responsibilities and deliberately retained Python/external boundaries are explicit.
- Every acceptance row has a reproducible test or is named as an unverified external acceptance boundary.
- Affected consumers pass against the selected Rust implementation, including its error and restart paths.
- Preservation and rollback checks use the same state format/identities; no second writer or duplicated external action is introduced.
- Feature mappings and source-qualified verification evidence match the exact candidate build.
- No production activation, user-thread inference, credential rotation or research execution is inferred from source/test completion.
