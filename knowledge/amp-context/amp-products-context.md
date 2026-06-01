# Amp Products — Technical Context for CS Theme Fixes

**Purpose:** Context file to reference when helping Amp CS reps fix CSS/HTML issues for merchants. Focused on *what these apps are, how they render, and what's customizable* — not pricing, strategy, or business metrics.

**Last updated:** May 2026

---

## What Amp ships

Amp builds Shopify apps for post-purchase recovery and AOV. The two apps CS most often debugs theme issues for:

- **Back in Stock (BIS)** — restock alerts. Customer hits an out-of-stock product, signs up to be notified when it's back, gets email/SMS/push when restocked.
- **Slide Cart** — cart drawer with upsells, free gifts, rewards. Slides in from the side when customer adds to cart or clicks the cart icon.

Both apps inject DOM into the merchant's theme via app embeds and theme app blocks. They do *not* require merchants to manually edit code in normal cases — but real-world theme variations mean ~10-15% of merchants need CSS/HTML adjustments to fit their theme cleanly.

---

## Back in Stock (BIS)

### What renders on the storefront

BIS adds two main UI elements to product pages where at least one variant is out of stock:

1. **Trigger button** (`#BIS_trigger`) — sits on the product page, usually replacing or adjacent to the "Add to Cart" button when the variant is OOS. Label is typically "Notify me when available" but is customizable per merchant.

2. **Modal / form** (`#BISModal`) — opens when the trigger is clicked. Contains:
   - Email input (always)
   - Phone input (if merchant has SMS enabled)
   - Push notification opt-in (if enabled)
   - Submit button
   - Optional: marketing opt-in checkbox, custom merchant message

### DOM structure (typical)

```
#BIS_trigger
  └─ button or div with merchant-customizable label

#BIS_frame                    ← IFRAME (src="about:blank")
  └─ (iframe document)
      └─ #BISModal
          ├─ .bis-modal-overlay     (dimmed background)
          ├─ .bis-modal-container   (the actual modal)
          │   ├─ .bis-modal-header  (title, close X)
          │   ├─ .bis-modal-body    (inputs)
          │   └─ .bis-modal-footer  (submit, optional opt-ins)
```

Exact class names vary slightly by app version — always inspect the actual DOM the CS rep pastes rather than assuming.

### ⚠️ CRITICAL: BIS modal renders inside an iframe

The BIS modal (`#BISModal`) is rendered inside an iframe with id `BIS_frame` and `src="about:blank"`. This has major implications for debugging:

1. **`search_dom` cannot see inside the iframe.** The main page DOM only shows the `<iframe id="BIS_frame">` tag — none of the modal's inner elements (`.bis-modal-container`, inputs, buttons) appear in a regular DOM search.

2. **Regular `inject_css` won't work.** CSS injected into the main page does NOT cascade into the iframe. The iframe has its own document with its own stylesheets.

3. **To style/fix the modal, you MUST use `inject_js` to reach into the iframe:**
   ```javascript
   // Access the iframe's inner document
   const frame = document.querySelector('#BIS_frame');
   const innerDoc = frame.contentDocument || frame.contentWindow.document;
   
   // Inject CSS into the iframe
   const style = innerDoc.createElement('style');
   style.textContent = `/* your CSS here */`;
   innerDoc.head.appendChild(style);
   
   // Query elements inside the iframe
   const modal = innerDoc.querySelector('#BISModal');
   const submitBtn = innerDoc.querySelector('.bis-modal-footer button');
   ```

4. **To inspect elements inside the iframe with `run_test`:**
   ```javascript
   const frame = document.querySelector('#BIS_frame');
   const innerDoc = frame.contentDocument || frame.contentWindow.document;
   return innerDoc.querySelector('.bis-modal-container')?.outerHTML;
   ```

5. **The iframe may not exist until the trigger button is clicked.** If you don't see `#BIS_frame` in the DOM, click the trigger button first, then check again.

**Rule of thumb:** If you're fixing BIS modal styling, you MUST use `inject_js` (not `inject_css`) and target `frame.contentDocument` — not the main document.

### Common BIS theme issues CS sees

| Symptom | Usual root cause | Fix lives in |
|---|---|---|
| Button styling doesn't match theme's other buttons | Theme uses very specific button classes BIS doesn't inherit | CSS — restyle `#BIS_trigger` to match theme button styles |
| Button placement is wrong (above instead of replacing ATC, etc.) | Theme has non-standard product form structure | CSS positioning, occasionally HTML/Liquid placement |
| Modal opens behind other elements (z-index conflict) | Theme uses high z-index on sticky headers, chat widgets | CSS — bump `#BISModal` z-index |
| Modal too narrow / too wide on mobile | Theme's viewport meta or wrapper constraints | CSS — adjust modal width with media queries |
| Form input fields look unstyled / out of place | Theme has aggressive global input resets | CSS — restyle inputs inside `#BISModal` |
| Multi-language: button label doesn't translate | Merchant hasn't configured BIS translations OR theme uses non-standard locale switcher | Usually NOT a CSS fix — direct to BIS settings |

### What's customizable in BIS settings (no code needed)

Before suggesting code, check if it's already a setting:
- Button text, color, font size, border radius, padding
- Modal title, body text, success message
- Form field labels and placeholders
- Email/SMS/push channel toggles
- Trigger placement rules (which products, which variants)

**Rule of thumb:** if a fix can be done in BIS settings, do that instead of code.

### What's NOT customizable without code

- Custom CSS for specific edge cases (e.g., "match this theme's exact button hover animation")
- DOM placement outside BIS's auto-detection
- Conditional logic ("only show button if X")
- Anything involving the merchant's own template files

These are where CS code fixes come in.

---

## Slide Cart

### What renders on the storefront

Slide Cart replaces (or augments) the merchant's default cart experience. When a customer:
- Adds an item to cart → drawer slides in from the side (or opens as a modal, depending on config)
- Clicks the cart icon in the header → drawer opens

All Slide Cart UI is contained inside `#slidecarthq`.

### DOM structure (typical)

```
#slidecarthq
  ├─ .slidecart-overlay       (dimmed background)
  ├─ .slidecart-container     (the drawer itself)
  │   ├─ .slidecart-header    (title, close X)
  │   ├─ .slidecart-rewards   (progress bar / tiered rewards, if enabled)
  │   ├─ .slidecart-items     (line items — qty selectors, remove buttons)
  │   ├─ .slidecart-upsells   (FBT / recommended products, if enabled)
  │   ├─ .slidecart-gifts     (free gift section, if MOQ/value triggered)
  │   ├─ .slidecart-discount  (discount code box, if enabled)
  │   ├─ .slidecart-shipping  (shipping protection toggle, if enabled)
  │   └─ .slidecart-footer    (subtotal, checkout button)
```

Section visibility depends on merchant's Slide Cart configuration.

### Features that affect the DOM

| Feature | What it adds |
|---|---|
| Upsells / cross-sell | `.slidecart-upsells` section with product cards |
| Free gifts | `.slidecart-gifts` section, appears when threshold met |
| Tiered rewards | `.slidecart-rewards` progress bar at top |
| BOGO | Visual treatment on qualifying line items |
| Discount box | Input field in footer area |
| Shipping protection | Toggle row above subtotal |
| Sticky cart drawer | Drawer stays partially visible on scroll |

### Common Slide Cart theme issues CS sees

| Symptom | Usual root cause | Fix lives in |
|---|---|---|
| Drawer slides under header / nav | Theme header has high z-index | CSS — bump `#slidecarthq` z-index above header |
| Drawer is too narrow on desktop | Theme's CSS resets are constraining width | CSS — set explicit width on `.slidecart-container` |
| Product images in cart are stretched/squished | Theme's global `img` styles overriding | CSS — scope image styles inside `#slidecarthq` |
| Checkout button styling doesn't match theme | Theme has custom button classes | CSS — restyle the footer button |
| Drawer doesn't open / opens then closes immediately | Usually a JS conflict, NOT CSS | **Escalate — Part 2** |
| Upsell products look unstyled | Theme's product card CSS not inherited | CSS — restyle `.slidecart-upsells` product cards |
| Progress bar colors wrong | Merchant hasn't set them in settings | Check Slide Cart settings first |
| Mobile drawer takes full screen but should be partial (or vice versa) | Merchant's preferred behavior vs default | CSS media query on mobile widths |
| Discount box doesn't apply codes | NOT a styling issue | Escalate — likely app or Shopify discount config issue |

### What's customizable in Slide Cart settings (no code needed)

- Drawer position (left, right, modal center)
- Color scheme, fonts, button styles
- Header text, empty cart message
- Which sections appear (upsells, gifts, rewards, etc.)
- Free gift triggers (MOQ, cart value)
- Progress bar tiers and messages
- Discount box visibility
- Mobile-specific layout overrides
- Custom CSS field (yes — there's a built-in custom CSS field in Slide Cart settings for simple overrides)

**Important:** Slide Cart has a **built-in custom CSS field** in its settings. For simple, scoped CSS overrides, the cleanest place to put them is *there*, not in theme.liquid. Only fall back to theme.liquid edits when:
- The fix needs to apply *before* Slide Cart's JS loads
- The fix involves HTML/Liquid changes outside Slide Cart's wrapper
- The custom CSS field doesn't support what you need (rare)

---

## Cross-cutting technical context

### Scoping rule (critical for all CSS fixes)

Every CSS rule should be scoped under one of these IDs:
- `#slidecarthq` for Slide Cart
- `#BIS_trigger` or `#BISModal` for BIS

This prevents accidentally restyling the merchant's theme. Example:

```css
/* ❌ BAD — affects every button on the merchant's site */
button.notify-me { background: blue; }

/* ✅ GOOD — scoped to our app */
#BIS_trigger button.notify-me { background: blue; }
```

### Where CSS fixes should live

In priority order:
1. **App settings** (BIS custom CSS field, Slide Cart custom CSS field) — if available, use this. Survives theme changes.
2. **`<style>` block in `theme.liquid`** (before `</head>`) — for fixes that need to load early, or for HTML/Liquid changes.
3. **Theme's custom CSS asset** (e.g., `custom.css`, `theme.css`) — acceptable but harder to track; the theme.liquid `<style>` block is usually preferable for app-specific fixes because it's findable.

Whichever location, always include a comment header:
```css
/* Amp CS fix — ticket #XXXX — <name> — <date> */
/* Issue: <one-line description> */
```

### Things that LOOK like CSS issues but aren't

- Drawer/modal won't open → JavaScript or app config
- Form submits but customer never gets notification → backend / integration
- Discount code doesn't apply → Shopify discount config
- Cart items show wrong price → Shopify variant/pricing config
- "It works on desktop but breaks on mobile" → could be CSS, could be JS, check both
- Anything involving Shopify Markets / multi-currency → may need BIS Markets support (in development as of May 2026)

### Files CS should NEVER edit when fixing app issues

- `checkout.liquid` (Plus stores only) — Shopify owns this flow
- Anything in `/assets/` that the app installs and manages
- Theme files for **headless themes** (Hydrogen, custom storefronts) — escalate to eng
- `config/settings_data.json` — Shopify manages this

### Integrations to be aware of

BIS commonly integrates with:
- **Klaviyo** — for email flows (BIS sends signup events; Klaviyo handles delivery)
- **Mailchimp** — same pattern
- **Postscript** — for SMS

If a styling issue involves the form's behavior (e.g., "submits but doesn't add to Klaviyo list"), it's an integration/config issue, not CSS.

Slide Cart commonly integrates with:
- Discount apps (e.g., merchant uses a third-party loyalty app for discount codes)
- Shipping protection providers
- Review apps (sometimes inject elements that conflict with the drawer)

---

## What this file is and isn't

**This file is:** Context for Claude to understand Amp's products at a technical/DOM level so it can write better CSS/HTML fixes.

**This file isn't:** Pricing, strategy, churn metrics, competitive positioning, or roadmap. For business context, see `amp-context.md` (not part of the CS project).

If a CS rep asks Claude a strategy question in this project ("should we raise BIS prices?"), Claude should redirect them — that's not what this project is for.

---

## Maintenance

When apps ship new features, this file needs updating. Owners:
- **BIS sections** → BIS PM
- **Slide Cart sections** → Slide Cart PM
- **Common fixes table** → CS lead (update from real ticket patterns)
