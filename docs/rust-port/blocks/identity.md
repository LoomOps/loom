# identity — Rust transition plan

Status: proposed; no Loom Rust implementation or deployment is performed by this document.

Baseline: `4d93ab9bdcb5750f3d0be161925e834984492f89` (Loom alpha.60).

## Decision and sequence

- Target: Rust actor/delegation and ownership domain; retained Python SSO/session boundary.
- Sequence: 1 contract fixtures; 6 HTTP/API cutover.
- Existing feature dependencies: none.

## Current source and authority

User authentication, SSO sessions and current ownership. The implemented contract is in the linked source and [identity feature specification](../../features/identity.md).

| File | Planning treatment |
|---|---|
| [dashboard/requirements.txt](../../../dashboard/requirements.txt) | Inspect domain/consumer boundary; port only the selected core responsibility |
| [dashboard/sso.py](../../../dashboard/sso.py) | Inspect domain/consumer boundary; port only the selected core responsibility |
| [ops/access.py](../../../ops/access.py) | Inspect domain/consumer boundary; port only the selected core responsibility |
| [ops/ownership.py](../../../ops/ownership.py) | Inspect domain/consumer boundary; port only the selected core responsibility |
| [ops/service_tokens.py](../../../ops/service_tokens.py) | Inspect domain/consumer boundary; port only the selected core responsibility |

## Retained code and external dependencies

Keep dashboard/sso.py and its existing authentication dependencies, native Tailscale identity integration and browser session lifecycle. Do not replace established cryptographic verification with a new hand-written implementation.

## Compatibility invariants

- Ownership does not restrict access. Browser sessions and MCP authentication are independent; invalidated browser sessions cannot be reused.
- Preserve existing IDs, authentication, configured roots, sealed bytes and operational history unless an explicit separate schema change is approved.
- Keep missing, null, false, zero, unknown, stale and unavailable distinctions required by this block.
- Development checks are evidence, not extra Job or agent-ACK execution gates.

## Detailed implementation work

1. Inventory every actor field, scope and delegated owner/notify rule from access.py; represent authenticated actors and attribution identities as distinct Rust types.
2. Extract scope decisions into pure Rust functions with the current fixture outcomes. Ownership overlays remain shared attribution, not per-owner visibility restrictions.
3. Keep token digests, credential IDs and revocation semantics byte-compatible. A rejected explicit Bearer credential must not fall through to another identity provider.
4. Define the retained SSO-to-Ops boundary using the existing trusted relay assertion; verify peer, signature, expiry, audience and installed instance identity before constructing an actor.
5. Port owner/profile attribution mutations into the same Ops transaction and maintenance fence as the corresponding record. Preserve original namespace and immutable provenance.
6. Compare Python and Rust read-only authorization decisions on synthetic actors; never run both implementations to issue or revoke a real credential.
7. At API cutover exercise Admin/non-Admin and two independent installation identities, then verify native browser/session invalidation through the retained Dashboard.

## Acceptance matrix

| Scenario | Required observable result |
|---|---|
| Invalid Bearer plus otherwise valid Tailscale identity | Reject; no authentication fallback. |
| Shared record registered by another user | Retain shared discovery and current attribution. |
| Revoked token or invalidated browser session | Reject new requests without altering historical owner IDs. |
| Non-Admin token-management request | Reject through the existing Admin boundary. |
| Attribution change while maintenance is active | No source/Job change and no unauthorized metadata write. |
| Assertion from another installation or untrusted peer | Reject before domain operations. |

### Existing regression sources

- [tests/ops/test_access_contract.py](../../../tests/ops/test_access_contract.py)
- [tests/ops/test_shared_ownership.py](../../../tests/ops/test_shared_ownership.py)
- [tests/ops/test_dashboard_identity.py](../../../tests/ops/test_dashboard_identity.py)
- [tests/dashboard/test_sso.py](../../../tests/dashboard/test_sso.py)
- [tests/ops/test_service_tokens.py](../../../tests/ops/test_service_tokens.py)

Existing Python-internal tests need boundary adaptation when their implementation moves. Passing the old implementation alone does not establish Rust parity. Add state/trace and crash cases from this matrix; keep actual external acceptance separately identified.

## State, cutover and rollback

No token regeneration or SSO migration is required. Keep existing protected credential/session stores and accepted relay formats; rollback uses the same identities and revocations.

## Main risk and design review

The browser identity, authenticated API principal and human attribution are different concepts. Consolidating them into one Rust User struct would change sharing and authority.

## Contracts and documentation to review

- [ops/access.py](../../../ops/access.py)
- [dashboard/sso.py](../../../dashboard/sso.py)
- [loom_use/operator.md](../../../loom_use/operator.md)

Change rule: When authentication or profile contracts change, review Ops actors, the Dashboard relay, new installations, ownership display and user guides together. Review the full installation doctor and step exit criteria when this feature changes; a local health response does not establish user-facing readiness.

Before implementation, apply the cross-block [compatibility contract](../COMPATIBILITY.md), [sequence and ownership rules](../README.md), and [whole-tree review findings](../REVIEW.md). Update the implementation source, public schema/guide, consumers and installation packaging together when an accepted contract changes.

## Exit criteria

- The implemented responsibilities and deliberately retained Python/external boundaries are explicit.
- Every acceptance row has a reproducible test or is named as an unverified external acceptance boundary.
- Affected consumers pass against the selected Rust implementation, including its error and restart paths.
- Preservation and rollback checks use the same state format/identities; no second writer or duplicated external action is introduced.
- Feature mappings and source-qualified verification evidence match the exact candidate build.
- No production activation, user-thread inference, credential rotation or research execution is inferred from source/test completion.
