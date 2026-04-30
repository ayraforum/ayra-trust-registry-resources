# Dependency risk notes

This repository uses `npm` as the canonical JavaScript package manager. Keep `package-lock.json` committed and use `npm ci` for reproducible installs in CI. The old `pnpm-lock.yaml` was removed to avoid split lockfile drift.

## JavaScript tooling

The documentation renderer is driven by `spec-up`; the previous `package.json` also listed most of `spec-up`'s internal renderer dependencies directly. That kept stale copies of packages such as `gulp@3`, old `lodash`, old `minimatch`, and old `axios` in the root dependency graph even though the repo only calls `require('spec-up')`.

Current mitigation:

- Keep only `spec-up` as the direct production dependency.
- Use npm `overrides` to force safer transitive versions for known vulnerable renderer dependencies, including `gulp@5`, modern `axios`, `katex`, `brace-expansion`, `braces`, `micromatch`, `minimatch`, `lodash`, `semver`, `follow-redirects`, and `form-data`.
- Run `npm run audit:prod` in CI with `--audit-level=high` so new high or critical production vulnerabilities fail the build.

Audit result after this cleanup:

- Before: 28 production findings (`1 critical`, `16 high`, `11 moderate`).
- After: 5 production findings (`5 moderate`, no high or critical findings).

## Accepted residual risk

`npm audit --omit=dev` still reports moderate advisories through `spec-up`'s markdown renderer stack (`markdown-it`, `markdown-it-anchor`, `markdown-it-attrs`, and `markdown-it-references`). The fixed `markdown-it@14` package changes internal module paths that `spec-up@0.10.8` and its pinned plugins still expect; forcing `markdown-it@14` makes `npm run render` fail with `Cannot find module .../markdown-it/lib/token`.

This residual risk is accepted for now because:

- The renderer runs in CI/developer tooling, not in an exposed production service.
- The affected package path is used for static documentation rendering.
- High and critical findings have been removed from the production dependency graph.
- CI now blocks newly introduced high/critical production advisories.

Recommended follow-up: replace or fork `spec-up` so the renderer supports modern `markdown-it@14+` and compatible plugins, then tighten CI to `npm audit --omit=dev` with no residual findings.

## Python tools

`tools/requirements.txt` is for the optional DID creator UI and helper scripts. The pins have been refreshed from old `streamlit` and `cryptography` releases to current maintained releases while keeping `base58` at its latest published version.
