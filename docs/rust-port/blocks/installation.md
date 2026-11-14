# installation — Rust transition plan

Status: proposed; no Loom Rust implementation or deployment is performed by this document.

Baseline: `4d93ab9bdcb5750f3d0be161925e834984492f89` (Loom alpha.60).

## Decision and sequence

- Target: Rust binaries/images within retained installer/update/orchestration tooling.
- Sequence: 1 immutable build design; 2 executor kit; 7 complete update acceptance.
- Existing feature dependencies: network, execution, observations, onboarding, dashboard, diagnostics.

## Current source and authority

Compose, host layout, services and immutable builds/releases. The implemented contract is in the linked source and [installation feature specification](../../features/installation.md).

| File | Planning treatment |
|---|---|
| [INSTALL.md](../../../INSTALL.md) | Retain interface/tooling; review exact bridge and packaging behavior |
| [deploy/build.py](../../../deploy/build.py) | Retain interface/tooling; review exact bridge and packaging behavior |
| [deploy/build.sh](../../../deploy/build.sh) | Retain interface/tooling; review exact bridge and packaging behavior |
| [deploy/compose.sh](../../../deploy/compose.sh) | Retain interface/tooling; review exact bridge and packaging behavior |
| [deploy/executor-attach.py](../../../deploy/executor-attach.py) | Retain interface/tooling; review exact bridge and packaging behavior |
| [deploy/guide_bundle.py](../../../deploy/guide_bundle.py) | Retain interface/tooling; review exact bridge and packaging behavior |
| [deploy/host_identity.py](../../../deploy/host_identity.py) | Retain interface/tooling; review exact bridge and packaging behavior |
| [deploy/host_services.py](../../../deploy/host_services.py) | Retain interface/tooling; review exact bridge and packaging behavior |
| [deploy/install-kit.py](../../../deploy/install-kit.py) | Retain interface/tooling; review exact bridge and packaging behavior |
| [deploy/install.py](../../../deploy/install.py) | Retain interface/tooling; review exact bridge and packaging behavior |
| [deploy/installer/INSTALL.md](../../../deploy/installer/INSTALL.md) | Retain interface/tooling; review exact bridge and packaging behavior |
| [deploy/installer/doctor.py](../../../deploy/installer/doctor.py) | Retain interface/tooling; review exact bridge and packaging behavior |
| [deploy/installer/install-plan.example.json](../../../deploy/installer/install-plan.example.json) | Retain interface/tooling; review exact bridge and packaging behavior |
| [deploy/installer/setup.py](../../../deploy/installer/setup.py) | Retain interface/tooling; review exact bridge and packaging behavior |
| [deploy/installer/smoke.py](../../../deploy/installer/smoke.py) | Retain interface/tooling; review exact bridge and packaging behavior |
| [deploy/installer/tailnet-plan.example.json](../../../deploy/installer/tailnet-plan.example.json) | Retain interface/tooling; review exact bridge and packaging behavior |
| [deploy/loom-authority.service](../../../deploy/loom-authority.service) | Retain interface/tooling; review exact bridge and packaging behavior |
| [deploy/migrations.py](../../../deploy/migrations.py) | Retain interface/tooling; review exact bridge and packaging behavior |
| [deploy/migrations/catalog.json](../../../deploy/migrations/catalog.json) | Retain interface/tooling; review exact bridge and packaging behavior |
| [deploy/migrations/research_tools.py](../../../deploy/migrations/research_tools.py) | Retain interface/tooling; review exact bridge and packaging behavior |
| [deploy/policy_cleanup.py](../../../deploy/policy_cleanup.py) | Retain interface/tooling; review exact bridge and packaging behavior |
| [deploy/release.py](../../../deploy/release.py) | Retain interface/tooling; review exact bridge and packaging behavior |
| [deploy/release_check_setup.py](../../../deploy/release_check_setup.py) | Retain interface/tooling; review exact bridge and packaging behavior |
| [deploy/runtime.sh](../../../deploy/runtime.sh) | Retain interface/tooling; review exact bridge and packaging behavior |
| [deploy/snapshot.py](../../../deploy/snapshot.py) | Retain interface/tooling; review exact bridge and packaging behavior |
| [deploy/source_install.py](../../../deploy/source_install.py) | Retain interface/tooling; review exact bridge and packaging behavior |
| [deploy/state_snapshot.py](../../../deploy/state_snapshot.py) | Retain interface/tooling; review exact bridge and packaging behavior |
| [deploy/storage_parity.py](../../../deploy/storage_parity.py) | Retain interface/tooling; review exact bridge and packaging behavior |
| [deploy/test.sh](../../../deploy/test.sh) | Retain interface/tooling; review exact bridge and packaging behavior |
| [deploy/uninstall.py](../../../deploy/uninstall.py) | Retain interface/tooling; review exact bridge and packaging behavior |
| [deploy/update.py](../../../deploy/update.py) | Retain interface/tooling; review exact bridge and packaging behavior |
| [docs/UPDATES.md](../../../docs/UPDATES.md) | Retain interface/tooling; review exact bridge and packaging behavior |
| [executor/loom-executor.service](../../../executor/loom-executor.service) | Retain interface/tooling; review exact bridge and packaging behavior |
| [ops/.dockerignore](../../../ops/.dockerignore) | Retain interface/tooling; review exact bridge and packaging behavior |
| [ops/Dockerfile.loom](../../../ops/Dockerfile.loom) | Retain interface/tooling; review exact bridge and packaging behavior |
| [ops/compose.data.yaml](../../../ops/compose.data.yaml) | Retain interface/tooling; review exact bridge and packaging behavior |
| [ops/compose.dev.yaml](../../../ops/compose.dev.yaml) | Retain interface/tooling; review exact bridge and packaging behavior |
| [ops/compose.executor.yaml](../../../ops/compose.executor.yaml) | Retain interface/tooling; review exact bridge and packaging behavior |
| [ops/compose.loom.fence.yaml](../../../ops/compose.loom.fence.yaml) | Retain interface/tooling; review exact bridge and packaging behavior |
| [ops/compose.loom.yaml](../../../ops/compose.loom.yaml) | Retain interface/tooling; review exact bridge and packaging behavior |
| [ops/compose.observations.yaml](../../../ops/compose.observations.yaml) | Retain interface/tooling; review exact bridge and packaging behavior |
| [ops/host_layout.py](../../../ops/host_layout.py) | Retain interface/tooling; review exact bridge and packaging behavior |
| [ops/release_updates.py](../../../ops/release_updates.py) | Retain interface/tooling; review exact bridge and packaging behavior |
| [deploy/runtime_doctor.py](../../../deploy/runtime_doctor.py) | Retain interface/tooling; review exact bridge and packaging behavior |
| [deploy/queue_control_cli.py](../../../deploy/queue_control_cli.py) | Retain interface/tooling; review exact bridge and packaging behavior |
| [deploy/boot_readiness.py](../../../deploy/boot_readiness.py) | Retain interface/tooling; review exact bridge and packaging behavior |
| [deploy/runtime.py](../../../deploy/runtime.py) | Retain interface/tooling; review exact bridge and packaging behavior |
| [deploy/runtime_inventory.py](../../../deploy/runtime_inventory.py) | Retain interface/tooling; review exact bridge and packaging behavior |

## Retained code and external dependencies

Keep Python/shell installers, Compose/systemd, Tailscale/SSH integration and dependency recipe builders initially. Existing new-install and cumulative update contracts remain authoritative.

## Compatibility invariants

- The loom service account, installation UUID and user profiles are independent. Separate dev and alpha databases, ports and data; restart only after execution resources return.
- New installation has one service contract: native Tailscale identity, Admin binding, Sharing Gateway, Ops, Dashboard, executor and explicit storage. Token-only fallback is not installation success.
- Doctor observes actual state independently of progress receipts. Only explicit smoke submits a Job; diagnostics never repair or grant access. Handoff leads with the verified Gateway URL.
- Preserve existing IDs, authentication, configured roots, sealed bytes and operational history unless an explicit separate schema change is approved.
- Keep missing, null, false, zero, unknown, stale and unavailable distinctions required by this block.
- Development checks are evidence, not extra Job or agent-ACK execution gates.

## Detailed implementation work

1. Extend snapshot/build/install-kit allowlists and source fingerprints for Rust sources, Cargo.lock, toolchain and native artifacts. Keep the frontend image/source unchanged where possible.
2. Choose and pin the supported Linux/architecture/libc build targets; bundle verified binaries so operators do not need a compiler merely to install a release.
3. Package a Rust Executor unit with the same installation grant/socket and least-privilege boundaries. Preserve service UID/GID and every configured storage/dependency root.
4. Add explicit backend/executor compatibility metadata and cumulative update steps. Skipped versions must collect all required transformations and prove compatibility before changing writers.
5. Use existing active-Job/callback/resource-return and Runtime-installation locks. Gate every attached instance when replacing shared executor helpers; never force-kill an installation or unknown owner.
6. Keep upgrade/rebuild preservation of accounts, tokens, registries, metadata, DBs, configured directories and marker identities. Rebuild containers is not permission to reinitialize state.
7. Port or retain health checks that prove storage parity, native entry, guide identity and effective binary provenance; HTTP 200 alone is not acceptance.
8. Run isolated fresh install, skipped-version update, retained-state rebuild, interrupted update/resume and rollback with exact preserved-row/file checks.
9. After all local acceptance, prepare a separate concrete deployment proposal for immutable release targets; this planning branch performs no production deployment.

## Acceptance matrix

| Scenario | Required observable result |
|---|---|
| Install on a machine without Cargo | Use the verified supported-platform artifact or report an explicit unsupported target. |
| Update while a Job/callback/Runtime build owns resources | Wait/refuse safely without remapping or terminating work. |
| Jump across multiple releases | Apply the cumulative ordered migration plan exactly once. |
| Rebuild an existing installation | Retain identities, credentials, catalogs and configured directories. |
| Explorer/API/Executor storage mismatch | Fail parity checks even if service health is 200. |
| Update interrupted after helpers or images change | Resume/rollback with matching source/settings and preserved ownership. |

### Existing regression sources

- [tests/deploy/test_host_identity.py](../../../tests/deploy/test_host_identity.py)
- [tests/deploy/test_install_doctor.py](../../../tests/deploy/test_install_doctor.py)
- [tests/deploy/test_install_kit.py](../../../tests/deploy/test_install_kit.py)
- [tests/deploy/test_installation.py](../../../tests/deploy/test_installation.py)
- [tests/deploy/test_packaging.py](../../../tests/deploy/test_packaging.py)
- [tests/deploy/test_public_source.py](../../../tests/deploy/test_public_source.py)
- [tests/deploy/test_release_check_setup.py](../../../tests/deploy/test_release_check_setup.py)
- [tests/deploy/test_release_lifecycle.py](../../../tests/deploy/test_release_lifecycle.py)
- [tests/deploy/test_storage_parity.py](../../../tests/deploy/test_storage_parity.py)
- [tests/deploy/test_uninstall.py](../../../tests/deploy/test_uninstall.py)
- [tests/deploy/test_upgrade_migrations.py](../../../tests/deploy/test_upgrade_migrations.py)
- [tests/ops/test_release_updates.py](../../../tests/ops/test_release_updates.py)
- [tests/deploy/test_runtime_doctor.py](../../../tests/deploy/test_runtime_doctor.py)
- [tests/deploy/test_boot_readiness.py](../../../tests/deploy/test_boot_readiness.py)
- [tests/deploy/test_runtime_install.py](../../../tests/deploy/test_runtime_install.py)

Existing Python-internal tests need boundary adaptation when their implementation moves. Passing the old implementation alone does not establish Rust parity. Add state/trace and crash cases from this matrix; keep actual external acceptance separately identified.

## State, cutover and rollback

Keep numbered releases immutable and development isolated. Stage new artifacts, drain and fence writers, snapshot with SQLite backup APIs, switch one authoritative implementation, verify and retain a concrete rollback path.

## Main risk and design review

Build success does not establish installability or data preservation. A source-only Rust switch without kit/update/doctor integration would strand existing installations.

## Contracts and documentation to review

- [INSTALL.md](../../../INSTALL.md)
- [deploy/installer/INSTALL.md](../../../deploy/installer/INSTALL.md)
- [deploy/installer/install-plan.example.json](../../../deploy/installer/install-plan.example.json)
- [deploy/installer/steps/01-plan.md](../../../deploy/installer/steps/01-plan.md)
- [deploy/installer/steps/02-host.md](../../../deploy/installer/steps/02-host.md)
- [deploy/installer/steps/03-images.md](../../../deploy/installer/steps/03-images.md)
- [deploy/installer/steps/04-configuration.md](../../../deploy/installer/steps/04-configuration.md)
- [deploy/installer/steps/05-services.md](../../../deploy/installer/steps/05-services.md)
- [deploy/installer/steps/06-network.md](../../../deploy/installer/steps/06-network.md)
- [deploy/installer/steps/07-handoff.md](../../../deploy/installer/steps/07-handoff.md)
- [deploy/update.py](../../../deploy/update.py)
- [docs/UNINSTALL.md](../../../docs/UNINSTALL.md)
- [docs/UPGRADE.md](../../../docs/UPGRADE.md)
- [ops/compose.loom.yaml](../../../ops/compose.loom.yaml)

Change rule: When adding files or dependencies, check Dockerfiles, snapshots, installer HOST_FILES, Compose mounts and new-installation/upgrade guides.

Before implementation, apply the cross-block [compatibility contract](../COMPATIBILITY.md), [sequence and ownership rules](../README.md), and [whole-tree review findings](../REVIEW.md). Update the implementation source, public schema/guide, consumers and installation packaging together when an accepted contract changes.

## Exit criteria

- The implemented responsibilities and deliberately retained Python/external boundaries are explicit.
- Every acceptance row has a reproducible test or is named as an unverified external acceptance boundary.
- Affected consumers pass against the selected Rust implementation, including its error and restart paths.
- Preservation and rollback checks use the same state format/identities; no second writer or duplicated external action is introduced.
- Feature mappings and source-qualified verification evidence match the exact candidate build.
- No production activation, user-thread inference, credential rotation or research execution is inferred from source/test completion.
