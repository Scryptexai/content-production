# FOOTAGE — stock clips pulled into the repo

Files here arrive through `.github/workflows/footage.yml`: GitHub's runners have
open internet, this sandbox does not, so the runner downloads and commits, and the
working session pulls with `git fetch origin footage/inbox`.

Rules:
- every clip lands with a `MANIFEST.md` recording source URL, sha256 and licence;
- licence must be CC0 / CC-BY / public domain, with the credit line captured;
- nothing from a stock site whose licence forbids re-hosting is committed.
