# onboarding — Rust transition plan

Status: proposed; no Loom Rust implementation or deployment is performed by this document.

Baseline: `4d93ab9bdcb5750f3d0be161925e834984492f89` (Loom alpha.60).

## Decision and sequence

- Target: Rust build/provenance and live-guide endpoints; retained Loom Use client/Skill installer.
- Sequence: 1 contract fixtures; 6 server guide integration.
- Existing feature dependencies: identity, api.

## Current source and authority

User guides, version identification and client entry. The implemented contract is in the linked source and [onboarding feature specification](../../features/onboarding.md).

| File | Planning treatment |
|---|---|
| [dashboard/build_version.py](../../../dashboard/build_version.py) | Inspect domain/consumer boundary; port only the selected core responsibility |
| [ops/build_version.py](../../../ops/build_version.py) | Inspect domain/consumer boundary; port only the selected core responsibility |
| [ops/onboarding.py](../../../ops/onboarding.py) | Inspect domain/consumer boundary; port only the selected core responsibility |
| [loom_use/client-release.json](../../../loom_use/client-release.json) | Inspect domain/consumer boundary; port only the selected core responsibility |
| [deploy/client_release.py](../../../deploy/client_release.py) | Inspect domain/consumer boundary; port only the selected core responsibility |
| [tests/ops/client_source.py](../../../tests/ops/client_source.py) | Inspect domain/consumer boundary; port only the selected core responsibility |
| [loom_use/runtimes.md](../../../loom_use/runtimes.md) | Inspect domain/consumer boundary; port only the selected core responsibility |

## Retained code and external dependencies

Keep independent Loom Use installation, Codex refresh, credential management and optional Skills. Do not bundle a second stale copy of server-owned usage rules into Rust.

## Compatibility invariants

- The running server is authoritative for guides. Updates do not change personal instructions or active Job pins.
- Preserve existing IDs, authentication, configured roots, sealed bytes and operational history unless an explicit separate schema change is approved.
- Keep missing, null, false, zero, unknown, stale and unavailable distinctions required by this block.
- Development checks are evidence, not extra Job or agent-ACK execution gates.

## Detailed implementation work

1. Capture the live manifest, guide index, guide bytes and contract revisions from onboarding.py and build_version modules.
2. Keep server guides authoritative and versioned; preserve update-on-connect/response semantics without mutating active Job pins.
3. Define Rust build identity including commit, source inventory and modified-state detection; include Rust sources/lockfiles in snapshot and component provenance.
4. Preserve the pinned client-release descriptor until the existing client cannot consume an accepted contract. A language change alone is not a client protocol break.
5. Generate guides/reference examples from the same Rust action registry or retained verified registry used at runtime.
6. Test compact describe/discovery and large Runtime/Profile summaries through the pinned actual Loom Use transport, not only an HTTP mock.
7. Where contract changes require it, update the client repository and Skill instructions together, preserving existing connection profiles and user authentication.
8. Validate a packaged guide against the immutable image build, not the mutable development tree.

## Acceptance matrix

| Scenario | Required observable result |
|---|---|
| Server guide revision changes with the same client pin | Refresh guidance without replacing credentials or rerunning Jobs. |
| Stale numbered Rust image or modified mounted source | Expose accurate provenance; no false immutable claim. |
| Caller has restricted scopes | Reference/index omit unavailable capabilities. |
| Versioned guide ZIP is installed twice | Reuse identical bytes; reject a different existing version. |
| New action with an older loaded Codex connection | Verify supported MCP refresh and an actual action call. |
| Large discovery response | Retain on-demand exact detail and existing transport limits. |

### Existing regression sources

- [tests/ops/test_onboarding.py](../../../tests/ops/test_onboarding.py)
- [tests/ops/test_client_setup.py](../../../tests/ops/test_client_setup.py)
- [tests/deploy/test_client_release.py](../../../tests/deploy/test_client_release.py)

Existing Python-internal tests need boundary adaptation when their implementation moves. Passing the old implementation alone does not establish Rust parity. Add state/trace and crash cases from this matrix; keep actual external acceptance separately identified.

## State, cutover and rollback

Keep the existing client/Skill registration unless the accepted protocol requires change. Install guide artifacts by immutable build and verify native client calls without daemon restart or new inference turns.

## Main risk and design review

Code, client release and usage guide revisions are separate. Reusing a Python build marker for a Rust binary would give false readiness.

## Contracts and documentation to review

- [ops/onboarding.py](../../../ops/onboarding.py)
- [loom_use/entry.md](../../../loom_use/entry.md)

Change rule: When usage contracts change, update Loom Use documents, bundle inventory, revisions and the stdio client. Review the full installation doctor and step exit criteria when this feature changes; a local health response does not establish user-facing readiness.

Before implementation, apply the cross-block [compatibility contract](../COMPATIBILITY.md), [sequence and ownership rules](../README.md), and [whole-tree review findings](../REVIEW.md). Update the implementation source, public schema/guide, consumers and installation packaging together when an accepted contract changes.

## Exit criteria

- The implemented responsibilities and deliberately retained Python/external boundaries are explicit.
- Every acceptance row has a reproducible test or is named as an unverified external acceptance boundary.
- Affected consumers pass against the selected Rust implementation, including its error and restart paths.
- Preservation and rollback checks use the same state format/identities; no second writer or duplicated external action is introduced.
- Feature mappings and source-qualified verification evidence match the exact candidate build.
- No production activation, user-thread inference, credential rotation or research execution is inferred from source/test completion.
