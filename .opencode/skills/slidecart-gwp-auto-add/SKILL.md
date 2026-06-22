---
name: slidecart-gwp-auto-add
description: Auto-adds gift-with-purchase in Slide Cart when reward tier is reached and removes it below threshold.
---
## Problem
Slide Cart rewards were showing manual "AJOUTER" buttons instead of automatically adding the free gift to the cart when the threshold was met. This was likely due to a custom script failing or missing standard Slide Cart configuration/state access.

## Workflow
1. Identify the issue where GWP is not auto-added.
2. Verify that `SLIDECART_STATE()` is available.
3. Inject a custom script that listens to `SLIDECART_UPDATED` and `SLIDECART_LOADED`.
4. The script reads reward tiers from `SLIDECART_STATE().settings.rewards_tiers`.
5. It calculates qualifying cart amount/count (excluding gifts).
6. It uses `/cart/add.js` and `/cart/change.js` to add/remove gifts.
7. It calls `window.SLIDECART_UPDATE()` to refresh the UI.

## Verification
1. Increase cart quantity to reach a reward tier.
2. Verify the GWP item is automatically added to the cart.
3. Decrease quantity below the threshold.
4. Verify the GWP item is automatically removed.
