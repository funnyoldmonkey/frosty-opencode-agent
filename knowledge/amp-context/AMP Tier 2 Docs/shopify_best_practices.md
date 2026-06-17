# Shopify Theme Troubleshooting & Best Practices — Tier 2 Support Reference

**Purpose:** Comprehensive reference for Frosty when handling Shopify theme issues, CSS fixes, performance optimization, and app integration debugging. This is the primary playbook for Tier 2 support.

**Last updated:** June 2026

---

## 1. Shopify Theme Architecture (Online Store 2.0)

### Core Concepts

- **JSON Templates** define page structure as data (which sections appear and their config). Liquid handles rendering.
- **Sections** are modular, reusable components. Up to **25 sections per template**.
- **Blocks** are sub-components within sections. Up to **50 blocks per section**. Blocks can be nested (parent-child).
- **Theme Blocks** (latest architecture) support all OS 2.0 features plus advanced customization.

### Template Types & Body Classes

| Page Type | Body Class | Template File |
|---|---|---|
| Homepage | `.template-index` | `templates/index.json` |
| Product | `.template-product` | `templates/product.json` |
| Collection | `.template-collection` | `templates/collection.json` |
| Cart | `.template-cart` | `templates/cart.json` |
| Blog | `.template-blog` | `templates/blog.json` |
| Article | `.template-article` | `templates/article.json` |
| Page | `.template-page` | `templates/page.json` |
| Search | `.template-search` | `templates/search.json` |
| 404 | `.template-404` | `templates/404.json` |

### Key Layout Files

- `layout/theme.liquid` — master layout wrapping all pages. Contains `<head>`, header, footer, and `{{ content_for_layout }}`
- `layout/checkout.liquid` — checkout layout (Plus stores only, **never edit for app fixes**)
- `sections/header.liquid` — site header/nav
- `sections/footer.liquid` — site footer

### How App Embeds & App Blocks Inject DOM

Understanding this is critical for debugging CSS conflicts:

**App Embed Blocks:**
- Injected via JavaScript before `</head>` or `</body>` closing tags
- Target locations: `compliance_head`, `head`, or `body`
- Run across ALL pages — not page-specific
- Use JS to inject functionality (not inline HTML/CSS)
- Toggled on/off in Theme Editor → App Embeds panel

**App Blocks:**
- Liquid-based blocks merchants add to specific sections
- Render inline content within a section
- Page-specific — only appear where placed
- Can be added/removed/reordered in Theme Editor

**AMP apps (BIS, Slide Cart) use app embeds** — they inject DOM via JavaScript on page load. This means:
- Their elements won't exist in the initial HTML source
- They appear in the DOM after JS executes
- DevTools "Elements" tab shows them, but "View Source" doesn't
- Timing matters — elements may not exist until user interaction (e.g., BIS trigger only appears when variant is OOS)

---

## 2. CSS Best Practices for Theme Fixes

### Scoping Rules (CRITICAL)

Every CSS rule for an app fix MUST be scoped to prevent breaking the merchant's theme:

```css
/* ❌ BAD — affects every button on the site */
button { background: blue; }

/* ❌ BAD — too broad */
.modal { z-index: 9999; }

/* ✅ GOOD — scoped to our app's container */
#slidecarthq .slidecart-footer button { background: blue; }
#BIS_trigger button.notify-me { background: blue; }
```

### Specificity Hierarchy

When a merchant's theme overrides app styles, increase specificity:

```css
/* Level 1: Class selector (specificity 0,1,0) */
.slidecart-container { width: 400px; }

/* Level 2: ID + class (specificity 1,1,0) */
#slidecarthq .slidecart-container { width: 400px; }

/* Level 3: Double ID or !important (last resort) */
#slidecarthq .slidecart-container { width: 400px !important; }
```

**Avoid `!important` unless absolutely necessary.** It makes future fixes harder. Prefer increasing selector specificity.

### Where to Place CSS Fixes (Priority Order)

1. **App's built-in custom CSS field** (BIS settings, Slide Cart settings) — survives theme changes, scoped to the app
2. **`<style>` block in `theme.liquid`** before `</head>` — for fixes that must load early or affect elements outside the app wrapper
3. **Theme's `assets/custom.css`** or equivalent — acceptable but harder to track across support tickets

**Always include a comment header:**
```css
/* Amp CS fix — <date> — <ticket/store> */
/* Issue: <one-line description> */
#slidecarthq .slidecart-header { ... }
```

### Common CSS Patterns for Theme Conflicts

**Z-index conflicts (most common):**
```css
/* Slide Cart drawer behind sticky header */
#slidecarthq { z-index: 999999 !important; }
#slidecarthq .slidecart-overlay { z-index: 999998 !important; }

/* BIS modal behind elements */
/* Note: BIS modal is in an iframe — see iframe section */
#BIS_frame { z-index: 999999 !important; position: relative; }
```

**Width/layout conflicts:**
```css
/* Theme constraining drawer width */
#slidecarthq .slidecart-container {
  width: 400px !important;
  max-width: 90vw !important;
}

/* Mobile full-width override */
@media (max-width: 749px) {
  #slidecarthq .slidecart-container {
    width: 100vw !important;
  }
}
```

**Font/typography inheritance:**
```css
/* Theme's font not inherited by app */
#slidecarthq {
  font-family: inherit;
  font-size: 14px;
  line-height: 1.5;
  color: inherit;
}
```

**Image aspect ratio issues:**
```css
/* Theme's global img rules distorting app images */
#slidecarthq img {
  width: auto;
  height: auto;
  max-width: 100%;
  object-fit: contain;
}
```

### Responsive Design Patterns

Always test on mobile. Common breakpoints across Shopify themes:

| Breakpoint | Description |
|---|---|
| `max-width: 749px` | Mobile (most themes) |
| `min-width: 750px` and `max-width: 989px` | Tablet |
| `min-width: 990px` | Desktop |
| `min-width: 1400px` | Large desktop |

Dawn and most modern themes use `750px` as the mobile/desktop breakpoint.

---

## 3. Liquid Quick Reference

### Essential Objects

| Object | Description | Common Use |
|---|---|---|
| `product` | Current product | `product.title`, `product.variants`, `product.available` |
| `product.selected_or_first_available_variant` | Active variant | Check if variant is in stock |
| `collection` | Current collection | `collection.products`, `collection.title` |
| `cart` | Shopping cart | `cart.items`, `cart.total_price`, `cart.item_count` |
| `shop` | Store info | `shop.name`, `shop.url`, `shop.currency` |
| `customer` | Logged-in customer | `customer.email`, `customer.tags` |
| `request` | Current request | `request.page_type`, `request.path` |
| `template` | Current template | `template.name`, `template.suffix` |
| `settings` | Theme settings | Access theme editor values |

### Essential Filters

```liquid
{{ product.title | escape }}              <!-- HTML-safe output -->
{{ product.price | money }}               <!-- Format as currency -->
{{ product.price | money_with_currency }} <!-- With currency code -->
{{ 'image.png' | asset_url }}             <!-- Theme asset URL -->
{{ 'image.png' | file_url }}              <!-- Uploaded file URL -->
{{ product.featured_image | img_url: '300x' }}  <!-- Sized image -->
{{ 'now' | date: '%Y-%m-%d' }}            <!-- Current date -->
{{ product.description | strip_html | truncate: 150 }} <!-- Clean text -->
```

### Debugging Liquid

```liquid
<!-- Dump variable as JSON to inspect structure -->
{{ product | json }}

<!-- Check object type -->
{{ variable | type }}

<!-- Conditional debugging -->
{% if template.name == 'product' %}
  <!-- Debug output here -->
{% endif %}
```

**Use `render` (not `include`)** — `render` scopes variables locally, `include` is deprecated and causes variable leaks.

---

## 4. Performance & Core Web Vitals

### Current Metrics (2026)

| Metric | Good | Needs Improvement | Poor |
|---|---|---|---|
| **LCP** (Largest Contentful Paint) | ≤ 2.5s | 2.5s – 4.0s | > 4.0s |
| **INP** (Interaction to Next Paint) | ≤ 200ms | 200ms – 500ms | > 500ms |
| **CLS** (Cumulative Layout Shift) | ≤ 0.1 | 0.1 – 0.25 | > 0.25 |

**Note:** Google replaced FID with INP in March 2024. If a merchant mentions FID, redirect to INP.

### Common Performance Killers on Shopify

1. **Third-party app script bloat** — #1 cause of failing CWV. Review widgets, chat apps, analytics trackers, popups.
2. **Unoptimized images** — Missing `loading="lazy"`, no explicit dimensions (causes CLS), oversized files.
3. **Render-blocking CSS/JS** — External fonts, non-critical CSS in `<head>`, synchronous scripts.
4. **Too many apps** — Each app embed adds JS that runs on every page load.

### Quick Wins for Performance

```liquid
<!-- Lazy load below-fold images -->
{{ product.featured_image | image_url: width: 600 | image_tag: loading: 'lazy', width: 600, height: 400 }}

<!-- Preload hero/LCP image -->
<link rel="preload" as="image" href="{{ section.settings.image | image_url: width: 1200 }}">

<!-- Defer non-critical JS -->
<script src="{{ 'custom.js' | asset_url }}" defer></script>
```

### CLS Debugging

Common CLS causes on Shopify:
- Images without explicit `width`/`height` attributes
- Fonts loading late and causing text reflow (FOUT)
- App embeds injecting content above the fold after page load
- Dynamic banners/announcements that push content down

```css
/* Prevent CLS from late-loading app embeds */
.announcement-bar { min-height: 40px; }
.header-wrapper { min-height: 64px; }
```

### Tools for Performance Analysis

- **Shopify Theme Inspector for Chrome** — visualizes Liquid render profiling (server-side)
- **Chrome DevTools Lighthouse tab** — full CWV audit
- **Chrome DevTools Performance tab** — trace recording for INP
- **performance.shopify.com** — Shopify's official theme performance benchmarks
- **PageSpeed Insights** — Google's field + lab data
- **Chrome DevTools MCP `lighthouse_audit`** — Frosty can run this directly

---

## 5. Debugging Workflow with DevTools

### Step-by-Step Process

1. **Console tab first** — check for red errors. Common ones:
   - `Uncaught ReferenceError: $ is not defined` → jQuery not loaded before script
   - `404 (Not Found)` on assets → file missing or path wrong
   - `Uncaught TypeError: Cannot read properties of null` → element doesn't exist yet (timing issue)

2. **Elements tab** — inspect the DOM:
   - Right-click element → Inspect
   - Check computed styles for inherited overrides
   - Look for `display: none`, `visibility: hidden`, `opacity: 0`
   - Check z-index stacking (computed tab)

3. **Network tab** — check resource loading:
   - Filter by CSS/JS to find load failures
   - Check file sizes (large files = slow)
   - Look for 3rd-party domains loading too many resources

4. **Application tab** — check cookies, localStorage, sessionStorage for app state issues

### Quick Diagnostic Commands (for `evaluate_script`)

```javascript
// Check if app element exists
document.querySelector('#slidecarthq') !== null

// Get computed z-index
getComputedStyle(document.querySelector('#slidecarthq')).zIndex

// List all stylesheets affecting an element
document.querySelector('#slidecarthq').computedStyleMap()

// Check total CSS size (for AMP pages)
document.querySelector('style[amp-custom]')?.textContent.length

// Find conflicting z-index values
document.querySelectorAll('*').forEach(el => {
  const z = getComputedStyle(el).zIndex;
  if (z !== 'auto' && parseInt(z) > 999) {
    console.log(el.tagName, el.id || el.className, 'z-index:', z);
  }
});

// Check if element is inside an iframe
document.querySelector('#BIS_frame')?.contentDocument?.querySelector('#BISModal')

// Get all loaded scripts (find app conflicts)
[...document.querySelectorAll('script[src]')].map(s => s.src)
```

---

## 6. Common Issue Patterns & Fixes

### A. App Element Not Visible

**Symptoms:** Button, drawer, or modal doesn't appear at all.

**Diagnostic steps:**
1. Check if element exists in DOM (`evaluate_script` → `document.querySelector(...)`)
2. If exists but invisible → check `display`, `visibility`, `opacity`, `height: 0`, `overflow: hidden`
3. If not in DOM → check if app embed is enabled in Theme Editor
4. For BIS: check if variant is actually OOS (button only shows for OOS variants)
5. Check console for JS errors from the app

### B. Z-Index / Layering Conflicts

**Symptoms:** Drawer opens behind header, modal behind overlay, etc.

**Fix pattern:**
1. Find the z-index of the overlapping element
2. Set app element's z-index higher
3. Check for `position` — z-index only works on positioned elements (`relative`, `absolute`, `fixed`, `sticky`)
4. Check for stacking contexts — `transform`, `opacity < 1`, `filter`, `will-change` create new stacking contexts

### C. Layout Shift / Content Jump

**Symptoms:** Page content jumps when app element loads or when drawer opens.

**Fix pattern:**
1. Reserve space for app elements with `min-height`
2. Use `position: fixed` or `position: absolute` for overlays (not `relative`)
3. Ensure drawer doesn't push body content (should overlay)

### D. Mobile-Specific Issues

**Symptoms:** Works on desktop, broken on mobile.

**Common causes:**
- Theme uses different DOM structure for mobile (responsive vs. separate markup)
- Touch events vs. click events
- Viewport meta tag issues
- `100vw` causing horizontal scroll (doesn't account for scrollbar on some browsers)

**Fix pattern:**
```css
@media (max-width: 749px) {
  #slidecarthq .slidecart-container {
    width: 100% !important; /* not 100vw */
    max-height: 100vh;
    overflow-y: auto;
  }
}
```

### E. Theme Update Broke the Fix

**Symptoms:** Previously working fix stopped working after theme update.

**Diagnostic steps:**
1. Check if fix is still present in the code
2. If in theme.liquid → may have been overwritten by theme update
3. If in app custom CSS field → should survive (check app settings)
4. Compare DOM structure before/after — class names may have changed
5. Recommend: always place fixes in the app's custom CSS field when possible

### F. Residual App Code

**Symptoms:** Ghost scripts, broken layouts, console errors from uninstalled apps.

**Fix:** Search theme code for references to the app:
```liquid
<!-- Search theme files for app remnants -->
{% comment %} Look for script tags, link tags, or Liquid includes referencing the app {% endcomment %}
```

Check: `theme.liquid`, `layout/theme.liquid`, snippets folder, and assets folder for leftover files.

---

## 7. Files You Should NEVER Edit

- `checkout.liquid` / `checkout/*.liquid` — Shopify-managed checkout (Plus stores only)
- `config/settings_data.json` — Shopify manages this; manual edits break Theme Editor
- App-installed assets in `/assets/` that the app manages and may overwrite
- Theme files for headless storefronts (Hydrogen, custom) — escalate to engineering
- `locales/*.json` — editing directly can break translations; use Theme Editor

---

## 8. Useful Shopify URLs & Tools

| Resource | URL |
|---|---|
| Shopify Liquid Reference | https://shopify.dev/docs/api/liquid |
| Shopify Cheat Sheet | https://www.shopify.com/partners/shopify-cheat-sheet |
| Theme Performance Benchmarks | https://performance.shopify.com |
| Theme Check (linter) | `shopify theme check` CLI command |
| Shopify Theme Inspector | Chrome extension for Liquid profiling |
| PageSpeed Insights | https://pagespeed.web.dev |
| Dawn Theme Source | https://github.com/Shopify/dawn |

---

## 9. Escalation Rules

**Escalate to engineering (do NOT attempt CSS fix) when:**
- Drawer/modal won't open or closes immediately → JS conflict
- Form submits but backend action doesn't happen → integration/webhook issue
- Discount codes don't apply → Shopify discount config
- Cart shows wrong price → Shopify variant/pricing
- Issue only on headless/Hydrogen storefronts
- Checkout page issues
- Anything requiring `checkout.liquid` edits
- Shopify Markets / multi-currency edge cases
