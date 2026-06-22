---
name: amp-troubleshoot
description: Orchestrate AMP Shopify store troubleshooting — @diagnose investigates, @explore searches knowledge, Frosty checks skills, fixes directly, and verifies.
---

## What I Do

Orchestrate troubleshooting of AMP-related issues on Shopify stores. `@diagnose` handles heavy investigation, `@explore` searches knowledge, Frosty fixes and verifies directly.

## When to Use Me

Use when Jall reports issues with AMP Shopify stores — broken layouts, validation errors, cache problems, missing widgets, performance degradation, or any BIS/Slide Cart theme issue.

## Steps — ALL MANDATORY

### Phase 1: Diagnose
Call `@diagnose` with the store URL and issue description. Be specific about what to check.

@diagnose returns structured findings: store URL, theme, elements, computed styles, console errors, network issues, JS state, root cause, confidence.

**If confidence is medium/low:** Call `@diagnose` again with the previous findings and follow-up questions. Max 3 rounds.

### Phase 2: Explore
Call `@explore` with your combined diagnosis. Ask for verified fixes and relevant context.

### Phase 3: Check Skills
Run `ls .opencode/skills/` and read any matching skill. Decide if a skill applies and use its steps if so.

### Phase 4: Fix
`list_pages` → `select_page` to the store tab. Inject CSS/JS live via `evaluate_script`.

**BIS iframe pattern:**
```javascript
const frame = document.querySelector('#BIS_frame');
const innerDoc = frame.contentDocument || frame.contentWindow.document;
const style = innerDoc.createElement('style');
style.textContent = `/* your CSS here */`;
innerDoc.head.appendChild(style);
```

**CSS scoping — ALWAYS scope under app IDs:**
- `#slidecarthq` for Slide Cart
- `#BIS_trigger` or `#BISModal` for BIS

For multi-issue tickets, fix and verify one issue at a time.

### Phase 5: Self-Verify
Screenshot + DOM check. For mobile issues, resize viewport first. For form submissions, verify the POST payload via `list_network_requests`.

If fix didn't work — adjust and go back to Phase 4.
If completely failed — call `@explore` with failure context, re-check skills, try different approach. Can also call `@diagnose` to re-investigate why the fix didn't work.

**CSS fix placement priority:**
1. App custom CSS field (BIS or Slide Cart settings) — survives theme changes
2. `<style>` block in theme.liquid before `</head>`
3. Theme custom CSS asset

Always include: `/* Amp CS fix — <date> — <issue description> */`

### Phase 6: Deliver
Provide fix code + placement to Jall. Ask "Is this fix verified?"

### Phase 7: Log Fix
If Jall confirms, append to `knowledge/amp-context/verified-fixes.md`. **Method:** Write the new entry to `tmp/verified-fix-entry.md` (Write tool), then `python -c "open('knowledge/amp-context/verified-fixes.md','a').write(open('tmp/verified-fix-entry.md').read())"`, then delete the temp file. NEVER pass markdown through PowerShell. See AGENTS.md Phase 7 for template.

### Phase 8: Session Log
Write to `logs/YYYY-MM-DD_HH-MM_<summary>.md`.

### Phase 9: Create Skill
If the workflow was novel, create `.opencode/skills/<name>/SKILL.md`. Check existing skills first — update instead of duplicating. Use kebab-case naming (`<app>-<issue-type>`), YAML frontmatter (`name`, `description`), then `## Problem`, `## Workflow`, `## Verification`. Don't ask — just do it and notify Jall.

## Common Issues Quick Reference

- **BIS modal behind elements:** z-index on `#BIS_frame` — inject via iframe contentDocument
- **Slide Cart under header:** z-index on `#slidecarthq`
- **Cache not updating:** Check webhook firing, try AMP Cache purge API
- **Validation errors:** Strip invalid HTML/JS, wrap in `<amp-iframe>` if needed
- **CSS overflow:** Minify, remove unused classes, check `<style amp-custom>` size
- **Missing 3rd-party widgets:** Check native AMP integration support, use `<amp-iframe>` fallback
