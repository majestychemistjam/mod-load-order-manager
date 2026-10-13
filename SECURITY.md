# Security Policy

## Supported versions

| Version | Supported |
|---------|-----------|
| 0.4.x   | yes       |
| 0.3.x   | security fixes only |
| < 0.3   | no        |

## Reporting a vulnerability

mod-load-order-manager parses untrusted mod archives and plugin headers.
The attack surface we care about:

- Zip/Tar/7z extraction path traversal (`..\` in entry names)
- Malformed plugin headers causing unbounded reads
- YAML/JSON profile files with `!!python/object` tags
- Symlink escapes when staging mods into the game dir

Email `security@modloadorder.dev` with a PoC archive. Do not open a
public issue. We aim to acknowledge within 72 hours.

## Hardening notes for users

- Run the manager as a normal user, not Administrator.
- Keep `profiles/` on a local disk, not a network share.
- Enable `strict_extract = true` in `config/settings.toml` if you
  download mods from untrusted sources.