# Source backup â€” 8 November 2026

Status: source and minimum simple-mode network/context data prepared for public GitHub upload. Original workspace files remain in place. The 31 GiB research workspace is not fully backed up by this repository.

Included: current and historical code, configuration/lockfiles, tests, text reports, minimum frozen networks and access metadata, scene and provenance/OD fixture. Excluded: raw/historical survey databases, frontend public exports, generated builds, simulation FCD/recordings, toolchain, dependencies, media and EXE/ZIP distributions. Existing historical reports describe their own earlier snapshots; README.md describes this repository's current entry point.

Security review: scanned selected UTF-8 files for private keys, common GitHub/AWS tokens and credential assignments. No matching secrets found. Email matches were public official Dishub contacts in research source/documents. No raw observation database or user survey identifiers were selected. This is a targeted scan, not a formal security certification.

The application keeps permissions and network geometry unchanged. Pedestrians remain unsupported and angkot uses an assumed van model. No calibration, full-project restore or all-milestone regression claim is made.

Validation from the isolated source copy: npm ci, TypeScript check and Vite simple build passed. Actual SUMO 1.28.0 run with 100 requests: 98 routed/departed/moved, 92 arrived, 2 rejected routes. Local test toolchain/dependencies/build/results are excluded from publication.
