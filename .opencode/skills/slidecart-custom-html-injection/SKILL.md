---
name: slidecart-custom-html-injection
description: Inject persistent custom HTML/icons into the Slide Cart footer
---

## Problem
Adding custom HTML (like trust badges, shipping info, or custom text) to the Slide Cart often results in the content disappearing when the cart re-renders (e.g., after adding an item or changing quantity).

## Workflow
1. **Identify Target**: Find a stable anchor element in the Slide Cart footer (e.g., `.trust-badge-icons` or `.button.full`).
2. **Prepare HTML**: Create the HTML string, preferably using inline styles for layout to avoid conflicts and ensure consistency.
3. **Implement Injection Logic**:
   - Check if the element already exists to avoid duplicate injections.
   - Use `parentNode.insertBefore(newElement, anchorElement)` to place content precisely.
4. **Ensure Persistence**:
   - Wrap the injection in a function.
   - Hook into `window.SLIDECART_LOADED` and `window.SLIDECART_UPDATED`.
   - Implement a `MutationObserver` on `#slidecarthq` to trigger the injection function whenever the DOM changes.

## Verification
1. Open Slide Cart.
2. Verify the custom content is visible and correctly positioned.
3. Add an item to the cart or change quantity.
4. Verify the content persists after the re-render.
