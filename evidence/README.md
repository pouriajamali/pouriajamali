# Shared career evidence registry

`projects.json` is the editable authority for the fourteen public labs. Profile links,
the portfolio build projection and resume-generation links consume it. This is
release provenance and presentation consistency, not a production or skill certificate.

- `latest_observed_release` records discovery. It never promotes a release automatically.
- `recommended_verified_release` pins the reviewed tag, commit, exact-commit CI and
  download/signature check scope. Run/check download evidence before promotion.
- `resume_editions` pins the evidence used when an immutable PDF edition was issued.
  It is deliberately separate from a newer launcher-only software preview. Current
  PDFs are hash-checked; old editions are not rewritten when a software tag changes.
- Historical source/measurement links retain their own tags and attribution.

After reviewing a new release, edit the registry, run
`python tools/evidence_registry.py --write`, then `python tools/evidence_registry.py`
and `python -m unittest discover -s tools -p 'test_*.py' -v`.
The GitHub workflow checks the profile contract on every push/PR; it does not claim
to execute the lab binaries or inspect private career accounts.
It also verifies `projects.json.sig` against the preserved portfolio public key.
This signature covers the exact registry bytes; Git commit signing and package
runtime verification are separate properties. Current README destinations use
named references inside one managed block. Historical tagged links outside it are
never rewritten.

In the private career workspace, `career-assets/sync_evidence_registry.py --write`
copies this exact JSON into the portable site and emits its browser-safe module.
Without `--write` it rejects drift. The site build rejects a stale generated module
or modified public PDF. `career-assets/evidence_registry.py` gives resume builders
either the current approved releases or an explicit, reproducible issuance snapshot.

No scheduled process scrapes GitHub or silently updates PDFs, account attachments,
benchmark claims, employer work or public posts.


## Resume edition, 17 November 2026

`layout-polish-20261117` registers the exact English PDF bytes checked by ResumeGo
(90/A for Backend and Trading). NL/ES bytes and every prior issuance remain
immutable. Project release recommendations are unchanged; a newer discovered
tag is not promoted by this resume update. The checker grade is not an employer
ATS result or an interview prediction. Account distribution is verified separately.


## Current downloads and frozen evidence, 19 November 2026

`current_download_release` records a newer download only after exact-tag identity,
all actual package hashes and the known SSH checksum signature are checked.
It does not inherit the older release's CI result. `recommended_verified_release`
retains the CI-verified evidence baseline; the original strict CI checks remain.
Publisher-reported local runtime checks are identified in each newer release entry.
This career update downloaded and inspected artifacts without running the lab binaries.

Market Data Integrity's newer CLI technology refresh is a separate channel. Its
existing 60-second GUI demonstration keeps the matching GUI release. The issued
CVs retain their original tested versions, counts and hashes; they are not silently
rewritten merely because a software download changes. Current download and design
links are generated from this registry. The stable portfolio design redirect is
updated during the same site build.
