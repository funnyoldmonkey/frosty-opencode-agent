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

### 2. Implement Translation Strategy

#### Option A: State-Based Translation (Preferred for Slide Cart Rewards)
If the app provides state hooks, overwrite the configuration before the app renders. This is the most stable method and avoids performance issues.

- **Hooks:** Use `window.SLIDECART_LOADED` and `window.SLIDECART_UPDATED`.
- **Mechanism:** Access `SLIDECART_STATE().settings` and modify the target properties (e.g., `rewards_tiers`).
- **Example Pattern:**
```javascript
window.SLIDECART_UPDATED = (cart) => {
  const lang = window.Shopify?.locale;
  const translations = {
    es: { rewards: [{ label: '10% de descuento', ... }] },
    // ... other languages
  };
  
  const rewardsTexts = translations[lang]?.rewards;
  if (!rewardsTexts) return;

  SLIDECART_STATE()?.settings?.rewards_tiers.forEach((reward, idx) => {
    const t = rewardsTexts[idx];
    if (t) {
      reward.label = t.label;
      reward.pre_unlock_text = t.pre_unlock_text;
      reward.post_unlock_text = t.post_unlock_text;
    }
  });
};
```

#### Option B: Surgical DOM Translation (Use for non-state elements)
Avoid bulk `innerHTML` replacements on the root. Instead:
- **Target Specific Classes:** Use specific CSS selectors for dynamic counts (e.g., `.rewards-tiers-labels-item-amount`) and text elements (e.g., `.rewards-tiers-labels-item-label`).
- **Use `textContent` instead of `innerText`:** When CSS `text-transform: uppercase` is applied, `innerText` returns the visually transformed text. Use `textContent` to get the actual DOM text.
- **Check `innerHTML` for Already-Applied Translations:** Use `el.innerHTML.includes('targetText')` to check if a translation was already applied.

### 3. Prevent Loops (The Debounce - Required for Option B)
If using a `MutationObserver`, always wrap the translation logic in a debounced function:
```javascript
const observer = new MutationObserver(() => {
  clearTimeout(window.ampTranslationTimeout);
  window.ampTranslationTimeout = setTimeout(() => {
    translateCart();
  }, 100);
});
```

### 4. Clean Up Previous Observers (Required for Option B)
Before re-injecting the script, disconnect any existing observer:
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
