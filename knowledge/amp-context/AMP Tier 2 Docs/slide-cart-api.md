# Slide Cart Callbacks, Methods & Globals — Support Reference
 
This document is a comprehensive reference for the Slide Cart JavaScript API exposed on the `window` object. It is intended for support agents (and AI agents) helping merchants who want to extend, observe, or control Slide Cart from their theme or third-party scripts.
 
All callbacks and methods are attached to the global `window` object and are available once Slide Cart has loaded on the storefront. Callbacks are **opt-in**: define them on `window` and Slide Cart will invoke them at the appropriate time. Methods can be called directly from any script after Slide Cart loads.
 
---
 
## Where to put this code
 
The recommended places to add these snippets:
 
1. The merchant's **theme.liquid** (or a custom asset loaded by it), inside a `<script>` tag placed **after** the Slide Cart embed snippet.
2. A custom Shopify **Theme App Extension** block, or
3. A tag-manager (Google Tag Manager, etc.) custom HTML tag.
Because Slide Cart loads asynchronously, callbacks should be **assigned, not called** — assign them before the cart fires the event (i.e., as early as possible, typically in `<head>` or top of `<body>`).
 
```html
<script>
  window.SLIDECART_LOADED = function (cart) {
    console.log('Slide Cart loaded', cart);
  };
</script>
```
 
Methods (e.g., `window.SLIDECART_OPEN()`), on the other hand, should only be invoked after the cart has loaded — easiest is to call them from inside `SLIDECART_LOADED`, a click handler, or any user-triggered event.
 
---
 
## The `cart` object
 
Most callbacks receive a `cart` argument. This is **Shopify's standard `/cart.js` response** — Slide Cart does not modify or wrap it. You can rely on all standard Shopify Ajax Cart fields. The most commonly used fields:
 
| Field | Type | Description |
|---|---|---|
| `token` | string | Unique cart token |
| `item_count` | number | Total number of items in the cart |
| `total_price` | number | Cart total in cents (e.g., `2599` = $25.99) |
| `original_total_price` | number | Total before any discounts, in cents |
| `total_discount` | number | Total discount in cents |
| `currency` | string | Cart currency code (e.g., `"USD"`) |
| `items` | array | Array of line items (see below) |
| `note` | string | Customer cart note |
| `attributes` | object | Custom cart attributes |
| `cart_level_discount_applications` | array | Active cart-level discounts |
 
Each `item` (line item) typically includes:
 
| Field | Type | Description |
|---|---|---|
| `id` | number | **Variant ID** (Shopify uses the variant id as the line `id`) |
| `key` | string | Unique line key (used for updates to a specific line) |
| `variant_id` | number | Variant ID |
| `product_id` | number | Product ID |
| `quantity` | number | Quantity of this line |
| `title` | string | Product title |
| `variant_title` | string | Variant title |
| `price` | number | Line item price in cents |
| `final_price` | number | Final per-item price after line-level discounts, in cents |
| `line_price` | number | Total line price (price × quantity), in cents |
| `final_line_price` | number | Final line total after discounts, in cents |
| `sku` | string | Variant SKU |
| `image` | string | Variant/product image URL |
| `url` | string | Product page URL |
| `properties` | object | Line item properties |
| `selling_plan_allocation` | object | Subscription / selling plan info, if any |
 
For the full schema, see Shopify's docs: https://shopify.dev/docs/api/ajax/reference/cart
 
---
 
# Callbacks
 
Each callback is **only invoked if defined**. They are fire-and-forget: return values are ignored.
 
## `window.SLIDECART_LOADED`
 
```js
window.SLIDECART_LOADED = function (cart) {
  // cart: full Shopify /cart.js cart object (see above)
};
```
 
Fires **once**, after Slide Cart finishes its initial cart fetch on page load. Use this for first-load instrumentation (analytics page view, conditional UI, etc.).
 
## `window.SLIDECART_UPDATED`
 
```js
window.SLIDECART_UPDATED = function (cart) {
  // cart: full Shopify /cart.js cart object (post-update)
};
```
 
Fires **every time the cart object changes** within Slide Cart — after adding/removing items, quantity changes, discount apply/remove, etc. Receives the latest cart object. Useful for keeping a sticky cart count or mini-cart in the theme in sync.
 
> Note: this can fire multiple times during a single user action (e.g., add-to-cart triggers both an add and an update event). Debounce in your handler if needed.
 
## `window.SLIDECART_ADD_TO_CART`
 
```js
window.SLIDECART_ADD_TO_CART = function ({ id, quantity }) {
  // id: variant id (number) being added
  // quantity: quantity added (number)
};
```
 
Fires when a user submits a Shopify add-to-cart **form** (any element with `action$="/cart/add"` or `data-slidecart-form`). The argument is a small object — it does **not** include the full line item; it's just `{ id, quantity }`.
 
> If you need richer info (final line item with product title, image, price), use `SLIDECART_ADDED_TO_CART` (below) or read the next `SLIDECART_UPDATED` event's cart payload.
 
## `window.SLIDECART_ADDED_TO_CART` (bonus — not in original doc)
 
```js
window.SLIDECART_ADDED_TO_CART = function (lineItem) {
  // lineItem: the full Shopify line item that was added/updated
};
```
 
Fires after Slide Cart's internal `addToCart` succeeds, with the matching line item from the updated cart. Useful for analytics where you need product title, price, image, etc.
 
## `window.SLIDECART_OPENED`
 
```js
window.SLIDECART_OPENED = function () {
  // no arguments
};
```
 
Fires whenever the drawer is opened (whether by `SLIDECART_OPEN()`, an add-to-cart with "open on add" enabled, or a cart-icon click).
 
## `window.SLIDECART_CLOSED`
 
```js
window.SLIDECART_CLOSED = function () {
  // no arguments
};
```
 
Fires whenever the drawer is closed.
 
## `window.SLIDECART_REMOVED_FROM_CART`
 
```js
window.SLIDECART_REMOVED_FROM_CART = function ({ id }, removedLineItem) {
  // id: variant id (number) of the removed line
  // removedLineItem: the line item object that was removed (may be undefined depending on path)
};
```
 
Fires when a line item's quantity reaches `0` (i.e., it's been removed). The second argument, when present, is the full line item snapshot from before removal.
 
## `window.SLIDECART_CHECKOUT`
 
```js
window.SLIDECART_CHECKOUT = function () {
  // no arguments
};
```
 
Fires when the customer clicks the **Checkout** button in the drawer (fires once per checkout-click sequence — not re-fired if the user double-clicks).
 
## `window.SLIDECART_UPSELL_ADD`
 
```js
window.SLIDECART_UPSELL_ADD = function (id) {
  // id: variant id (number) of the upsell variant added
};
```
 
Fires when a user adds an item from an **Upsell** or **Auto-Upsell (Aupsell)** slot in the drawer. Use this to attribute revenue to upsell flows in your analytics.
 
---
 
# Methods
 
All methods are functions on `window`. Call them after Slide Cart has loaded (i.e., from inside `SLIDECART_LOADED`, a DOM event, or once the page is fully interactive).
 
## `window.SLIDECART_OPEN()`
 
```js
window.SLIDECART_OPEN();
```
 
Opens the drawer programmatically. No arguments, no return value. Useful for binding a custom "cart" button in the theme.
 
## `window.SLIDECART_CLOSE()`
 
```js
window.SLIDECART_CLOSE();
```
 
Closes the drawer programmatically.
 
## `window.SLIDECART_UPDATE([callback])`
 
```js
window.SLIDECART_UPDATE();              // refetch + re-render
window.SLIDECART_UPDATE(function () {   // refetch + run callback when done
  window.SLIDECART_OPEN();
});
```
 
Forces Slide Cart to refetch the cart from Shopify (`/cart.js`) and re-render. Pass an optional callback that runs after the refetch completes — handy when you've just modified the cart through another script and want Slide Cart to pick up the changes before opening it.
 
## `window.SLIDECART_SET_CART(cart)`
 
```js
window.SLIDECART_SET_CART(cart);
// cart: a Shopify cart object (same shape as /cart.js response)
```
 
Replaces Slide Cart's internal cart state with the cart object you pass in (no network call). Use this when you have a fresh cart payload from your own code (e.g., from a custom add-to-cart fetch) and want Slide Cart to reflect it immediately without an extra HTTP request.
 
> The shape must match Shopify's `/cart.js` response. Passing a malformed object will break rendering.
 
## `window.SLIDECART_APPLY_DISCOUNT(code)`
 
```js
window.SLIDECART_APPLY_DISCOUNT('SUMMER10');
// code: string — a Shopify discount code
```
 
Programmatically applies a discount code to the cart, as if the customer typed it in the drawer's discount box. The code is validated against Shopify; invalid codes will be rejected and surfaced to the user the same way a manual entry would be.
 
## `window.SLIDECART_STATE()`
 
```js
const state = window.SLIDECART_STATE();
// state: the internal CartStore (MobX store)
```
 
Returns the internal Slide Cart MobX store. Useful for inspection/debugging in the browser console. Common fields on the returned store:
 
- `state.cart` — current cart object
- `state.settings` — Slide Cart settings (theme, behavior toggles, etc.)
- `state.upsells`, `state.aupsells` — currently configured upsells
- `state.discountCode` — applied discount codes
- `state.open` — whether the drawer is currently open
- `state.currency` — current currency code
> **Use with caution.** This is the live internal store. Mutating fields directly is unsupported and may cause UI bugs. Read-only inspection is fine. For supported mutations, use the methods documented above.
 
---
 
# Other useful `window` globals
 
These aren't documented in the original callbacks doc but come up regularly in support tickets:
 
| Global | Type | Effect |
|---|---|---|
| `window.SLIDECART_DISABLE` | boolean | If truthy at load time, Slide Cart does not initialize on the page. Set in theme code to suppress on specific pages. |
| `window.SLIDECART_DEV` | boolean | Enables internal dev logging. |
| `window.SLIDECART_FORMAT` | string | Override the Shopify money format (e.g., `'<span class=money>${{amount}}</span>'`). Mirrors the shop's money format string. |
| `window.SLIDECART_ENABLE_CART_REFETCH` | boolean | If true, Slide Cart refetches the cart 2s after each add-to-cart. Useful when third-party "bundle" apps mutate the cart asynchronously. |
| `window.SLIDECART_AUPSELL_AUTOPLAY` | boolean | Auto-play the auto-upsell carousel. |
| `window.SLIDECART_UPSELL_AUTOPLAY` | boolean | Auto-play the upsell carousel. |
| `window.SLIDECART_ANNOUNCEMENT_AUTOPLAY` | boolean | Auto-play the announcement banner carousel. |
| `window.SLIDECART_REWARDS_USE_TOTAL_PRICE` | boolean | Use cart total (instead of item count) for tiered-reward thresholds. |
| `window.SLIDECART_SET_FEATURE_FLAG(name, value)` | function | Override a feature flag at runtime — internal/debugging only. |
 
---
 
# Common support scenarios
 
### "How do I open the cart from a custom button?"
```html
<button onclick="window.SLIDECART_OPEN()">View cart</button>
```
 
### "How do I update my theme's cart count when the drawer changes items?"
```js
window.SLIDECART_UPDATED = function (cart) {
  document.querySelectorAll('[data-cart-count]').forEach(function (el) {
    el.textContent = cart.item_count;
  });
};
```
 
### "How do I fire an analytics event when something is added?"
```js
window.SLIDECART_ADDED_TO_CART = function (lineItem) {
  myAnalytics.track('Added to Cart', {
    variant_id: lineItem.variant_id,
    product_id: lineItem.product_id,
    quantity:   lineItem.quantity,
    price:      lineItem.price / 100,
    title:      lineItem.title,
  });
};
```
 
### "How do I auto-apply a discount via URL parameter?"
```js
window.SLIDECART_LOADED = function () {
  const code = new URLSearchParams(location.search).get('promo');
  if (code) window.SLIDECART_APPLY_DISCOUNT(code);
};
```
 
### "I added an item with my own fetch — why doesn't Slide Cart show it?"
Call `window.SLIDECART_UPDATE()` after your fetch resolves, or pass the cart you got back into `window.SLIDECART_SET_CART(cart)` to avoid the extra request.
 
### "The cart shows stale data after a bundle app modifies the cart."
Set `window.SLIDECART_ENABLE_CART_REFETCH = true;` to make Slide Cart re-fetch 2 seconds after each add. Alternatively, call `window.SLIDECART_UPDATE()` from the bundle app's own callback.
 
---
 
# Notes for AI agents handling support tickets
 
- **`id` in `SLIDECART_ADD_TO_CART`, `SLIDECART_REMOVED_FROM_CART`, and `SLIDECART_UPSELL_ADD` is always a Shopify variant ID** (number), not a product ID and not a line key.
- **Prices are always integers in cents** (Shopify convention). Divide by 100 for display.
- **Callbacks are global** — only one handler per name. If a merchant needs multiple subscribers, chain them inside a single function or wrap with their own pub/sub.
- **Methods are no-ops if Slide Cart hasn't loaded.** If a merchant reports "nothing happens when I call `SLIDECART_OPEN()`", ask whether they wait for `SLIDECART_LOADED` first, or whether `window.SLIDECART_DISABLE` is set on that page.
- **`SLIDECART_STATE()` is for debugging.** Never recommend that merchants mutate it directly — recommend the documented methods (`SLIDECART_SET_CART`, `SLIDECART_APPLY_DISCOUNT`, etc.) instead.
- If a merchant asks for a callback that doesn't exist (e.g., `on quantity changed`), the closest substitute is `SLIDECART_UPDATED` — they can diff against a stored previous cart.