# AMP Verified Fixes Log

This file is automatically maintained by Frosty. Each entry represents a troubleshooting fix that Jall has confirmed as verified and working. Frosty references this log to resolve similar issues faster in the future.

---

### [2026-06-02] BIS Button Template/Product Type Filtering & Flicker Fix
- **Store URL:** https://adj1cvsfyklpc9vsbiny.myshopify.com/
- **Issue:** Button appearing on excluded templates, "Digital Goods" products, and flickering on first variant selection.
- **Fix Description:** Updated integration script with early exits for specific body classes and product categories, and implemented a unified visibility manager to synchronize theme ATC state and BIS state, eliminating the flicker.
- **Script:**
\`\`\`javascript
// Updated integration script with early exits and unified visibility sync
// See session log for full implementation
\`\`\`
- **Verified by Jall:** Yes

