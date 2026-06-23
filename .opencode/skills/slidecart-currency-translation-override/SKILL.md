---
name: slidecart-currency-translation-override
description: Fix Slide Cart currency mismatches and dynamic string translations using Shopify API and lifecycle hooks.
---

## Problem
When a Shopify store's base currency differs from the app's internal settings (e.g., store is PLN, app is EUR), Slide Cart may display a raw value (e.g., 2.95 zł) that doesn't match the actual converted price added to the cart (e.g., 13,00 zł). Additionally, some dynamic labels in the cart footer may remain in English.

## Workflow

### 1. Identify Targets
- Locate the `handle` and `variant_id` of the product being used for Shipping Protection.
- Identify the exact English strings that need translation (e.g., "Discounts" $\rightarrow$ "Rabaty").

### 2. Implement Price Override
- **Fetch Real Price:** Use `fetch('/products/{handle}.js')` to get the current price of the variant in the store's active currency.
- **Dynamic Formatting:** Create a `formatMoney` function that prioritizes `window.SLIDECART_FORMAT`, then `window.Shopify.money_format`, and finally a default fallback.

### 3. Implement Lifecycle Hooks
- **Wrap Callbacks:** To avoid clobbering existing app logic, wrap `window.SLIDECART_LOADED`, `window.SLIDECART_UPDATED`, and `window.SLIDECART_OPENED`.
- **Execution:** Trigger the price update and translation logic on each of these events.

### 4. Ensure Persistence
- Use a `MutationObserver` on `#slidecarthq` with `subtree: true` and `characterData: true` to re-apply fixes whenever the cart content updates.

### 5. Code Pattern
```javascript
(function () {
  // 1. State & Constants
  var PROTECTION_HANDLE = '...', PROTECTION_VARIANT_ID = ...;
  var translations = { 'Old Text': 'New Text' };

  // 2. Money Formatter
  function formatMoney(cents) { ... }

  // 3. API Fetch
  function loadPrice() {
    return fetch('/products/' + PROTECTION_HANDLE + '.js').then(...)
  }

  // 4. Application Logic
  function apply() {
    var root = document.querySelector('#slidecarthq');
    if (!root) return;
    // Update Price
    // Update Translations
  }

  // 5. Lifecycle Integration
  var oldLoaded = window.SLIDECART_LOADED;
  window.SLIDECART_LOADED = function(c) {
    if (oldLoaded) oldLoaded(c);
    loadPrice().then(apply);
  };
  // Repeat for UPDATED and OPENED

  // 6. DOM Observer
  new MutationObserver(apply).observe(root, { childList: true, subtree: true });
})();
```

## Verification
1. **Price Check:** Add Shipping Protection to the cart. Verify the displayed price matches the actual increase in the subtotal.
2. **Translation Check:** Verify that all target strings are correctly translated.
3. **Persistence Check:** Add/remove items or change variants to ensure the fix persists after the cart re-renders.
