---
name: slidecart-subscription-compare-at-fix
description: Restore original variant compare-at price in Slide Cart for subscription lines (e.g. Kaching) across all currencies.
---

## Problem
When certain subscription apps (like Kaching Automatic Refills) are used, Shopify's Cart API replaces the variant's true `compare_at_price` with the "one-time purchase price" inside the `selling_plan_allocation` object. 

Slide Cart uses this value for the strikethrough price, which makes the discount appear smaller than it actually is to the customer.

## Workflow
1. **Identify Discrepancy:** Verify if the strikethrough price in Slide Cart for a subscription item matches the one-time price instead of the variant's actual compare-at price.
2. **Inject Interceptor:** Override `window.SLIDECART_UPDATED` to intercept the cart object before it is rendered.
3. **Calculate Discount Ratio:** 
   - Fetch the product JSON (`/products/{handle}.js`).
   - For the specific variant, calculate the ratio: `ratio = variant.compare_at_price / variant.price`.
   - Store this ratio in a cache to avoid repeated network requests.
4. **Apply Ratio to Presentment Price:**
   - Multiply the `selling_plan_allocation.compare_at_price` (which is in the user's local currency) by the calculated ratio.
   - Use a small tolerance (e.g., 2 cents) to prevent floating point errors from triggering infinite re-render loops.
5. **Trigger Re-render:** Call `window.SLIDECART_SET_CART(cart)` to refresh the UI with the corrected prices.

## Verification
- Add a subscription product to the cart.
- Open Slide Cart.
- Confirm the strikethrough price matches the original product compare-at price.
- Switch currencies (if Shopify Markets is enabled) and confirm the ratio still produces the correct local compare-at price.
- Check `/cart.js` to ensure the actual billing prices (`price`, `total_price`) were not modified.
