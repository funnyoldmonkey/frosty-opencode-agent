---
name: bis-integration-filter
description: Handle requests to exclude the BIS button from specific templates or product types via the Integration Script.
---

## What I Do
I implement early-exit logic within the BIS Integration Script to prevent the "Notify Me" button from rendering on specific templates or products based on custom conditions (like product type or body classes).

## When to Use Me
- Merchant wants to remove the BIS button from specific page templates.
- Merchant wants to hide the button for specific product types (e.g., "Digital Goods").
- BIS button is flickering or appearing/disappearing incorrectly during variant changes.

## Prerequisites
- Access to the store's product pages.
- Identification of `body` classes for templates or HTML markers for product types.

## Steps
1. **Identify Markers**: Find the `body` class or a unique HTML element (like a category link) that distinguishes the pages to be excluded.
2. **Implement Early Exit**: Add a check at the start of the `BIS.popup.ready.then(...)` block to `return` if the markers are found.
3. **Unified Visibility Manager**: To fix flickers, replace fragmented visibility logic with a single `syncBISButton()` function that checks both the theme's ATC button state and BIS internal state.
4. **Immediate Hide**: Ensure the button is created with `display: none !important` and is hidden immediately upon any variant change event before the sync function runs.
5. **Verify**: Test on both excluded and included pages, and verify the first-variant-selection behavior.

## Tips
- Use `document.body.className.includes()` for template checks.
- Use `document.querySelector('a[href*="..."]')` for product category checks if no other marker exists.
- Always use `.setProperty('display', '...', 'important')` to override theme styles.
