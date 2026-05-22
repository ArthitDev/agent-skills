# Agent Skills

A collection of Agent Skills installable via `npx skills`.

## Install a skill

```bash
# List all available skills
npx skills@latest add ArthitDev/agent-skills --list

# Install run-cloakbrowser (stealth browser automation)
npx skills@latest add ArthitDev/agent-skills --skill run-cloakbrowser

# Install globally (available across all projects)
npx skills@latest add ArthitDev/agent-skills --skill run-cloakbrowser --global
```

## Available Skills

| Skill | Description |
|-------|-------------|
| [run-cloakbrowser](skills/run-cloakbrowser/) | Stealth Chromium browser automation. Bypasses reCAPTCHA v3 (score 0.9), Cloudflare Turnstile, FingerprintJS. Drop-in Playwright API. |

## Requirements

- `uv` installed
- Run once after install: `uv tool install "cloakbrowser[patchright]" && uv tool run patchright install chromium`
