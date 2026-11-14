# portability — Rust transition plan

Status: proposed; no Loom Rust implementation or deployment is performed by this document.

Baseline: `4d93ab9bdcb5750f3d0be161925e834984492f89` (Loom alpha.60).

## Decision and sequence

- Target: Rust read/write compatibility for preserved records and fences; retained operator migration tools.
- Sequence: 1 preservation fixtures; 7 migration/rollback acceptance.
- Existing feature dependencies: identity, catalog, results, execution.

## Current source and authority

Preserved data, Job migration and remote ownership. The implemented contract is in the linked source and [portability feature specification](../../features/portability.md).

| File | Planning treatment |
|---|---|
| [deploy/assign-owner.py](../../../deploy/assign-owner.py) | Inspect domain/consumer boundary; port only the selected core responsibility |
| [ops/portability.py](../../../ops/portability.py) | Inspect domain/consumer boundary; port only the selected core responsibility |
| [ops/remote-handoff.py](../../../ops/remote-handoff.py) | Inspect domain/consumer boundary; port only the selected core responsibility |
| [ops/remote_fence.py](../../../ops/remote_fence.py) | Inspect domain/consumer boundary; port only the selected core responsibility |

## Retained code and external dependencies

Keep snapshot/archive tooling and explicit operator-owned transfer workflows until Rust state compatibility is proven. Never migrate research bytes or issue new identities as a side effect of the port.

## Compatibility invariants

- Distinguish original preservation from current presentation and retain installation identifiers. Cloned installations running concurrently require distinct identities.
- Preserve existing IDs, authentication, configured roots, sealed bytes and operational history unless an explicit separate schema change is approved.
- Keep missing, null, false, zero, unknown, stale and unavailable distinctions required by this block.
- Development checks are evidence, not extra Job or agent-ACK execution gates.

## Detailed implementation work

1. Inventory immutable original snapshots versus mutable attribution/presentation overlays and exact installation/storage IDs.
2. Capture representative old-schema Ops/executor/Runtime databases with synthetic or explicitly sanitized data; retain original request and content hashes.
3. Port remote ownership grants/fencing with stable epoch/expiry semantics and a single active execution authority.
4. Keep clone identity rules: two running installations require independent identities; restoring one installation must preserve its own accepted references.
5. Validate locator resolution and selective migration exclusions without inferring paths from another host.
6. Compare row counts and normalized row hashes before/after a no-op Rust open and a controlled approved mutation.
7. Exercise upgrade and rollback using the same storage/settings/credentials and resolve unreturned execution before any ownership transfer.
8. Keep a recoverable previous executable/image/source and preservation receipt; do not automatically delete the original archive.

## Acceptance matrix

| Scenario | Required observable result |
|---|---|
| No-op open of an existing database | No historical payload, identity or pin rewrite. |
| Old snapshot hash differs from a later live DB | Keep distinct evidence; no automatic replacement. |
| Two workers claim a remote execution authority | Reject stale/duplicate owner rather than overlap. |
| Selective migration excludes an operational fixture | Retain references and original archive evidence consistently. |
| Secondary store is moved with the same logical ID | Verify marker/grants and exact referenced bytes. |
| Rollback after an uncertain external action | Preserve its unresolved ownership and original operation key. |

### Existing regression sources

- [tests/ops/test_remote_ownership.py](../../../tests/ops/test_remote_ownership.py)
- [tests/deploy/test_boot_readiness.py](../../../tests/deploy/test_boot_readiness.py)

Existing Python-internal tests need boundary adaptation when their implementation moves. Passing the old implementation alone does not establish Rust parity. Add state/trace and crash cases from this matrix; keep actual external acceptance separately identified.

## State, cutover and rollback

Run preservation checks before switching and compare again afterward. Retain all installation-specific state independently; never use another machine's state as a template.

## Main risk and design review

A language migration is not a new-machine installation. Treating it as reinstall-and-import would unnecessarily threaten credentials, storage IDs and historical references.

## Contracts and documentation to review

- [ops/portability.py](../../../ops/portability.py)
- [ops/remote_fence.py](../../../ops/remote_fence.py)

Change rule: When migration changes, check locator/storage IDs, original hashes, ownership overlays, selective exclusions and rerun idempotency.

Before implementation, apply the cross-block [compatibility contract](../COMPATIBILITY.md), [sequence and ownership rules](../README.md), and [whole-tree review findings](../REVIEW.md). Update the implementation source, public schema/guide, consumers and installation packaging together when an accepted contract changes.

## Exit criteria

- The implemented responsibilities and deliberately retained Python/external boundaries are explicit.
- Every acceptance row has a reproducible test or is named as an unverified external acceptance boundary.
- Affected consumers pass against the selected Rust implementation, including its error and restart paths.
- Preservation and rollback checks use the same state format/identities; no second writer or duplicated external action is introduced.
- Feature mappings and source-qualified verification evidence match the exact candidate build.
- No production activation, user-thread inference, credential rotation or research execution is inferred from source/test completion.
