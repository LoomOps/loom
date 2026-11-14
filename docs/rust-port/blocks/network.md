# network — Rust transition plan

Status: proposed; no Loom Rust implementation or deployment is performed by this document.

Baseline: `4d93ab9bdcb5750f3d0be161925e834984492f89` (Loom alpha.60).

## Decision and sequence

- Target: Retained Python Tailscale enrollment/Sharing/Gateway services; Rust receives existing trusted API requests.
- Sequence: retain initially; 6 trust-boundary acceptance.
- Existing feature dependencies: identity, diagnostics.

## Current source and authority

Tailscale enrollment, Serve and native identity configuration. The implemented contract is in the linked source and [network feature specification](../../features/network.md).

| File | Planning treatment |
|---|---|
| [deploy/tailnet.py](../../../deploy/tailnet.py) | Retain interface/tooling; review exact bridge and packaging behavior |
| [dashboard/admission.py](../../../dashboard/admission.py) | Retain interface/tooling; review exact bridge and packaging behavior |
| [dashboard/admission_http.py](../../../dashboard/admission_http.py) | Retain interface/tooling; review exact bridge and packaging behavior |
| [deploy/access_setup.py](../../../deploy/access_setup.py) | Retain interface/tooling; review exact bridge and packaging behavior |
| [deploy/installer/access-plan.example.json](../../../deploy/installer/access-plan.example.json) | Retain interface/tooling; review exact bridge and packaging behavior |
| [dashboard/gateway.py](../../../dashboard/gateway.py) | Retain interface/tooling; review exact bridge and packaging behavior |
| [dashboard/gateway.js](../../../dashboard/gateway.js) | Retain interface/tooling; review exact bridge and packaging behavior |
| [dashboard/gateway.html](../../../dashboard/gateway.html) | Retain interface/tooling; review exact bridge and packaging behavior |
| [dashboard/gateway.css](../../../dashboard/gateway.css) | Retain interface/tooling; review exact bridge and packaging behavior |
| [dashboard/sharing.py](../../../dashboard/sharing.py) | Retain interface/tooling; review exact bridge and packaging behavior |
| [dashboard/managed_resources.py](../../../dashboard/managed_resources.py) | Retain interface/tooling; review exact bridge and packaging behavior |

## Retained code and external dependencies

Keep Tailscale provider integration, SSO/enrollment cryptography, public request-only Gateway, protected resource journal and policy cleanup behavior. No network re-enrollment is part of a Rust port.

## Compatibility invariants

- New installations keep Dashboard and MCP on private Serve and require a separate public request-only Gateway. tag:loom supports Hub discovery; user grants apply per machine.
- tag:loom is Hub discovery only; access approvals target one stable machine/device identity and exact addresses. Public request listener exposes no operational data or MCP.
- Preserve existing IDs, authentication, configured roots, sealed bytes and operational history unless an explicit separate schema change is approved.
- Keep missing, null, false, zero, unknown, stale and unavailable distinctions required by this block.
- Development checks are evidence, not extra Job or agent-ACK execution gates.

## Detailed implementation work

1. Freeze private Dashboard/MCP and public Gateway exposure, approved trusted peers and native identity assertion rules.
2. Keep exact per-machine/device/address grants; tag-based discovery must not become authorization to every Loom host.
3. Preserve managed-resources intent journaling, ambiguous external-write states and stable installation identity.
4. Preserve atomic journal replacement, service-account ownership, 0600 modes and no-symlink lock/file validation. Ported helpers must not recreate the prior root-only journal failure.
5. Keep accepted/pending invitation state separate from upstream connectivity and local permission errors; preserve actionable diagnostics.
6. Test private/public ingress against the Rust API while leaving provider resources and browser origin unchanged.
7. Only consider rewriting provider clients after explicit SDK/cryptographic compatibility and operator acceptance, not merely to reduce Python file count.
8. Keep sharing removal and uninstall scoped to resources recorded as owned by the installation; never revoke unrelated user/device access.

## Acceptance matrix

| Scenario | Required observable result |
|---|---|
| Public request URL is queried for Jobs/MCP | No operational data or API access. |
| Same host tag on another device | No unintended access grant. |
| Provider write succeeds but reply is lost | Preserve pending journal; reconcile, do not resend blindly. |
| Root-run update replaces journal | Service UID/GID and private mode remain correct. |
| Invite accepted but local journal unreadable | Report the actual local error rather than inferring provider outage. |
| Sharing cleanup or rollback | Preserve unrelated identities, policy entries and other installations. |

### Existing regression sources

- [tests/deploy/test_tailnet.py](../../../tests/deploy/test_tailnet.py)
- [tests/dashboard/test_admission.py](../../../tests/dashboard/test_admission.py)
- [tests/deploy/test_access_setup.py](../../../tests/deploy/test_access_setup.py)
- [tests/dashboard/test_gateway.py](../../../tests/dashboard/test_gateway.py)
- [tests/dashboard/test_sharing.py](../../../tests/dashboard/test_sharing.py)
- [tests/deploy/test_managed_resources.py](../../../tests/deploy/test_managed_resources.py)
- [tests/dashboard/test_managed_permissions.py](../../../tests/dashboard/test_managed_permissions.py)
- [tests/deploy/test_boot_readiness.py](../../../tests/deploy/test_boot_readiness.py)

Existing Python-internal tests need boundary adaptation when their implementation moves. Passing the old implementation alone does not establish Rust parity. Add state/trace and crash cases from this matrix; keep actual external acceptance separately identified.

## State, cutover and rollback

Keep provider resources, origins, TLS and identities in place. The Rust backend consumes existing authenticated ingress; network changes require their own evidence and are not prerequisites to language parity.

## Main risk and design review

The highest-cost external integrations already live behind useful Python boundaries. A new Rust implementation must not widen ingress or lose resource ownership journals.

## Contracts and documentation to review

- [deploy/installer/tailnet-plan.example.json](../../../deploy/installer/tailnet-plan.example.json)
- [docs/ACCESS-ENROLLMENT.md](../../../docs/ACCESS-ENROLLMENT.md)

Change rule: When enrollment or proxy behavior changes, verify installation plans, exact trusted peers, callback URLs, reruns/pending approvals, TLS and policy scope. Review the full installation doctor and step exit criteria when this feature changes; a local health response does not establish user-facing readiness.

Before implementation, apply the cross-block [compatibility contract](../COMPATIBILITY.md), [sequence and ownership rules](../README.md), and [whole-tree review findings](../REVIEW.md). Update the implementation source, public schema/guide, consumers and installation packaging together when an accepted contract changes.

## Exit criteria

- The implemented responsibilities and deliberately retained Python/external boundaries are explicit.
- Every acceptance row has a reproducible test or is named as an unverified external acceptance boundary.
- Affected consumers pass against the selected Rust implementation, including its error and restart paths.
- Preservation and rollback checks use the same state format/identities; no second writer or duplicated external action is introduced.
- Feature mappings and source-qualified verification evidence match the exact candidate build.
- No production activation, user-thread inference, credential rotation or research execution is inferred from source/test completion.
