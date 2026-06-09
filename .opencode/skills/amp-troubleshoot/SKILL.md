---
name: amp-troubleshoot
description: Troubleshoot AMP Shopify store issues using Chrome DevTools MCP. Includes self-verification, network POST checking, and auto skill creation.
---

## What I Do

Debug and troubleshoot AMP-related issues on Shopify stores using Chrome DevTools MCP (`evaluate_script`, `take_screenshot`, `navigate_page`, `lighthouse_audit`, `list_network_requests`) for navigation, DOM inspection, and live fix testing.

## When to Use Me

Use when Jall reports issues with AMP Shopify stores — broken layouts, validation errors, cache problems, missing widgets, performance degradation, or any BIS/Slide Cart theme issue.

## Prerequisites (MANDATORY — DO NOT SKIP ANY)

1. **Check verified-fixes.md FIRST.** Read `knowledge/amp-context/verified-fixes.md` and search for similar issues (same store, same symptom, same element). If a match exists, use that fix as your starting point. If you skip this step, you risk wasting time re-solving a problem that's already been fixed.
2. If you need Shopify debugging best practices, BIS/Slide Cart DOM structure, or any deep AMP context — use the **Gemini Google Drive tab** (see AGENTS.md for instructions).

## Tools — Chrome DevTools MCP ONLY

| Task | Tool |
|---|---|
| Navigate to store URL | `navigate_page` |
| Take screenshots | `take_screenshot` |
| Inspect/modify DOM | `evaluate_script` |
| Inject CSS/JS fixes | `evaluate_script` |
| Check network requests | `list_network_requests` / `get_network_request` |
| Performance audit | `lighthouse_audit` |
| Mobile viewport | `resize_page` |
| Click elements | `click` |
| Fill inputs | `fill` / `type_text` |
| Check console errors | `list_console_messages` |

## Steps

### Phase 1: Navigate & Identify
1. **Get the store URL** from Jall
2. **Navigate** to the store page
3. **Take a screenshot** to see current state

### Phase 2: Inspect with Chrome DevTools
4. **Inspect DOM** (`evaluate_script`) — query for relevant app elements:
   ```javascript
   document.querySelector('#slidecarthq')?.outerHTML  // Slide Cart
   document.querySelector('#BIS_trigger')?.outerHTML   // BIS trigger
   document.querySelector('#BIS_frame')               // BIS iframe
   ```
5. **Check for BIS iframe** — if debugging BIS modal, it's inside `#BIS_frame` iframe. Use `evaluate_script` to access `frame.contentDocument` (regular DOM queries CANNOT see inside it)
6. **Diagnose** (`evaluate_script`) — check computed styles, z-index, CSS size, element visibility

### Phase 3: Test Fix Live
7. **Inject CSS/JS** (`evaluate_script`) to apply the fix live
8. **For BIS iframe fixes** — MUST go through `frame.contentDocument` (see iframe pattern below)

### Phase 4: Self-Verify (BEFORE asking Jall)
9. **Screenshot after fix** (`take_screenshot`) — visually confirm it worked
10. **DOM verify** (`evaluate_script`) — programmatically confirm the fix (check element exists, style applied, etc.)
11. **For cart/form submissions** — use `list_network_requests` to intercept the actual POST data and verify the correct variant/data was sent. Do NOT just check the resulting page DOM — verify the actual request payload.
12. **If self-check fails** — do NOT ask Jall. Go back to Phase 3 and try a different approach. Repeat until it works.

### Phase 5: Deliver & Log
13. **Provide the final CSS/JS** to Jall with clear placement instructions:
    - Where to put it (app custom CSS field, theme.liquid, or theme asset)
    - Include comment header: `/* Amp CS fix — <date> — <issue> */`
14. **Ask Jall to verify:** "Is this fix verified and working?"
15. **If verified**, log to `knowledge/amp-context/verified-fixes.md` using the format from AGENTS.md

### Phase 6: Create Skill (MANDATORY if workflow was novel)
16. **If this debugging session involved a novel pattern**, create a new skill:
    - Create `.opencode/skills/<name>/SKILL.md` with proper YAML frontmatter
    - Include the specific steps, code patterns, and gotchas you discovered
    - Verify the file was actually written by reading it back
    - Notify Jall: "New skill created: `<name>` — <reason>"
    - **If you announce a skill but don't write the file, you have failed this step**

## BIS Modal Iframe Pattern (CRITICAL)

```javascript
const frame = document.querySelector('#BIS_frame');
const innerDoc = frame.contentDocument || frame.contentWindow.document;

// Inject CSS into iframe
const style = innerDoc.createElement('style');
style.textContent = `/* your CSS here */`;
innerDoc.head.appendChild(style);

// Query elements inside iframe
const modal = innerDoc.querySelector('#BISModal');
```

## Network POST Verification Pattern

For cart/form submission issues, verify the actual data sent:
```javascript
// After clicking Add to Cart, check network requests for the POST to /cart/add
// The request body should contain the correct variant ID
```
Use `list_network_requests` to find the `/cart/add` POST, then `get_network_request` to inspect its payload.

## CSS Scoping Rule

Always scope CSS under app IDs:
- `#slidecarthq` for Slide Cart
- `#BIS_trigger` or `#BISModal` for BIS

## Where to Place CSS Fixes (priority order)

1. **App custom CSS field** (BIS or Slide Cart settings) — survives theme changes
2. **`<style>` block in theme.liquid** before `</head>` — for early-loading fixes
3. **Theme custom CSS asset** — acceptable but harder to track

Always include: `/* Amp CS fix — <date> — <issue description> */`

## Common Issues Quick Reference

- **Cache not updating:** Check webhook firing, try AMP Cache purge API
- **Validation errors:** Strip invalid HTML/JS, wrap in `<amp-iframe>` if needed
- **CSS overflow:** Minify, remove unused classes, check `<style amp-custom>` size
- **Missing 3rd-party widgets:** Check native AMP integration support, use `<amp-iframe>` fallback
- **BIS modal behind elements:** z-index on `#BIS_frame` via `evaluate_script` into iframe's contentDocument
- **Slide Cart under header:** z-index on `#slidecarthq` via `evaluate_script`
- **Drawer won't open/closes immediately:** JS conflict, NOT CSS — escalate
