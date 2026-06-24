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
8. **Lifecycle Hooking**: 
   - Chain the injection logic to `window.SLIDECART_LOADED`, `window.SLIDECART_UPDATED`, and `window.SLIDECART_OPENED` to ensure tiers are applied after any app state refreshes.
   - Implement an idempotency check (signature match) and a `busy` flag to prevent infinite re-render loops.
9. **Placement**: Render the snippet in `theme.liquid` before the Slide Cart app embed.

## Verification

1. **Market Gating**: Switch between markets (e.g., via Shopify's market selector) and verify that only the gifts assigned to that specific market appear in the Slide Cart.
2. **Currency Accuracy**: Verify that the thresholds in the progress bar match the `USD base * Shopify.currency.rate` calculation.
3. **Token Integrity**: Ensure the "Spend [amount] more" text renders correctly and is not blank (confirming `{% raw %}` worked).
4. **Cumulative Logic**: If multiple tiers are defined for one market, verify that they unlock cumulatively.
5. **Network**: Check the Network tab to confirm `.js` product files are fetched once per market change.
