# testing — Rust transition plan

Status: proposed; no Loom Rust implementation or deployment is performed by this document.

Baseline: `4d93ab9bdcb5750f3d0be161925e834984492f89` (Loom alpha.60).

## Decision and sequence

- Target: Retain Python/Firefox harnesses; add Rust unit/property/contract and fault-injection suites.
- Sequence: 0 review baseline; every subsequent phase.
- Existing feature dependencies: none.

## Current source and authority

Feature specifications, impact analysis and isolated test tools. The implemented contract is in the linked source and [testing feature specification](../../features/testing.md).

| File | Planning treatment |
|---|---|
| [tests/dashboard/mock_ops.py](../../../tests/dashboard/mock_ops.py) | Retain interface/tooling; review exact bridge and packaging behavior |
| [tests/dashboard/verify_browser.py](../../../tests/dashboard/verify_browser.py) | Retain interface/tooling; review exact bridge and packaging behavior |
| [tests/dashboard/verify_workspace.py](../../../tests/dashboard/verify_workspace.py) | Retain interface/tooling; review exact bridge and packaging behavior |
| [deploy/features.py](../../../deploy/features.py) | Retain interface/tooling; review exact bridge and packaging behavior |
| [tests/suite.py](../../../tests/suite.py) | Retain interface/tooling; review exact bridge and packaging behavior |
| [tests/run.py](../../../tests/run.py) | Retain interface/tooling; review exact bridge and packaging behavior |
| [tests/ops/test_support.py](../../../tests/ops/test_support.py) | Retain interface/tooling; review exact bridge and packaging behavior |
| [tests/README.md](../../../tests/README.md) | Retain interface/tooling; review exact bridge and packaging behavior |
| [deploy/TESTING.md](../../../deploy/TESTING.md) | Retain interface/tooling; review exact bridge and packaging behavior |

## Retained code and external dependencies

Keep existing pytest/unittest fixtures, browser automation, feature ownership catalog and isolated integration tooling. Porting tests wholesale to Rust would remove a useful independent implementation boundary.

## Compatibility invariants

- Development validation adds no new gates to Job execution. Distinguish test results from actual deployment state.
- Preserve existing IDs, authentication, configured roots, sealed bytes and operational history unless an explicit separate schema change is approved.
- Keep missing, null, false, zero, unknown, stale and unavailable distinctions required by this block.
- Development checks are evidence, not extra Job or agent-ACK execution gates.

## Detailed implementation work

1. Classify every existing test as pure domain behavior, Python implementation coupling, HTTP/MCP contract, filesystem/SQLite fault boundary, packaging or real external acceptance.
2. Capture state/input/output traces from the current verified base commit. Store only synthetic/sanitized fixtures in Git, with generated IDs/times normalized explicitly.
3. Add Rust domain/property tests for states, graph/ordering invariants, serialization and authorization; keep black-box Python clients independent of Rust implementation details.
4. Replace monkeypatches of Python internals with equivalent faults at the actual Rust boundary: SQLite aborts, process death, pipe/socket reply loss and restart reconciliation.
5. Provide an isolated differential runner that reads the same fixture/clock for both implementations. Only one may perform a real external mutation; shadow execution is read-only.
6. Extend feature catalog ownership, source hashes and audit evidence for Rust crates, schema snapshots, binaries and Python bridges. Test counts are not a substitute for complete behavior coverage.
7. Run retained Firefox suites against Rust-generated API projections and record both list/detail and narrow/light/dark behavior.
8. Keep Docker/GPU, actual Tailscale, native client and power-loss boundaries explicit. A skipped/unavailable external check is never a pass or an execution admission gate.

## Acceptance matrix

| Scenario | Required observable result |
|---|---|
| Rust behavior differs while both suites are green | Differential trace reports the precise contract difference. |
| Mutation commits but response is lost | Original key reconciles once; no automatic duplicate effect. |
| Process dies between filesystem and DB publication | Recover/reuse a matching snapshot or report a safe conflict. |
| Tests are run against modified sources after evidence capture | Feature audit rejects stale hashes. |
| Client/backend transport uses a different representation | Hash/type/null/error fixtures detect the mismatch. |
| An external acceptance tool is absent | Report the unverified boundary without borrowing production state. |

### Existing regression sources

- [tests/deploy/test_features.py](../../../tests/deploy/test_features.py)
- [tests/deploy/test_distribution.py](../../../tests/deploy/test_distribution.py)

Existing Python-internal tests need boundary adaptation when their implementation moves. Passing the old implementation alone does not establish Rust parity. Add state/trace and crash cases from this matrix; keep actual external acceptance separately identified.

## State, cutover and rollback

Tests and fixtures change before switching writers. Preserve the Python implementation as a bounded comparison reference during development, then remove duplicate production authorities only after acceptance.

## Main risk and design review

Most current tests import Python functions directly. Merely copying the 710-pass baseline onto a Rust branch would not test Rust behavior.

## Contracts and documentation to review

- [docs/features/catalog.schema.json](../../../docs/features/catalog.schema.json)
- [deploy/features.py](../../../deploy/features.py)
- [docs/features/VERIFICATION.md](../../../docs/features/VERIFICATION.md)
- [docs/features/catalog.json](../../../docs/features/catalog.json)

Change rule: Register each new feature's unique ID, owned files, inputs/outputs, dependencies, tests and live-validation limitations. Test behavior and failure boundaries rather than adding generic assertions.

Before implementation, apply the cross-block [compatibility contract](../COMPATIBILITY.md), [sequence and ownership rules](../README.md), and [whole-tree review findings](../REVIEW.md). Update the implementation source, public schema/guide, consumers and installation packaging together when an accepted contract changes.

## Exit criteria

- The implemented responsibilities and deliberately retained Python/external boundaries are explicit.
- Every acceptance row has a reproducible test or is named as an unverified external acceptance boundary.
- Affected consumers pass against the selected Rust implementation, including its error and restart paths.
- Preservation and rollback checks use the same state format/identities; no second writer or duplicated external action is introduced.
- Feature mappings and source-qualified verification evidence match the exact candidate build.
- No production activation, user-thread inference, credential rotation or research execution is inferred from source/test completion.
