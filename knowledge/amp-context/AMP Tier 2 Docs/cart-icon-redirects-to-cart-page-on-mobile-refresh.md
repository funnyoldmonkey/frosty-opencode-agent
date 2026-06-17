---
title: Cart icon redirects to /cart page when tapped during mobile page refresh
app: Slide Cart
themes: any
tags: cart-redirect, race-condition, mobile-only, theme-js
severity: normal
last_verified: 2026-05-06
author: Amp support team
---
 
# Cart icon redirects to /cart page when tapped during mobile page refresh
 
## Symptom
 
On mobile, when a customer refreshes the storefront and quickly taps the cart icon before the page fully loads, the browser navigates them to the theme's `/cart` page instead of opening the Slide Cart drawer. Letting the page fully load first makes the drawer open as expected. Reproduces reliably on slow connections; harder to catch on fast desktop.
 
## Cause
 
The theme's cart icon is a standard anchor link (`<a href="/cart">`). Slide Cart loads asynchronously and only attaches its click interceptor once it's ready. If the customer taps during the window between the icon being rendered and Slide Cart binding its handler, the browser follows the native link.
 
Not a bug in Slide Cart per se — a race condition that affects any third-party cart drawer on any Shopify theme. The CS reply *"this is intended behavior"* is inaccurate and should be avoided.
 
## Solution
 
Two approaches have shipped successfully:
 
### Option A — Disable the cart icon until Slide Cart loads (team-preferred)
 
This is what was applied for `luxyourlife.com` on the Atlas theme (Helpscout #108150). A snippet is added that disables interaction on the theme's cart icon until `SLIDECART_LOADED` fires. The CS lead has the exact code from the Atlas implementation — paste it into a new `snippets/amp-slidecart-edits.liquid` file and render it from `theme.liquid`. **[Insert the team's actual 63-line snippet here when next applied — currently lives in merchant theme code, needs to be captured.]**
 
### Option B — Intercept the click and queue it
 
Cleaner UX (no visibly dead icon during load), but slightly more code. Drop the following into `theme.liquid` as close to the top of `<head>` as possible, **before** the Slide Cart embed snippet:
 
```html
<script>
(function () {
  var slidecartReady = false;
  var pendingOpen = false;
 
  // Cart-icon selectors common across Shopify themes.
  // Add any theme-specific selector here if needed.
  var CART_ICON_SELECTOR =
    'a[href$="/cart"], #cart-icon-bubble, .cart-link, ' +
    '.header__icon--cart, [data-cart-icon], .site-header__cart';
 
  // Capture-phase listener so we run BEFORE the browser follows the link.
  document.addEventListener('click', function (e) {
    var target = e.target.closest && e.target.closest(CART_ICON_SELECTOR);
    if (!target) return;
 
    e.preventDefault();
    e.stopPropagation();
 
    if (slidecartReady && window.SLIDECART_OPEN) {
      window.SLIDECART_OPEN();
    } else {
      pendingOpen = true;
    }
  }, true); // capture: true is critical
 
  // Chain onto SLIDECART_LOADED instead of overwriting it.
  var prevLoaded = window.SLIDECART_LOADED;
  window.SLIDECART_LOADED = function (cart) {
    slidecartReady = true;
    if (typeof prevLoaded === 'function') {
      try { prevLoaded(cart); } catch (err) {}
    }
    if (pendingOpen && window.SLIDECART_OPEN) {
      pendingOpen = false;
      window.SLIDECART_OPEN();
    }
  };
 
  // Safety net: if Slide Cart never loads, release the lock after 3s.
  setTimeout(function () {
    if (!slidecartReady && pendingOpen) {
      pendingOpen = false;
      window.location.href = '/cart';
    }
  }, 3000);
})();
</script>
```
 
## Scope and caveats
 
- Affects every Slide Cart install on every Shopify theme on mobile, in principle. We just don't hear about it unless a merchant tests the exact sequence (refresh, then tap before load).
- Selectors in Option B cover Dawn-family, OS 2.0 defaults, and most common themes. Custom themes may need an extra selector — inspect the cart icon in DevTools and add its selector to the list.
- Option A produces a visibly disabled icon during page load. On slow 3G connections this can be noticeable (1–3s).
- Option B keeps the icon visually live; the tap is queued and fired the moment Slide Cart is ready.
- Both approaches are reversible — just remove the snippet.
## Merchant-ready reply
 
> Hi there,
>
> Thanks for spotting this — you're right that the cart icon can briefly fall back to the theme's `/cart` page if it's tapped before Slide Cart has finished loading. It's a race condition between your theme's HTML link and our drawer's click interceptor, not the intended behavior.
>
> I've added a snippet to your theme that prevents the cart icon from following the native link until Slide Cart is ready. On a fast tap during page load, the drawer will now open as soon as it's loaded instead of sending the customer to the cart page.
>
> The changes are in [file locations]. Please test on your phone with a hard refresh and let me know if anything looks off.
 
## Related
 
- `T2 docs/Cart Page Redirection in Showcase Theme (1) ...md` — same root cause, theme-specific fix
- `T2 docs/Fix Cart Page redirection in Broadcast theme (1) ...md` — same root cause, Broadcast theme
- `T2 docs/Fix cart page redirection (Impulse theme) ...md` — Impulse theme variant
- `T2 docs/Hide cart drawer and fix Cart Page redirection (Minimog Theme) ...md` — Minimog
- `T2 docs/Pursuit Theme Cart Icon Redirecting to Cart Page ...md` — Pursuit
- Helpscout #108150 (Apr 15, 2026) — original ticket that drove this fix
- **Product opportunity:** five theme-specific fix docs all addressing the same race condition. Strong candidate for a one-time addition to the Slide Cart embed itself. File as Linear ticket.