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
- **Target Leaf Nodes:** Iterate through all elements and only replace text in elements that have no children (`el.children.length === 0`).
- **Target Specific Classes:** Use specific CSS selectors for dynamic counts (e.g., `.rewards-tiers-labels-item-amount`).

### 3. Prevent Loops (The Debounce)
Always wrap the translation logic in a debounced function to batch mutations.

```javascript
function debounce(func, wait) {
  let timeout;
  return function(...args) {
    clearTimeout(timeout);
    timeout = setTimeout(() => func.apply(this, args), wait);
  };
}

const debouncedTranslate = debounce(translateCart, 100);
const observer = new MutationObserver(debouncedTranslate);
observer.observe(rootElement, { childList: true, subtree: true });
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
