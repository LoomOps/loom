# dashboard — Rust transition plan

Status: proposed; no Loom Rust implementation or deployment is performed by this document.

Baseline: `4d93ab9bdcb5750f3d0be161925e834984492f89` (Loom alpha.60).

## Decision and sequence

- Target: Retain HTML/JavaScript/CSS and Python browser/SSO/relay server.
- Sequence: all phases: retain; 3/6 consumer acceptance.
- Existing feature dependencies: identity, api, catalog, observations, onboarding, diagnostics.

## Current source and authority

Dashboard HTTP relay·workspace UI. The implemented contract is in the linked source and [dashboard feature specification](../../features/dashboard.md).

| File | Planning treatment |
|---|---|
| [dashboard/.dockerignore](../../../dashboard/.dockerignore) | Retain interface/tooling; review exact bridge and packaging behavior |
| [dashboard/Dockerfile](../../../dashboard/Dockerfile) | Retain interface/tooling; review exact bridge and packaging behavior |
| [dashboard/branding/brand.css](../../../dashboard/branding/brand.css) | Retain interface/tooling; review exact bridge and packaging behavior |
| [dashboard/branding/brand.js](../../../dashboard/branding/brand.js) | Retain interface/tooling; review exact bridge and packaging behavior |
| [dashboard/branding/logo.svg](../../../dashboard/branding/logo.svg) | Retain interface/tooling; review exact bridge and packaging behavior |
| [dashboard/branding/scene.js](../../../dashboard/branding/scene.js) | Retain interface/tooling; review exact bridge and packaging behavior |
| [dashboard/dev.py](../../../dashboard/dev.py) | Retain interface/tooling; review exact bridge and packaging behavior |
| [dashboard/server.py](../../../dashboard/server.py) | Retain interface/tooling; review exact bridge and packaging behavior |
| [dashboard/theme/style.css](../../../dashboard/theme/style.css) | Retain interface/tooling; review exact bridge and packaging behavior |
| [dashboard/theme/theme.js](../../../dashboard/theme/theme.js) | Retain interface/tooling; review exact bridge and packaging behavior |
| [dashboard/workspace/access.html](../../../dashboard/workspace/access.html) | Retain interface/tooling; review exact bridge and packaging behavior |
| [dashboard/workspace/activity.js](../../../dashboard/workspace/activity.js) | Retain interface/tooling; review exact bridge and packaging behavior |
| [dashboard/workspace/build.py](../../../dashboard/workspace/build.py) | Retain interface/tooling; review exact bridge and packaging behavior |
| [dashboard/workspace/details.js](../../../dashboard/workspace/details.js) | Retain interface/tooling; review exact bridge and packaging behavior |
| [dashboard/workspace/explorer.js](../../../dashboard/workspace/explorer.js) | Retain interface/tooling; review exact bridge and packaging behavior |
| [dashboard/workspace/extensions.js](../../../dashboard/workspace/extensions.js) | Retain interface/tooling; review exact bridge and packaging behavior |
| [dashboard/workspace/frame.css](../../../dashboard/workspace/frame.css) | Retain interface/tooling; review exact bridge and packaging behavior |
| [dashboard/workspace/frame.js](../../../dashboard/workspace/frame.js) | Retain interface/tooling; review exact bridge and packaging behavior |
| [dashboard/workspace/icons.js](../../../dashboard/workspace/icons.js) | Retain interface/tooling; review exact bridge and packaging behavior |
| [dashboard/workspace/lazy_logs.py](../../../dashboard/workspace/lazy_logs.py) | Retain interface/tooling; review exact bridge and packaging behavior |
| [dashboard/workspace/mcp.js](../../../dashboard/workspace/mcp.js) | Retain interface/tooling; review exact bridge and packaging behavior |
| [dashboard/workspace/media.js](../../../dashboard/workspace/media.js) | Retain interface/tooling; review exact bridge and packaging behavior |
| [dashboard/workspace/operations-desk.css](../../../dashboard/workspace/operations-desk.css) | Retain interface/tooling; review exact bridge and packaging behavior |
| [dashboard/workspace/parent.css](../../../dashboard/workspace/parent.css) | Retain interface/tooling; review exact bridge and packaging behavior |
| [dashboard/workspace/parent.js](../../../dashboard/workspace/parent.js) | Retain interface/tooling; review exact bridge and packaging behavior |
| [dashboard/workspace/projection.js](../../../dashboard/workspace/projection.js) | Retain interface/tooling; review exact bridge and packaging behavior |
| [dashboard/workspace/queue.js](../../../dashboard/workspace/queue.js) | Retain interface/tooling; review exact bridge and packaging behavior |
| [dashboard/workspace/surfaces.js](../../../dashboard/workspace/surfaces.js) | Retain interface/tooling; review exact bridge and packaging behavior |
| [dashboard/workspace/template.html](../../../dashboard/workspace/template.html) | Retain interface/tooling; review exact bridge and packaging behavior |
| [dashboard/workspace/text-preview.js](../../../dashboard/workspace/text-preview.js) | Retain interface/tooling; review exact bridge and packaging behavior |
| [dashboard/workspace/job-activity.js](../../../dashboard/workspace/job-activity.js) | Retain interface/tooling; review exact bridge and packaging behavior |
| [dashboard/workspace/research.js](../../../dashboard/workspace/research.js) | Retain interface/tooling; review exact bridge and packaging behavior |
| [dashboard/workspace/dependencies.js](../../../dashboard/workspace/dependencies.js) | Retain interface/tooling; review exact bridge and packaging behavior |

## Retained code and external dependencies

All workspace source, generated empty-data template, branding/media libraries, Gateway UI and existing browser authentication remain. Rust migration is not a frontend rewrite.

## Compatibility invariants

- Never send credentials to the opaque iframe. Browser writes respect Origin/CSRF boundaries. The UI must not infer completed backend states.
- Preserve existing IDs, authentication, configured roots, sealed bytes and operational history unless an explicit separate schema change is approved.
- Keep missing, null, false, zero, unknown, stale and unavailable distinctions required by this block.
- Development checks are evidence, not extra Job or agent-ACK execution gates.

## Detailed implementation work

1. Inventory every HTTP route, parent/iframe message and projected field consumed by the workspace. Preserve opaque iframe isolation and keep credentials exclusively in the parent/server boundary.
2. Keep the pinned template hash, generated HTML pipeline and existing layout/icon/localization decisions unchanged.
3. Preserve the limited relay route/method allowlist, Origin/CSRF checks, trusted-peer assertions, session logout and account-switch invalidation.
4. Point only an isolated development Dashboard at the Rust API during parity testing. Do not alter users' production browser sessions or apply design changes as part of the port.
5. Exercise Job status/recovery/scheduling distinctions, logical Steps/Attempts, Activity counts and preserved-history views against Rust-produced projections.
6. Exercise Profiles/Components/Tools/Runtimes/Dependencies links, exact revisions, full inventory collapse, category/search and unavailable states.
7. Run Firefox in light/dark at wide/narrow sizes, including refresh, persistent panes, cancellation controls, logs, previews and shared-access flows.
8. Update frontend code only for an explicitly accepted contract incompatibility; otherwise a browser change signals a backend parity gap to investigate.

## Acceptance matrix

| Scenario | Required observable result |
|---|---|
| Switch backend from Python to Rust | Same routes, panes and visible data semantics. |
| Session/account changes during an in-flight response | Do not restore the old account's cached catalog or controls. |
| Job is executing a recovery Attempt | Show one execution phase without duplicate status text. |
| Activity receives canonical and source records | Count the intended outcome without duplicating source executions. |
| Runtime metadata is unavailable | Show unavailable rather than an empty verified inventory. |
| Hostile metadata or file preview content | Remain escaped/inert across list, detail and messages. |

### Existing regression sources

- [tests/dashboard/test_proxy.py](../../../tests/dashboard/test_proxy.py)
- [tests/dashboard/browser/test_workspace.py](../../../tests/dashboard/browser/test_workspace.py)

Existing Python-internal tests need boundary adaptation when their implementation moves. Passing the old implementation alone does not establish Rust parity. Add state/trace and crash cases from this matrix; keep actual external acceptance separately identified.

## State, cutover and rollback

Retain the existing Dashboard image/source and point its verified relay at the selected backend. No UI rebuild is required unless a reviewed consumer change is accepted; keep the same browser origin and trust boundary.

## Main risk and design review

Keeping the UI does not remove compatibility work: projections, timestamps, error shapes and refresh revisions are all consumed behavior.

## Contracts and documentation to review

- [dashboard/server.py](../../../dashboard/server.py)
- [dashboard/workspace/parent.js](../../../dashboard/workspace/parent.js)

Change rule: Rebuild the generated workspace after UI source edits. Verify both HTTP behavior and real Firefox for authentication, session or relay changes. Review the full installation doctor and step exit criteria when this feature changes; a local health response does not establish user-facing readiness.

Before implementation, apply the cross-block [compatibility contract](../COMPATIBILITY.md), [sequence and ownership rules](../README.md), and [whole-tree review findings](../REVIEW.md). Update the implementation source, public schema/guide, consumers and installation packaging together when an accepted contract changes.

## Exit criteria

- The implemented responsibilities and deliberately retained Python/external boundaries are explicit.
- Every acceptance row has a reproducible test or is named as an unverified external acceptance boundary.
- Affected consumers pass against the selected Rust implementation, including its error and restart paths.
- Preservation and rollback checks use the same state format/identities; no second writer or duplicated external action is introduced.
- Feature mappings and source-qualified verification evidence match the exact candidate build.
- No production activation, user-thread inference, credential rotation or research execution is inferred from source/test completion.
