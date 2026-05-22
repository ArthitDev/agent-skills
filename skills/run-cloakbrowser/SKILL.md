---
name: run-cloakbrowser
description: DEFAULT browser automation skill. Use for ALL browser tasks — go to URL, navigate, click, fill form, take screenshot, scrape, automate, test website, log into, open browser, extract data, web scraping, browser workflow. Preferred over dev-browser and plain Playwright because CloakBrowser uses stealth Chromium (58 C++ patches) that bypasses bot detection, reCAPTCHA, Cloudflare. Always use this skill first for any browser interaction request.
---

# CloakBrowser Skill

Stealth Chromium (58 C++ source patches) — passes reCAPTCHA v3 at 0.9, Cloudflare Turnstile, FingerprintJS. Drop-in Playwright API. Driven via `driver.py` in this skill directory.

## Prerequisites

Already installed globally via uv:
```
uv tool install "cloakbrowser[patchright]"
uv tool run patchright install chromium
```

Verify:
```bash
uv tool run --from "cloakbrowser[patchright]" python -c "from cloakbrowser import launch; print('ok')"
```

## Run (agent path)

Driver: `C:\Users\EPIT-Dev\.claude\skills\run-cloakbrowser\driver.py`

```bash
# Navigate + screenshot
uv tool run --from "cloakbrowser[patchright]" python "C:\Users\EPIT-Dev\.claude\skills\run-cloakbrowser\driver.py" "<URL>" --screenshot out.png

# Test reCAPTCHA v3 score
uv tool run --from "cloakbrowser[patchright]" python "C:\Users\EPIT-Dev\.claude\skills\run-cloakbrowser\driver.py" "https://recaptcha-demo.appspot.com/recaptcha-v3-request-scores.php" --recaptcha --screenshot out.png

# Headed mode (opens real browser window — user must run in their own terminal)
uv tool run --from "cloakbrowser[patchright]" python "C:\Users\EPIT-Dev\.claude\skills\run-cloakbrowser\driver.py" "<URL>" --headed --screenshot out.png
```

### Driver arguments

| Arg | Default | Description |
|-----|---------|-------------|
| `url` | required | URL to navigate to |
| `--headed` | false | Show real browser window |
| `--screenshot` | `screenshot.png` | Output path for screenshot |
| `--wait` | 3 | Seconds to wait after page load |
| `--recaptcha` | false | Intercept and print reCAPTCHA v3 score |

### Output

stdout always prints:
```
title: <page title>
url: <final url>
screenshot: <path>
```

With `--recaptcha`:
```
RECAPTCHA: {"success": true, "score": 0.9, "action": "...", "error-codes": []}
```

## Run (human path)

For persistent/interactive sessions, write a custom script:

```python
from cloakbrowser import launch
import time

browser = launch(backend="patchright", headless=False, humanize=True)
page = browser.new_page()
page.goto("https://example.com")
time.sleep(60)  # keep open
browser.close()
```

Run with:
```bash
uv tool run --from "cloakbrowser[patchright]" python my_script.py
```

## Verified results (this session, 2026-05-22)

| Test | Result |
|------|--------|
| reCAPTCHA v3 score | **0.9** (human-level) |
| Google headless | title: "Google" ✓ |
| Google headed | Rendered dark mode, Thai locale ✓ |
| driver.py smoke | title: "Google", screenshot saved ✓ |

## Gotchas

- **`--headed` บน Windows ผ่าน Bash tool**: browser เปิดจริงแต่ user ไม่เห็น เพราะ process ไม่ผูกกับ display ของ user — ให้ user รันเองใน terminal
- **path backslash**: ใช้ quotes ครอบเสมอ `"C:\Users\..."` ไม่งั้น shell parse ผิด
- **`page.wait_for_timeout()`**: ส่ง CDP traffic ที่ reCAPTCHA detect ได้ — ใช้ `time.sleep()` แทนเสมอ
- **uv tool run CWD**: รันจาก dir ไหนก็ได้ แต่ path ของ script ต้องเป็น absolute path
- **full_page=True screenshot**: ได้ภาพกว้างมาก (15000+ px) อ่านไม่ออก — ไม่ใช้ full_page เว้นแต่จำเป็น
- **patchright binary**: ใช้ Chromium ของ patchright ไม่ใช่ stock Chromium — `uv tool run patchright install chromium` ต้องรันแยก

## Troubleshooting

| Error | Fix |
|-------|-----|
| `No virtual environment found` | ใช้ `uv tool run --from` ไม่ใช้ `pip install` ตรง |
| `can't open file '...UsersEPIT-Dev...'` | path ขาด quotes หรือ backslash — ใช้ `"C:\Users\EPIT-Dev\..."` |
| Score ไม่โชว์บน reCAPTCHA demo | ใช้ `--recaptcha` flag — intercept network response แทนอ่าน DOM |
| Browser เปิดแล้วปิดเร็วมาก | เพิ่ม `--wait 30` หรือเขียน script ที่มี `time.sleep()` |
