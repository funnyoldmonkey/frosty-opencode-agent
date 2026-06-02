<div align="center">

<img src="opencode-profile-pic/frosty_icon.png" alt="Frosty" width="120" />

# Frosty — AI-Powered Tier 2 Shopify Support Agent

**An autonomous troubleshooting agent for [OpenCode Desktop](https://opencode.ai) that debugs live Shopify stores using Chrome DevTools, auto-creates reusable skills, and builds a growing knowledge base of verified fixes.**

[![OpenCode](https://img.shields.io/badge/OpenCode-Desktop-00BFFF?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI+PHBhdGggZmlsbD0id2hpdGUiIGQ9Ik0xMiAyQzYuNDggMiAyIDYuNDggMiAxMnM0LjQ4IDEwIDEwIDEwIDEwLTQuNDggMTAtMTBTMTcuNTIgMiAxMiAyem0wIDE4Yy00LjQxIDAtOC0zLjU5LTgtOHMzLjU5LTggOC04IDggMy41OSA4IDgtMy41OSA4LTggNHoiLz48L3N2Zz4=)](https://opencode.ai)
[![Chrome DevTools MCP](https://img.shields.io/badge/Chrome_DevTools-MCP-4285F4?style=for-the-badge&logo=googlechrome&logoColor=white)](https://www.npmjs.com/package/chrome-devtools-mcp)
---

**Tested with free AI models — no paid API required.**

[Getting Started](#-getting-started) · [How It Works](#-how-it-works) · [Model Comparison](#-model-comparison) · [API Key Rotator](#-api-key-rotator)

</div>

---

## What Is Frosty?

Frosty is a pre-configured AI agent that runs inside [OpenCode Desktop](https://opencode.ai) and acts as a **Tier 2 Technical Support Specialist** for Shopify stores. Give it a store URL and a list of issues — it will:

1. **Navigate** to the live store using Chrome DevTools
2. **Inspect** the DOM, computed styles, console errors, and network requests
3. **Diagnose** the root cause (z-index conflicts, CSS overflow, JS errors, variant sync issues, etc.)
4. **Inject fixes live** (CSS/JS) and verify them with screenshots + DOM checks
5. **Self-verify** before asking you to confirm — retries silently if the fix didn't work
6. **Log verified fixes** to a growing knowledge base so it resolves similar issues faster next time
7. **Auto-create reusable skills** for novel debugging patterns it discovers
8. **Write a session log** with full audit trail of every action taken

It gets smarter over time. Every verified fix and every new skill compounds into a richer knowledge base.

---

## Features

| Feature | Description |
|---|---|
| **Chrome DevTools MCP** | Full browser automation — navigate, screenshot, evaluate JS, inspect network, Lighthouse audits, resize viewport |
| **Self-Healing Loop** | If a fix fails self-verification, Frosty retries with a different approach without asking you |
| **Verified Fixes Log** | Every confirmed fix is logged with store URL, issue, code, and verification status |
| **Auto Skill Creation** | Novel debugging patterns are saved as reusable skills with proper structure and metadata |
| **Session Logs** | Full audit trail for every troubleshooting session — exportable markdown files |
| **API Key Rotator** | Built-in Python proxy that round-robins Google API keys to avoid rate limits |
| **BIS Iframe Handling** | Knows that Back in Stock modals render inside iframes and uses `contentDocument` patterns |
| **CSS Scoping Rules** | Always scopes fixes under app-specific IDs to avoid breaking merchant themes |
| **Network POST Verification** | Verifies cart submissions by inspecting actual request payloads, not just page DOM |
| **Knowledge-Driven** | Pre-loaded with Shopify best practices, AMP product DOM structure, and CSS patterns |

---

## Model Comparison

Frosty has been tested with multiple free AI models on the same 6-issue Shopify store audit (variant sync, CSS spacing, duplicate buttons, mobile responsive, badge verification, cart data verification):

| Model | Vision | Speed | Issues Fixed | Hard Problem (Variant Sync) | Skill Created | Session Log | Score |
|---|---|---|---|---|---|---|---|
| **Gemini 3.1 Flash Lite** | Yes | ~2m 44s | 5/6 | UI sync only — flagged submission for escalation | ✅ | ❌ | **9/10** |
| **Gemma 4 31B IT** | Yes | ~13m | 6/6 | Fully fixed — GID/short ID format detection | ✅ | ✅ | **10/10** |
| **Gemma 4 26B A4B** | Yes | ∞ (stuck) | 0/6 | Infinite reasoning loop — never executed | ❌ | ❌ | **0/10** |
| **Xiaomi MiMo V2.5** | Yes | ~10m | 6/6 | Fully fixed — color map + URL param sync | ✅ | ✅ | **10/10** |

### Recommendations

- **Gemini 3.1 Flash Lite** — Best for quick CSS fixes and straightforward debugging. Blazing fast. Good for high-volume, simpler tickets.
- **Gemma 4 31B IT** — Best for complex issues requiring deep reasoning (variant sync, form data, multi-step JS). Slower but thorough.
- **Xiaomi MiMo V2.5** — Excellent all-rounder. Solved the hard problem with the most thorough approach (URL param handling). Recommended.
- **Gemma 4 26B A4B** — **Not recommended.** Gets stuck in infinite reasoning loops on agentic tasks.
- **Non-vision models** — Still work. Frosty falls back to DOM inspection (`evaluate_script`, `take_snapshot`) instead of screenshot verification. Less reliable for visual/layout issues, equally effective for JS/logic issues.

Most models are **free** through [Google AI Studio](https://aistudio.google.com/apikey) or [OpenRouter](https://openrouter.ai).

---

## Getting Started

### Prerequisites

| Requirement | How to Get It |
|---|---|
| **OpenCode Desktop** | Download from [opencode.ai](https://opencode.ai) |
| **Node.js** (v18+) | [nodejs.org](https://nodejs.org) — needed for Chrome DevTools MCP |
| **Python 3.10+** | [python.org](https://python.org) — needed for the API key rotator |
| **Google AI API Key(s)** | Free from [aistudio.google.com/apikey](https://aistudio.google.com/apikey) |
| **Git** | [git-scm.com](https://git-scm.com) |

### Step 1: Clone the Repository

```bash
git clone https://github.com/funnyoldmonkey/frosty-opencode-agent.git
cd frosty-opencode-agent
```

### Step 2: No MCP Configuration Needed

The MCP servers and API key rotator proxy are already configured in the project's `opencode.jsonc` file. Everything is self-contained — no global config changes required.

The included `opencode.jsonc` sets up:
- **Chrome DevTools MCP** — browser automation with `--isolated` flag (clean session each time)
- **Google provider baseURL** — routes through the API key rotator at `http://127.0.0.1:5555`

> **Note:** The MCP tab in OpenCode Desktop may show "No MCPs configured" — this is a UI bug. The tools load and work correctly from the project config.

### Step 3: Get Google AI API Keys

You need at least one API key, but **3-4 keys are recommended** to avoid rate limits with the built-in key rotator.

#### Creating Your First Key

1. Go to [aistudio.google.com/apikey](https://aistudio.google.com/apikey)
2. Sign in with your Google account
3. Click **"Create API Key"**
4. Select or create a Google Cloud project
5. Copy the key (starts with `AIza...`)

#### Getting Multiple Keys (Recommended)

Google allows one API key per project, but you can create multiple projects:

1. Go to [console.cloud.google.com](https://console.cloud.google.com)
2. Click the project dropdown → **"New Project"**
3. Name it (e.g., `frosty-key-2`, `frosty-key-3`)
4. Go back to [aistudio.google.com/apikey](https://aistudio.google.com/apikey)
5. Create a new key in each project

You can also use **different Google accounts** — each gets its own free quota.

#### Setting Up Your Keys

```bash
cp api-key-rotator/keys.txt.example api-key-rotator/keys.txt
```

Edit `api-key-rotator/keys.txt` and add your keys (one per line):

```
AIzaSyA1234567890abcdefghijklmnop
AIzaSyB0987654321zyxwvutsrqponml
AIzaSyC1111111111222222222233333
```

> **Security:** `keys.txt` is in `.gitignore` and will never be committed.

### Step 4: Start the Key Rotator

```bash
python api-key-rotator/rotator.py
```

First run auto-installs dependencies. You'll see:

```
  Frosty API Key Rotator
  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Proxy      http://127.0.0.1:5555
  Dashboard  http://127.0.0.1:5555/_stats
  Keys       3 loaded
  Rotation   every 3 requests per key
  On 429     instant switch + retry (up to 3x)
```

Open `http://127.0.0.1:5555/_stats` in your browser for a live dashboard showing key usage, rate limits, and request logs.

### Step 5: Open in OpenCode Desktop

1. Open OpenCode Desktop
2. Open the `frosty-opencode-agent` folder as your project
3. Frosty should appear as the default agent (bottom-left of the UI)
4. Select your preferred model (Gemma 4 31B IT recommended)
5. Start chatting!

---

## How It Works

### Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    OpenCode Desktop                      │
│  ┌──────────┐  ┌──────────────┐  ┌───────────────────┐  │
│  │  Frosty  │  │  AGENTS.md   │  │  Knowledge Files  │  │
│  │  Agent   │──│  (Rules)     │──│  (Pre-loaded)     │  │
│  └────┬─────┘  └──────────────┘  └───────────────────┘  │
│       │                                                  │
│  ┌────▼──────────────────┐  ┌─────────────────────────┐  │
│  │  Chrome DevTools MCP  │  │  Skills                 │  │
│  │  (Browser Automation) │  │  (.opencode/skills/)    │  │
│  └────┬──────────────────┘  └─────────────────────────┘  │
└───────┼──────────────────────────────────────────────────┘
        │
  ┌─────▼─────────────┐     ┌──────────────────────┐
  │  Live Shopify      │     │  API Key Rotator     │
  │  Store (Browser)   │     │  (Python Proxy)      │
  └────────────────────┘     └──────────────────────┘
```

### Troubleshooting Flow

When you give Frosty a store issue, it follows this exact sequence:

1. **Check verified fixes** — searches past solutions for similar issues
2. **Navigate** to the store URL via Chrome DevTools
3. **Screenshot** the current state
4. **Inspect DOM** — query elements, check computed styles, z-index, console errors
5. **Diagnose** the root cause
6. **Inject fix** — apply CSS/JS live via `evaluate_script`
7. **Self-verify** — screenshot + DOM check + network POST verification
8. **Retry if needed** — silently tries a different approach if self-check fails
9. **Deliver** — provides final code with placement instructions
10. **Ask for verification** — waits for your confirmation
11. **Log the fix** — appends to `verified-fixes.md`
12. **Create skill** — saves novel patterns for future use
13. **Write session log** — full audit trail to `logs/`

### Knowledge System

```
knowledge/
└── amp-context/
    ├── shopify_best_practices.md   ← 270-line Shopify debugging playbook
    ├── amp-products-context.md     ← BIS & Slide Cart DOM structure
    ├── verified-fixes.md           ← Growing log of confirmed fixes
    └── (your files here)           ← Drop .md files to expand knowledge
```

All files are **automatically loaded** into Frosty's context on every session. Add new `.md` files anytime — they're picked up on the next session.

### Auto-Created Skills

After completing a novel debugging workflow, Frosty creates a skill file:

```
.opencode/skills/
├── amp-troubleshoot/SKILL.md       ← Built-in: core troubleshooting workflow
├── variant-bundle-sync/SKILL.md    ← Auto-created: variant sync pattern
└── (new skills appear here)        ← Grows over time
```

Skills are discovered automatically. On the next session, Frosty sees the new skill and uses it when a matching issue comes up.

---

## API Key Rotator

The built-in Python proxy solves rate limiting for free Google AI API keys.

### Features

- **Round-robin rotation** — switches key every 3 requests (configurable)
- **Auto-retry on 429/5xx** — instantly switches to next key and retries
- **Live dashboard** — `http://127.0.0.1:5555/_stats` with per-key stats
- **JSON API** — `http://127.0.0.1:5555/_stats/json` for programmatic access
- **Auto-install** — dependencies install on first run

### Configuration

Edit `api-key-rotator/rotator.py` to change:

```python
REQUESTS_PER_KEY = 3   # Switch key every N requests
MAX_RETRIES = 3        # Retry attempts on 429/5xx
LISTEN_PORT = 5555     # Proxy port
```

### Dashboard

The stats dashboard auto-refreshes every 5 seconds and shows:

- Total requests, successes, rate limits, errors
- Per-key usage with active key highlighted
- Recent request log with status badges

---

## Project Structure

```
frosty-opencode-agent/
├── .opencode/
│   ├── AGENTS.md                    ← Agent personality, rules, and workflows
│   └── skills/
│       └── amp-troubleshoot/        ← Core troubleshooting skill
│           └── SKILL.md
├── knowledge/
│   └── amp-context/
│       ├── README.md
│       ├── shopify_best_practices.md  ← Shopify debugging playbook
│       ├── amp-products-context.md    ← BIS & Slide Cart DOM reference
│       └── verified-fixes.md         ← Auto-maintained fix log
├── api-key-rotator/
│   ├── rotator.py                   ← Key rotation proxy
│   ├── keys.txt.example             ← Template for API keys
│   └── requirements.txt
├── logs/                            ← Session logs (auto-created, gitignored)
├── opencode-profile-pic/
│   └── frosty_icon.png
├── opencode.json                    ← Agent and skill configuration
├── opencode.jsonc                   ← MCP servers and provider config (portable)
├── .gitignore
└── README.md
```

---

## Customization

### Adding Knowledge

Drop any `.md` file into `knowledge/amp-context/` with relevant information:

- Client-specific notes
- New app features or DOM changes
- Edge cases and workarounds
- Integration documentation

Files are automatically loaded on the next session.

### Adapting for Your Apps

Frosty is built for [AMP](https://useamp.com) Shopify apps (Back in Stock, Slide Cart), but you can adapt it:

1. **Edit `AGENTS.md`** — change the role, tone, and focus
2. **Replace knowledge files** — add your own app's DOM structure and debugging patterns
3. **Update the troubleshooting skill** — modify selectors, patterns, and common issues
4. **Add new skills** — create `.opencode/skills/<name>/SKILL.md` for your workflows

---

## Troubleshooting

### Frosty doesn't respond

The `.opencode/tools/` folder crashes OpenCode Desktop on Windows. If you see this, delete the `tools/` folder:

```bash
rm -rf .opencode/tools/
```

### MCP servers don't appear

This is a [known OpenCode bug](https://github.com/anomalyco/opencode/issues/19098). However, the tools still load and work correctly from the project config — it's just the UI that doesn't show them.

### Rate limits (429 errors)

- Add more API keys to `keys.txt`
- Lower `REQUESTS_PER_KEY` in `rotator.py` (default: 3)
- Use different Google accounts for more keys

### Agent uses Playwright instead of Chrome DevTools

The AGENTS.md explicitly says "Do NOT use Playwright for debugging tasks." If a model still picks Playwright, try a stronger model (Gemma 4 31B) or restart the session.

---

## Use Your Own Browser (AutoConnect Mode)

By default, Frosty spawns its own isolated Chromium browser. With AutoConnect, Frosty connects to **your actual Chrome browser** — giving it access to your logged-in sessions (Helpscout, Shopify Partners, Notion, etc.).

### Setup

**Step 1: Enable Remote Debugging in Chrome**

1. Open your Chrome browser
2. Navigate to `chrome://inspect/#remote-debugging`
3. Follow the dialog to **enable remote debugging**
4. You should see: `Server running at 127.0.0.1:9222`

> **Note:** You need to re-enable this each time you restart Chrome.

**Step 2: Update `opencode.jsonc`**

Change the `chrome-devtools` command to:

```json
"chrome-devtools": {
  "type": "local",
  "command": ["npx", "-y", "chrome-devtools-mcp@latest", "--autoConnect"],
  "enabled": true
}
```

**Step 3: Restart OpenCode and tell Frosty which tab to work on**

- *"Go to the Helpscout tab and check ticket #384379"*
- *"Open the Notion tab and scrape the BIS documentation"*
- *"Work on the Shopify Partners tab — find store xyz"*

Frosty uses `list_pages` to see all your open tabs, then `select_page` to target the one you specify. Your other tabs are untouched.

### Tips

- Be specific: *"the tab with helpscout.net"* or *"the Notion tab titled BIS Docs"*
- Requires Chrome 144+
- Connects to one Chrome profile at a time
- To switch back to isolated mode, remove `--autoConnect` from the command
