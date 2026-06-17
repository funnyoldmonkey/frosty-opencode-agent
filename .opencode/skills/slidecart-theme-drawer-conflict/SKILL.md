---
name: slidecart-theme-drawer-conflict
description: Handle conflicts between Slide Cart and theme native drawers that cause mobile scrolling issues.
---

# Slide Cart Theme Drawer Conflict

When Slide Cart is set to "Drawer" mode, it may conflict with the Shopify theme's own cart drawer, often resulting in the page becoming non-scrollable on mobile after the cart is closed (due to overlapping overlays).

## Troubleshooting Steps

1. **Identify the Conflict**
   - Open the store on a mobile emulator.
   - Open the Slide Cart and then close it.
   - Attempt to scroll the page. If it's blocked, inspect the DOM for overlays (e.g., `.slidecarthq-overlay` or theme-specific drawer overlays) that have `opacity: 0` but `pointer-events: auto`.

2. **Apply the Setting Fix**
   - Change the Slide Cart setting from **Drawer** to **Page**.
   - Verify that the scrolling issue is resolved.

3. **Restore Slide Cart Behavior**
   - Changing the setting to "Page" will cause "Add to Cart" buttons and cart links to navigate to the `/cart` page instead of opening the Slide Cart.
   - Implement an integration script to restore the AJAX behavior.

## Implementation Script

Inject the following script into `theme.liquid` or as a custom script to intercept cart interactions:

```javascript
(function () {
  // 1) Cart icon / cart links -> open SlideCart instead of navigating to /cart
  document.addEventListener('click', function (e) {
    var link = e.target.closest('a.header-controls__cart, a[href="/cart"], a[href^="/cart?"]');
    if (link && typeof window.SLIDECART_OPEN === 'function') {
      e.preventDefault();
      window.SLIDECART_OPEN();
    }
  }, true);

  // 2) Add-to-cart: intercept the CLICK in capture phase, AJAX-add, then open SlideCart
  //    after a 500ms delay to ensure the item is registered first.
  document.addEventListener('click', function (e) {
    var btn = e.target.closest('button[name="add"], .product__add-to-cart-button');
    if (!btn) return;
    var form = btn.closest('form[action*="/cart/add"]');
    if (!form) return;
    if (typeof window.SLIDECART_OPEN !== 'function') return;

    e.preventDefault();
    e.stopImmediatePropagation();

    btn.setAttribute('disabled', 'disabled');
    fetch('/cart/add.js', {
      method: 'POST',
      headers: { 'Accept': 'application/json' },
      body: new FormData(form)
    })
      .then(function (r) { return r.json(); })
      .then(function () {
        if (typeof window.SLIDECART_UPDATE === 'function') {
          try { return window.SLIDECART_UPDATE(); } catch (err) {}
        }
      })
      .then(function () {
        return new Promise(function (resolve) { setTimeout(resolve, 500); }); // 500ms delay
      })
      .then(function () { window.SLIDECART_OPEN(); })
      .catch(function () { form.submit(); }) // fallback: native submit if AJAX fails
      .finally(function () { btn.removeAttribute('disabled'); });
  }, true);
})();
```

## Verification
- [ ] Cart links open the Slide Cart drawer without navigating.
- [ ] Adding a product to the cart opens the Slide Cart drawer without navigating.
- [ ] Closing the Slide Cart does not block page scrolling on mobile.
