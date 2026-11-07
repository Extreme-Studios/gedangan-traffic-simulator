# GITHUB BACKUP PLAN AFTER CLEANUP
## Current state
No Git repository exists in this directory; no upload has occurred. This is a preparation plan and measured file allowlist, not a claim of remote backup.

## 1. Minimal source Git repository
Explicit allowlist: documentation/storage_cleanup/GITHUB_SOURCE_ALLOWLIST.json. 448 files / 4,121,399 bytes / 0.004 GiB before Git compression/history. Includes backend, tests/fixtures, frontend source/config/HTML/package lock, research configs, root launchers and human-readable milestone documentation. Do not use git add -A on the whole research workspace. Existing .gitignore covers some caches/runs but not all large archives/builds, so review the allowlist and exclusions before staging. Scan for secrets and human survey identifiers before any upload. No actual credentials printed or uploaded in this task.

## 2. Scientific research data
Keep a separate immutable archive with inventory SHA256: simulation/, geodata/, data/, frontend/public/ originals, calibration schemas, provenance, seeds/OD/registry, documentation source registers and milestone baseline checkpoint ZIPs. Actual simulation/geodata/data 12,511,771,516 bytes / 11.652 GiB; frontend/public 560,465,172 bytes / 0.522 GiB; toolchain 606,295,443 bytes / 0.565 GiB. Preserve original observation databases/video permissions and use local SQLite backup while stopped; do not place unreviewed private survey data in a public repository. No data was moved to a new storage destination.

## 3. Windows release
One canonical FINAL_RELEASE portable ZIP: 149,515,535 bytes / 0.139 GiB; SHA256 5a0b36c4f8a20ec86a3bcb8d5b906ff0b3814cfa3465f376fc7df7cc8e76d520. Store as a release asset after explicit user upload authorization; avoid committing EXE/runtime/ZIP to source history. GitHub blocks ordinary Git files larger than 100 MiB and documents Releases as an option for distributing binaries. [GitHub official large-file guidance](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github?platform=windows). Check available quotas and privacy before any LFS choice; no paid service is activated here.

## 4. Presentation assets
M11 canonical slide/PPTX/PDF/MP4 and final user manuals already included in the Windows release; do not separately upload their duplicate copies unless editorial source backup is required. Keep presentation_demo/m11/build authoring source plus generated slide images and external authoring runtime requirements. M10/M11 reports remain historical; cleanup manifest records retired packaging products.

## 5. Recovery verification
Clone source into a new location, restore separately inventoried research data and approved survey backup, restore pinned dependencies from requirements/package-lock, verify SUMO toolchain/hash, rebuild in a disposable directory, and run actual EXE/playback/importer/export checks. Verify the final release ZIP hash independently. Record source commit, release hash and scientific dataset manifest together. Until that restore has actually been performed, do not describe the whole scientific project as remotely backed up or remotely recoverable.

## Minimal upload answer
Source Git alone: 4,121,399 bytes / 0.004 GiB. Ready-to-use app additionally: 149,515,535 bytes / 0.139 GiB. Full scientific history is not covered by those two artifacts; the retained 12.5 GB scientific dataset, original public exports, toolchain and checkpoint archives need their own explicit backup. No file removed merely to fit a GitHub target size.
