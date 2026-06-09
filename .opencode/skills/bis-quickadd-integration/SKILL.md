---
name: bis-quickadd-integration
description: Integrate BIS buttons into Shopify quick-add drawers or popups with variant awareness and performance optimization.
---

# BIS Quick-Add Integration Skill

This skill describes the workflow for adding the Back in Stock (BIS) trigger to dynamic elements like quick-add drawers that are not recognized as Product Detail Pages (PDPs) by the BIS app.

## Core Challenges
1. **PDP Restriction**: The BIS app often restricts popup initialization to PDPs using `BIS.urlIsProductPage()`.
2. **Mutation Loops**: Monitoring dynamic drawers can cause infinite loops if the observer modifies the DOM it's watching.
3. **Theme CSS Overrides**: Theme button classes (like `btn--secondary`) may have opacity or visibility transitions that hide the button.
4. **Variant Sync**: The BIS modal needs the current variant ID to show the correct product.

## Implementation Workflow

### 1. Enable BIS Logic
Spoof the `BIS.urlIsProductPage` method to return `true` when the quick-add drawer is present.
```javascript
if (window.BIS && typeof window.BIS.urlIsProductPage === 'function') {
  var origUrl = window.BIS.urlIsProductPage;
  window.BIS.urlIsProductPage = function() {
    if (document.querySelector('quick-add-drawer')) return true;
    return origUrl.apply(this, arguments);
  };
}
```

### 2. Performance-Optimized Observation
Use a `MutationObserver` combined with `requestAnimationFrame` and **Strict State Checking** (comparing current value vs target value) to prevent browser freezes.

### 3. Styling for Instant Visibility
Avoid theme button classes. Use pure inline styles to ensure the button is visible immediately and bypasses theme-specific transitions.

### 4. Variant-Aware Triggering
The BIS `genericTriggerHandler` requires:
- **Class**: `BIS_trigger`
- **Attribute**: `data-product-handle` (the product handle)
- **Attribute**: `data-variant-id` (the current variant ID from `input[name="id"]`)

## Verification Checklist
- [ ] Button appears only when the variant is sold out.
- [ ] Button is visible immediately (no hover required).
- [ ] Switching variants in the drawer updates the `data-variant-id` on the button.
- [ ] Clicking the button opens the BIS modal with the correct variant selected.
- [ ] Page performance remains smooth (no "perma-loading" or freezes).
