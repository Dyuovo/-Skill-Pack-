---
name: solo-release-artifact-builder
description: Prepare immutable release artifacts for solo-product deployment. Use when the user needs SemVer, annotated tags, build outputs, tarballs or image digests, SHA256 checksums, RELEASE.json metadata, release plans, or CI artifact handoff. 适用于 release 制品、版本号、校验和.
---

# Solo Release Artifact Builder

## Purpose

Separate build from deploy. Produce an immutable artifact and enough metadata to prove what will be deployed.

## Inputs

- Repo and build command.
- Target version or SemVer decision.
- Git SHA.
- Deployment target.
- Files that must or must not be included.

## Workflow

1. Confirm working tree and release branch/tag policy.
2. Choose version:
   - patch for fixes.
   - minor for backward-compatible features.
   - major for breaking changes.
3. Create an annotated tag for release when appropriate.
4. Build locally or in CI.
5. Package only required runtime files.
6. Exclude real `.env`, secrets, logs, uploads, backups, and temporary files.
7. Generate SHA256 checksum.
8. Write `RELEASE.json`.
9. Record the release plan and expected verification values.

## RELEASE.json Fields

```json
{
  "app": "myapp",
  "version": "0.1.0",
  "git_sha": "",
  "release_id": "",
  "build_time": "",
  "artifact": "",
  "artifact_sha256": ""
}
```

## Release Plan Template

```markdown
# Release Plan

## Version

## Git SHA

## Artifact

## SHA256

## Included Files

## Excluded Files

## Pre-Deploy Checks

## Expected Version Response

## Rollback Target
```

## Quality Gate

Do not deploy from a mutable working directory when the project has production users or valuable data. Deploy an artifact or a clearly identified immutable image.

