# Contributing to mod-load-order-manager

Thanks for wanting to help sort the pile. This is a Windows desktop mod
manager focused on one job: **deterministic load-order sorting** for
plugin/mod trees across Bethesda-style games, Unity mod stacks, and
generic folder-based mod layouts.

## Ground rules

- One feature per PR. Load-order logic changes need a test in
  `tests/test_load_order_resolver.py`.
- No new runtime deps without a note in the PR body. We keep the core
  import-light so the frozen build stays under ~40 MB.
- Python 3.11+ only. We use `tomllib`, `match`, and `ExceptionGroup`.
- GUI code lives under `src/modloadorder/ui/`. Business logic never
  imports from `ui/`.

## Local dev

```
py -3.11 -m venv .venv
.venv\Scripts\activate
pip install -e .[dev]
pytest -q
python -m modloadorder
```

## Commit style

`scope: short imperative summary` — e.g.
`resolver: break ties by plugin mtime when masters are equal`.

## Reporting load-order bugs

Attach the `logs/resolve_trace.json` dump from a failing profile. It
contains the full dependency graph and the tie-break decisions.