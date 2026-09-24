# masonre-artifacts

Host for shareable static HTML artifacts (interactive maps, apps, one-off tools), deployed via GitHub Pages. See `README.md` for the publishing workflow.

## Cursor Cloud specific instructions

### Standing rule: private pages are password-protected

Private / family / client content **must** be published as a password-gated page via `scripts/protect.py` — same pattern as `israel-itinerary.html`. Never commit plaintext private HTML. Edit a `*.src.html` source (gitignored), then regenerate the protected output:

```bash
python3 scripts/protect.py <source.src.html> <output.html> "$FAMILY_PASSWORD" "<Title>"
```

Only the encrypted `output.html` is committed and served. Decryption happens in-browser via WebCrypto over `http://` (not `file://`).

### Local serve / tooling

- This repo is a **static HTML site** — no package manager, build step, lint, or automated test suite. "Running" it means serving files and opening them in a browser.
- Serve from the repo root: `python3 -m http.server 8000`, then open `http://localhost:8000/<file>.html`. No hot reload — refresh after edits.
- `protect.py` needs only Python 3 stdlib + the `openssl` CLI. The family unlock password lives in the `FAMILY_PASSWORD` secret when testing protected pages (e.g. `israel-itinerary.html`).
- Public smoke-test page: `hello.html`. Canonical private example: `israel-itinerary.html`.
