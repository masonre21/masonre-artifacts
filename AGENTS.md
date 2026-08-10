# masonre-artifacts

Public host for shareable static HTML artifacts (interactive maps, apps, one-off tools), deployed via GitHub Pages. See `README.md` for the publishing workflow.

## Cursor Cloud specific instructions

- This repo is a **static HTML site** — there is no package manager, build step, lint, or automated test suite. "Running" it means serving the files and opening them in a browser.
- Serve locally from the repo root with `python3 -m http.server 8000`, then open `http://localhost:8000/<file>.html` (e.g. `hello.html`). There is no hot reload; refresh the browser after editing a file.
- `scripts/protect.py` turns an HTML file into a password-gated, client-side-decrypting page. Usage: `python3 scripts/protect.py <source.html> <output.html> <password> [title]`. It requires only the Python 3 stdlib plus the `openssl` CLI (both preinstalled). Decryption happens in-browser via WebCrypto, so verify protected pages by loading them over `http://` (not `file://`) and entering the password.
- `*.src.html` is gitignored (used as plaintext sources for `protect.py`); the generated protected `.html` is what gets committed/published.
- Everything here is public — never commit client-confidential data.
