---
name: amp-dynamic-translation
description: Translate dynamic app elements (Slide Cart, BIS) while avoiding performance death spirals.
---

# AMP Dynamic Translation Skill

Use this skill when you need to translate specific strings in a dynamic Shopify app element (like the Slide Cart or BIS Modal) that updates frequently via JavaScript.

## The Problem: The Death Spiral
Updating `innerHTML` or `innerText` inside a `MutationObserver` can trigger a new mutation, which triggers the observer again, leading to an infinite loop that freezes the browser.

## Workflow

### 1. Identify Language & Targets
- Verify the active language using `document.documentElement.lang` or `window.Shopify.locale`.
- Identify the root container (e.g., `#slidecarthq`).
- List all "Old Text" $\rightarrow$ "New Text" mappings, including required HTML tags (like `<strong>`).

### 2. Implement Surgical Translation
Avoid bulk `innerHTML` replacements on the root. Instead:
- **Target Specific Classes:** Use specific CSS selectors for dynamic counts (e.g., `.rewards-tiers-labels-item-amount`) and text elements (e.g., `.rewards-tiers-labels-item-label`).
- **Use `textContent` instead of `innerText`:** When CSS `text-transform: uppercase` is applied, `innerText` returns the visually transformed text (e.g., "GRATIS VERZENDING" instead of "Gratis verzending"). Use `textContent` to get the actual DOM text.
- **Check `innerHTML` for Already-Applied Translations:** Use `el.innerHTML.includes('targetText')` to check if a translation was already applied, preventing duplicate updates.

### 3. Prevent Loops (The Debounce)
Always wrap the translation logic in a debounced function to batch mutations. Use `clearTimeout` before setting a new timeout to prevent multiple pending executions.

```javascript
const observer = new MutationObserver(() => {
  clearTimeout(window.ampTranslationTimeout);
  window.ampTranslationTimeout = setTimeout(() => {
    translateCart();
  }, 100);
});
```

### 4. Clean Up Previous Observers
Before re-injecting the script (e.g., during debugging), disconnect any existing observer to prevent duplicate observers:

```javascript
if (window.ampTranslationObserver) {
  window.ampTranslationObserver.disconnect();
}
```

### 4. Verification
- Verify that all target strings are translated.
- Verify that HTML formatting (bold, italics) is preserved.
- **Performance Check:** Add/remove items from the cart to ensure the browser remains responsive and the translation applies immediately.

## Example Mapping Structure
```javascript
const translations = {
  'Old Dutch Text': 'Neues Deutsch Text',
  'Old Text with formatting': '<strong>New Text with formatting</strong>'
};
```
