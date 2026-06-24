---
name: bis-force-show-inline
description: Force-show an inline "Notify me when available" button on merchant-selected products, even when technically in stock.
---

## Problem
Some merchants use custom out-of-stock (OOS) logic where they suppress the "Add to Cart" button but the Shopify variant still reports `available: true`. 

By default, the BIS app gates the rendering of its signup form and button on `BIS.popup.variantIsUnavailable(variant)`. If the variant is reported as available, the app initializes nothing, making `_BISConfig.button.visible = true` ineffective because there is no UI to make visible.

## Workflow
1. **Identify Targeted Products:** Create a list of PDP URLs (or handles) where the BIS button should be forced to appear.
2. **Override Availability Check:** Inject a script that overrides `BIS.popup.variantIsUnavailable` to always return `true` for the target pages.
3. **Force UI Initialization:** 
   - Manually push the product's variants into `BIS.popup.variants`.
   - Call `BIS.popup.createUI()` to build the internal signup form and logic.
4. **Clean Up Native UI:** Hide the native floating BIS button (`.bis-button { display: none !important; }`) to avoid duplication.
5. **Inject Inline Button:**
   - Find the theme's purchase button (Add to Cart / Sold Out) to use as a styling reference.
   - Create a new `<button>` element.
   - Copy computed styles from the reference button to ensure visual consistency.
   - Set colors (e.g., black background, white text) and width to 100%.
   - Attach a click event that calls `BIS.popup.show(variantId)`.
6. **Handle Theme Re-renders:** Use a `setInterval` guard to re-inject the button if the theme's JS removes it during variant changes.

## Verification
1. **Check Target Product:** Navigate to a product in the allow-list. Confirm the custom inline button appears.
2. **Trigger Popup:** Click the inline button. Confirm the BIS signup modal opens.
3. **Verify Payload:** Use the Network tab to ensure the form submission contains the correct `product_no` and `variant_no`.
4. **Check Non-Target Product:** Navigate to a product NOT in the allow-list. Confirm the custom button does NOT appear and native BIS behavior remains.
5. **Test In-Stock Variant:** Verify that the button appears even on variants that are technically "available" in Shopify.
