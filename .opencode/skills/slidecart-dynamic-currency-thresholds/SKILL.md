---
name: slidecart-dynamic-currency-thresholds
description: Handle per-currency free shipping threshold overrides in Slide Cart using runtime JS.
---

## Problem
Merchants often need different free shipping thresholds depending on the customer's currency (e.g., $150 USD vs $200 AUD). Slide Cart's native reward tier settings are global and do not support per-currency logic out of the box.

## Workflow

1.  **Identify the target thresholds**: Define a mapping of currency codes to target amounts (e.g., `{ USD: "150.00", AUD: "200.00" }`).
2.  **Access Slide Cart State**: Use `window.SLIDECART_STATE()` to access the current settings and rewards tiers.
3.  **Inject Runtime Override**:
    - Create a function `applyThreshold()` that:
        - Detects the current currency via `SLIDECART_STATE().currency` or `window.Shopify.currency.active`.
        - Locates the first reward tier (`state.settings.rewards_tiers[0]`).
        - Updates the `amount` to the target threshold.
        - **Crucial**: Also updates `state.settingsBackup.rewards_tiers[0].amount` to ensure the change persists through internal app updates.
        - Calls `window.SLIDECART_UPDATE()` to refresh the UI.
    - Use a flag (e.g., `applying = true`) to prevent infinite loops caused by `SLIDECART_UPDATED` triggering `applyThreshold`.
4.  **Attach Event Listeners**: Listen to the following events to ensure the threshold is applied whenever the cart or currency changes:
    - `slidecart:open`
    - `SLIDECART_UPDATED`
    - `shopify:currency:change`
    - `window:pageshow` (for browser back/forward)
    - A couple of `setTimeout` calls as a safety net for late-loading scripts.

## Verification

1.  **Verify Threshold in USD**:
    - Set currency to USD.
    - Open Slide Cart.
    - Verify the progress bar/rewards label shows the $150 threshold.
2.  **Verify Threshold in AUD**:
    - Set currency to AUD.
    - Open Slide Cart.
    - Verify the progress bar/rewards label shows the $200 threshold.
3.  **Verify Persistence**:
    - Add/remove items to trigger `SLIDECART_UPDATED` and ensure the threshold remains correct.
