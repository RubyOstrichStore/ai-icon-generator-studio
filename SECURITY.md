# Security Policy

## Supported versions

| Version | Supported |
|---------|-----------|
| 0.6.x   | yes       |
| 0.5.x   | security-only |
| < 0.5   | no        |

## Reporting a vulnerability

Do not open a public issue for security problems. Email
`security@ai-icon-generator-studio.dev` with:

- A description of the issue
- Reproduction steps
- Affected version(s)
- Any proof-of-concept files

We aim to acknowledge within 72 hours and ship a patch within 14 days
for confirmed issues.

## Threat model

`ai-icon-generator-studio` is a local desktop tool. It does not open
network sockets except for:

1. Optional model downloads from the configured mirror
   (`config/models.yaml`).
2. Opt-in telemetry, disabled by default.

If you find a path where the tool exfiltrates prompt content, generated
icons, or the local config without explicit user opt-in, that's a
security bug — report it.

## Model supply chain

Model files are downloaded over HTTPS and verified against SHA-256
hashes pinned in `config/models.yaml`. If a mirror serves a mismatched
hash, the download is rejected. Report any bypass of this check.

## Third-party presets

Style presets under `presets/` are plain YAML. They are parsed with
`safe_load`. If you find a preset that can trigger code execution,
that's a critical bug.