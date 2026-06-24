---
name: slidecart-market-gwp
description: Implement market-specific Gift-With-Purchase (GWP) tiers for Slide Cart with dynamic currency conversion.
---

## Problem
The Slide Cart dashboard reward tiers are global. Merchants often need different GWP gifts and thresholds based on the customer's Shopify Market (e.g., different gifts for UK vs US), and they need these thresholds to reflect the local currency accurately based on a USD base.

Additionally, placing this logic in a `.liquid` snippet can lead to Shopify's Liquid engine stripping the `{{ amount }}` and `{{ reward }}` tokens used by Slide Cart's JS for interpolation, breaking the "Spend X more to get Y" text.

## Workflow

1. **Create a Dedicated Snippet**: Create `snippets/amp-slidecart.liquid` to keep the logic separate from `theme.liquid`.
2. **Wrap in `{% raw %}`**: Wrap the entire script in `{% raw %} ... {% endraw %}`. This is critical to prevent Shopify from evaluating `{{ amount }}` and `{{ reward }}` as Liquid variables.
3. **Define Market Mapping**: Create a `MARKET_GIFTS` object mapping market keys (e.g., `uk`, `us`, `eu`, `row`) to an array of gift objects containing the product `handle` and the `base` threshold in USD.
4. **Detect Market**: Use `window.Shopify.country` to determine the active market.
5. **Dynamic Product Loading**: 
   - Use `fetch('/products/<handle>.js')` to get the latest product data (ID, Image, Title) for the market-specific gifts.
   - This ensures the script doesn't rely on hard-coded variant IDs which can change.
6. **Currency Conversion**: 
   - Multiply the USD `base` threshold by `window.Shopify.currency.rate` to calculate the local currency threshold.
7. **Inject into Slide Cart State**:
   - Capture the merchant's desired wording (labels/text) from `window.SLIDECART_STATE().settingsBackup`.
   - Build the reward tier objects and inject them into `window.SLIDECART_STATE().settings.rewards_tiers`.
   - **Progress Bar Fix**: Set `st.settings.rewards_final_total = true` to ensure the bar measures the final total (excluding the free gifts), preventing the bar from prematurely unlocking higher tiers.
8. **Implement Auto-Add/Remove Logic**:
   - **Hidden UI**: Inject a CSS style to hide the native Slide Cart "Free Gifts" claim section (`[data-testid="FreeGifts"]`).
   - **Reconciliation Loop**: Implement a `reconcileGifts` function that:
     - Calculates the "qualifying" total by excluding all defined market gifts.
     - Adds unlocked gifts that are missing from the cart.
     - Removes gifts whose tier is no longer met.
     - Removes gifts belonging to other markets (essential for market switching).
   - **Guardrails**: Use a `reconciling` flag and a `failedAdds` map (to track sold-out products) to prevent infinite loops.
9. **Lifecycle Hooking**: 
   - Chain the injection and reconciliation logic to `window.SLIDECART_LOADED`, `window.SLIDECART_UPDATED`, and `window.SLIDECART_OPENED`.
   - Implement an idempotency check (signature match) for tiers.
10. **Placement**: Render the snippet in `theme.liquid` before the Slide Cart app embed.

## Verification

1. **Market Gating**: Switch between markets (e.g., via Shopify's market selector) and verify that only the gifts assigned to that specific market appear in the Slide Cart.
2. **Currency Accuracy**: Verify that the thresholds in the progress bar match the `USD base * Shopify.currency.rate` calculation.
3. **Token Integrity**: Ensure the "Spend [amount] more" text renders correctly and is not blank (confirming `{% raw %}` worked).
4. **Auto-Add & Removal**: 
   - Add items to cross a tier threshold and verify the gift is added automatically.
   - Remove items to drop below a threshold and verify the gift is removed.
   - Switch markets and verify that the previous market's gift is removed and the new one is added.
5. **Progress Bar Accuracy**: Verify the progress bar does not "jump" forward when a free gift is auto-added.
6. **Network**: Check the Network tab to confirm `.js` product files are fetched once per market change.
