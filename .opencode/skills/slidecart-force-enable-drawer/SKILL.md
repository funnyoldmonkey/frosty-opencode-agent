---
name: slidecart-force-enable-drawer
description: Fixes cases where Slide Cart drawer doesn't render (only overlay shows) by forcing `settings.enabled = true` and overriding theme drawer triggers.
---

## Problem
The merchant reports that clicking the cart icon triggers the page overlay (the background goes dark), but the Slide Cart drawer itself never appears. 

This typically happens when:
1. `window.SLIDECART_STATE().settings.enabled` is `null` or `false`, preventing the React app from rendering.
2. The theme has its own cart drawer logic that triggers an overlay (e.g., adding classes like `.js-drawer-open` to the body) but doesn't actually open a drawer, or blocks the Slide Cart from appearing.

## Workflow
1. **Verify the state**
   - Open DevTools console.
   - Run `window.SLIDECART_STATE().settings.enabled`. If it returns `null` or `false`, the app is suppressed.
   - Check if the body gets a class like `js-drawer-open` or `active-pop-up` when clicking the cart icon.

2. **Inject the Force-Enable Script**
   Add the following script to `theme.liquid` or the Slide Cart snippet to force the app to render and intercept theme triggers.

\`\`\`javascript
(function () {
  if (window.__ampSlideCartFix) return;
  window.__ampSlideCartFix = true;

  var slidecartReady = false;
  var pendingOpen = false;

  // 1. Define theme triggers that should open Slide Cart
  var CART_TRIGGER_SELECTOR =
    '.js-drawer-open-button-right, #cart-icon-bubble, .header-cart, .btn-to-drawer';

  // 2. Force-enable the app state
  function ensureEnabled() {
    try {
      var s = window.SLIDECART_STATE && window.SLIDECART_STATE();
      if (s && s.settings) {
        if (s.settings.enabled !== true) s.settings.enabled = true;
        return true;
      }
    } catch (e) {}
    return false;
  }

  function openSlideCart() {
    // Clear theme-specific overlays that block the UI
    document.body.classList.remove('js-drawer-open', 'active-pop-up');
    ensureEnabled();
    if (slidecartReady && typeof window.SLIDECART_OPEN === 'function') {
      window.SLIDECART_OPEN();
    } else {
      pendingOpen = true;
    }
  }

  // 3. Intercept clicks in capture phase to override theme behavior
  document.addEventListener('click', function (e) {
    var trigger = e.target.closest && e.target.closest(CART_TRIGGER_SELECTOR);
    if (!trigger) return;
    e.preventDefault();
    e.stopImmediatePropagation();
    openSlideCart();
  }, true);

  // 4. Sync with Slide Cart lifecycle
  var prevLoaded = window.SLIDECART_LOADED;
  window.SLIDECART_LOADED = function (cart) {
    slidecartReady = true;
    ensureEnabled();
    if (typeof prevLoaded === 'function') { try { prevLoaded(cart); } catch (err) {} }
    if (pendingOpen && typeof window.SLIDECART_OPEN === 'function') {
      pendingOpen = false;
      window.SLIDECART_OPEN();
    }
  };

  var prevOpened = window.SLIDECART_OPENED;
  window.SLIDECART_OPENED = function () {
    ensureEnabled();
    if (typeof prevOpened === 'function') { try { prevOpened(); } catch (e) {} }
  };

  // 5. Initial polling to set state before app fully loads
  var tries = 0;
  var poll = setInterval(function () {
    tries++;
    if (typeof window.SLIDECART_OPEN === 'function') slidecartReady = true;
    var ok = ensureEnabled();
    if ((ok && slidecartReady) || tries > 60) clearInterval(poll);
  }, 100);
})();
\`\`\`

## Verification
- [ ] Click the cart icon: the drawer should open immediately.
- [ ] Ensure no theme-specific overlay classes (`js-drawer-open`, etc.) remain on the `<body>` when the drawer is open.
- [ ] Run `window.SLIDECART_STATE().settings.enabled` in console and verify it is `true`.
