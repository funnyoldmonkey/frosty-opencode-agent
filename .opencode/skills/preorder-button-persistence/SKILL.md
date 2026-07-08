---
name: preorder-button-persistence
description: Ensures preorder button text and behavior persist across variant switches in themes with dynamic button swapping.
---

## Problem
Preorder button reverts to "Add to cart" or disappears when a user changes product variants on themes that dynamically re-render the add-to-cart form/button on variant changes.

## Workflow
1. Implement the provided mutation observer and variant-change listener script.
2. Ensure the script is injected in `theme.liquid` or a theme asset file.
3. The script will:
   - Automatically detect variant changes.
   - Re-apply `data-preorderModified` attribute.
   - Re-inject the preorder selling plan and preorder comment.

## Verification
- Select a preorder variant.
- Observe that the button text changes and selling plans are attached.
- Change to a different size/variant (also preorder).
- Ensure the button text remains the preorder text.
- Change to an in-stock variant.
- Ensure the button text reverts to the theme's original "Add to cart" text.
