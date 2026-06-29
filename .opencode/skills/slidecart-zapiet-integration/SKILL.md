---
name: slidecart-zapiet-integration
description: Integrate Zapiet delivery date/time selection into Slide Cart drawer by relocating the widget.
---

## Problem
Zapiet relies on the Shopify `/cart` page to render its delivery date and time selection widget. Slide Cart can bypass this page during the checkout flow or hide the native cart, preventing customers from selecting their delivery preferences before proceeding to checkout. Simply adding a second mount point (`#storePickupApp`) often causes ID collisions, leaving the drawer widget empty while the page-level widget remains populated.

## Workflow

1. **Suppress Native Mini-Cart**: If the theme has a native mini-cart that conflicts with Slide Cart's visibility, use CSS and a `MutationObserver` to ensure it remains hidden.
2. **Identify Zapiet Mount Point**: Zapiet typically renders its widget into an element with the ID `#storePickupApp`.
3. **Relocate the Populated Widget**:
   - Instead of creating a new mount point, find the *already populated* `#storePickupApp` element on the page.
   - Move this element into the `#slidecart-checkout-form` immediately before the checkout button.
   - This avoids ID collisions and ensures the user interacts with the active Zapiet session.
4. **Handle Delayed Rendering**:
   - If the widget is not yet rendered, ensure a mount point exists in the drawer.
   - Dispatch the `zapiet:start` custom event to trigger Zapiet's initialization.
   - Use a retry mechanism (e.g., `setTimeout`) to move the widget once it appears.
5. **Integrate with Slide Cart Lifecycles**:
   - Wrap the relocation logic in a function and call it during `window.SLIDECART_OPENED`, `window.SLIDECART_LOADED`, and `window.SLIDECART_UPDATED`.
   - Ensure previous lifecycle callbacks are preserved to avoid breaking other integrations.

## Verification

1. **Drawer Trigger**: Add an item to the cart and confirm the Slide Cart drawer opens.
2. **Widget Visibility**: Verify that the Zapiet delivery date/time selection widget is visible inside the drawer, above the checkout button.
3. **Functionality**: Select a delivery date/time within the drawer.
4. **Checkout Flow**: Click the checkout button and verify that the selection is preserved and the user is routed correctly through the checkout process.
5. **Conflict Check**: Ensure the native theme mini-cart does not reappear or overlap the drawer.
