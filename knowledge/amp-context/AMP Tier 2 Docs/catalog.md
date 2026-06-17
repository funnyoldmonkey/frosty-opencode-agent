
raw
# Fix Catalog
 
Single source of truth for documented support fixes. When a ticket comes in, search this file first.
 
The catalog has two layers:
 
1. **Curated fixes** — docs in the new template format under `fixes/`. Hand-reviewed, with structured frontmatter and a known-good code snippet. These are the high-confidence entries.
2. **Legacy archive (auto-catalogued)** — every doc in `T2 docs/` that the previous team wrote. The titles and file paths are exact; the `Themes` and `Tags` columns are heuristic-generated and may include false positives. Use these as a starting point and read the underlying file to confirm.
**How to read this:**
- `App` — which Amp app the fix is for.
- `Themes` — which Shopify themes the fix applies to. `any` means theme-agnostic.
- `Tags` — issue category and keywords. Use these to filter.
- `File` — relative path to the full fix doc.
- `Status` — `template` means converted to the new template format (in `fixes/`); `legacy` means original archive doc.
**How to add a row (new fix):**
1. Document the fix using `_template-fix.md` (save to `fixes/`).
2. Add a row under the relevant app's **Curated fixes** section. Keep the summary one line.
3. Use lowercase, hyphenated tags. Stick to existing tag names — see "Tag glossary" at the bottom.
**How to upgrade a legacy entry to curated:**
1. Rewrite the legacy doc using `_template-fix.md`, save to `fixes/<short-name>.md`.
2. Add a row under the relevant app's **Curated fixes** section.
3. Remove the corresponding row from the legacy archive section (or mark it `[superseded]`).
---
 
## Curated fixes
 
### Slide Cart — curated
 
| Title | App | Themes | Tags | Status | File |
|---|---|---|---|---|---|
| Cart icon redirects to /cart page when tapped during mobile page refresh | Slide Cart | any | cart-redirect, race-condition, mobile-only, theme-js | template | `fixes/cart-icon-redirects-to-cart-page-on-mobile-refresh.md` |
 
### BIS — curated
 
*No BIS fixes have been curated yet.*
 
### Bundles — curated
 
*No Bundles fixes have been curated yet.*
 
### Lifetimely — curated
 
*No Lifetimely fixes have been curated yet.*
 
---
 
## Legacy archive (auto-catalogued)
 
The 306 docs below were imported in bulk from `T2 docs/` and classified by a heuristic script. Treat them as searchable but not authoritative — open the underlying file before applying any fix. Theme and tag accuracy is approximately 80–90%; expect some false positives (e.g., a doc tagged `mobile-only` may discuss mobile but apply more broadly).
 
 
### Slide Cart — full archive (auto-catalogued)
 
| Title | Themes | Tags | Status | File |
|---|---|---|---|---|
| "DO NOT DELETE - Advanced Descriptions Assets" was removed by the merchant. | any | rewards | legacy | `T2 docs/DO NOT DELETE - Advanced Descriptions Assets was r 35aa41d3e45b80fb8034e54312ae5474.md` |
| Add a Custom Tag to items from an specific Collection | any | cart-items, styling, custom-app | legacy | `T2 docs/Add a Custom Tag to items from an specific Collect 35aa41d3e45b80c49985d1e54d4dbf6f.md` |
| Add a toggle button to display/hide the custom properties | any | styling, custom-app, programmatic, hover | legacy | `T2 docs/Add a toggle button to display hide the custom pro 35aa41d3e45b803886a9e5ce31bb69c4.md` |
| ADD button and titles from free gift section in tier rewards are too big | any | styling, upsell, free-gift, rewards | legacy | `T2 docs/ADD button and titles from free gift section in ti 35aa41d3e45b80e48f21cfb63d4423fc.md` |
| Add continue shopping button on empty cart | any | checkout-button, cart-button, empty-cart, styling, svg-icon, rewards | legacy | `T2 docs/Add continue shopping button on empty cart (1) 35aa41d3e45b80bd8ddad8de34911a16.md` |
| Add custom elements on empty cart screen | any | empty-cart, styling, race-condition, custom-app | legacy | `T2 docs/Add custom elements on empty cart screen (1) 35aa41d3e45b8038af1cce7539962512.md` |
| Add custom shipping thresholds for other currencies | any | styling, svg-icon, shipping, rewards, multi-currency, programmatic | legacy | `T2 docs/Add custom shipping thresholds for other currencie 35aa41d3e45b8003b77be50e80b4b186.md` |
| Add discount code from shared URL | any | discount-code, programmatic, url-param | legacy | `T2 docs/Add discount code from shared URL (1) 35aa41d3e45b80879d50fb2148d68cf7.md` |
| Add discount code when adding it from the cart page (Prestige v.10 theme) | Prestige | discount-code, programmatic-open, programmatic | legacy | `T2 docs/Add discount code when adding it from the cart pag 35aa41d3e45b80c18d54fe0d778131eb.md` |
| Add Image To Shipping Protection Widget | any | styling, shipping-protection | legacy | `T2 docs/Add Image To Shipping Protection Widget (1) 35aa41d3e45b8082873ff898de0629e9.md` |
| Add more than 1 T&C Checkbox and enable the Checkout button when these are checked. | any | checkout-button, styling, terms-checkbox, programmatic-open, programmatic | legacy | `T2 docs/Add more than 1 T&C Checkbox and enable the Checko 35aa41d3e45b8080ade7ef6e6449b377.md` |
| Add Multiple Products to Cart with One Button (With loader animation) | any | discount-code, programmatic-open, programmatic | legacy | `T2 docs/Add Multiple Products to Cart with One Button (Wit 35aa41d3e45b8025b66ee0e71e3c9448.md` |
| Add payment icon image below checkout button | any | checkout-button, styling | legacy | `T2 docs/Add payment icon image below checkout button (1) 35aa41d3e45b805e976bf21e7c6c4738.md` |
| Add payment icon image below checkout button with translation | any | checkout-button, svg-icon, multi-language, custom-app | legacy | `T2 docs/Add payment icon image below checkout button with  35aa41d3e45b8067b26ace11f06c1645.md` |
| Add SVG icon - Checkout button | any | checkout-button, styling, svg-icon, mobile-only | legacy | `T2 docs/Add SVG icon - Checkout button (1) 35aa41d3e45b8015b905e3a5b02d0800.md` |
| Add the store logo to the header | any | styling | legacy | `T2 docs/Add the store logo to the header (1) 35aa41d3e45b8017b5aaef20cf146d63.md` |
| Add the store logo to the header | any | styling, programmatic | legacy | `T2 docs/Add the store logo to the header (1) 35aa41d3e45b80bc924ce5de1dd020d0.md` |
| Add to Cart button Adding doubled qty to Slide Cart | any | cart-redirect, atc-button, cart-icon, quantity-bug | legacy | `T2 docs/Add to Cart button Adding doubled qty to Slide Car 35aa41d3e45b80038282f826383e272a.md` |
| Add To Cart Event not tracked in Shopify Analytics | any | atc-button, analytics, atc-tracking, programmatic | legacy | `T2 docs/Add To Cart Event not tracked in Shopify Analytics 35aa41d3e45b80c4b052d25aeea1de55.md` |
| Add Unit Price value to cart items | any | cart-items, styling, programmatic | legacy | `T2 docs/Add Unit Price value to cart items (1) 35aa41d3e45b80b38c60c13571d08bd5.md` |
| Add Zapiet Widget To Upsell Cart | any | styling, upsell, zapiet | legacy | `T2 docs/Add Zapiet Widget To Upsell Cart (1) 35aa41d3e45b80fd86bbe5e452977856.md` |
| Add-To-Cart button redirecting to cart page in Palo Alto theme | Palo Alto | cart-redirect, atc-button, programmatic | legacy | `T2 docs/Add-To-Cart button redirecting to cart page in Pal 35aa41d3e45b80429d93fd1dfc517173.md` |
| Add-To-Cart button redirecting to cart page in Prestige theme | Prestige | cart-redirect, atc-button, theme-js | legacy | `T2 docs/Add-To-Cart button redirecting to cart page in Pre 35aa41d3e45b8076aa65d6d08917c562.md` |
| Adding a Button that Redirects to the Cart Page | any | cart-redirect, styling, checkout | legacy | `T2 docs/Adding a Button that Redirects to the Cart Page (1 35aa41d3e45b80109a27d4e6dc377f16.md` |
| Adding a Dropdown Arrow to the Embedded Upsell | any | styling, svg-icon, upsell | legacy | `T2 docs/Adding a Dropdown Arrow to the Embedded Upsell (1) 35aa41d3e45b8054a792cd33167454e8.md` |
| Adding a lock icon to the checkout button in Conversion cart | any | checkout-button | legacy | `T2 docs/Adding a lock icon to the checkout button in Conve 35aa41d3e45b8038b76dfcbcb071bdec.md` |
| Adding a lock icon to the checkout button in Conversion cart | any | checkout-button | legacy | `T2 docs/Adding a lock icon to the checkout button in Conve 35aa41d3e45b80c69714cdc2aab96baa.md` |
| Adding a Sub-Title to the Upsells Section | any | styling, upsell | legacy | `T2 docs/Adding a Sub-Title to the Upsells Section (1) 35aa41d3e45b80bab96bf9db8f207116.md` |
| Adding Compare-At Price | any | cart-items, multi-currency | legacy | `T2 docs/Adding Compare-At Price (1) 35aa41d3e45b80469297e347b9eae707.md` |
| Adding compare-at-price with Manual Discount | any | styling, multi-language, multi-currency, programmatic | legacy | `T2 docs/Adding compare-at-price with Manual Discount (1) 35aa41d3e45b809ca353db517e358838.md` |
| Adding Custom HTML below the Checkout Button | any | checkout-button, custom-app | legacy | `T2 docs/Adding Custom HTML below the Checkout Button (1) 35aa41d3e45b8072864cef382115878a.md` |
| Adjusting the Gap between Compare-at Price and Price | any | styling | legacy | `T2 docs/Adjusting the Gap between Compare-at Price and Pri 35aa41d3e45b8095a175e21d20cea7f4.md` |
| Advanced Product Descriptions - APD is not showing for the Porto theme | any | untagged | legacy | `T2 docs/Advanced Product Descriptions - APD is not showing 35aa41d3e45b8034a89cf3d5210c330c.md` |
| AMP Cart Not Appearing with “Uncaught SyntaxError: missing }…” | any | console-error, multi-currency | legacy | `T2 docs/AMP Cart Not Appearing with “Uncaught SyntaxError  35aa41d3e45b8028a1bec3504e1828fe.md` |
| AMP Upsells - update the cart icon for Prestige theme | Prestige | cart-icon, upsell | legacy | `T2 docs/AMP Upsells - update the cart icon for Prestige th 35aa41d3e45b8024b5f3fcd442e8f06f.md` |
| Announcement section scroll automatically | any | announcement, programmatic-open, programmatic | legacy | `T2 docs/Announcement section scroll automatically (1) 35aa41d3e45b8033a078d7f97a57edb7.md` |
| Announcement section taking up screen height in Safari browsers | any | styling, announcement | legacy | `T2 docs/Announcement section taking up screen height in Sa 35aa41d3e45b80f793ecd59ad6a84776.md` |
| AP toggles a lot of times when opening the + sectionsAppHQ | any | styling, ui-bug | legacy | `T2 docs/AP toggles a lot of times when opening the + secti 35aa41d3e45b801199aaca2ad4f1b48f.md` |
| App not working for add-on options products | any | cart-icon, ui-bug, programmatic-open, programmatic | legacy | `T2 docs/App not working for add-on options products (1) 35aa41d3e45b8026a09cd56f7c0ddb5b.md` |
| Approaching an integration for Weglot and SlideCart | any | weglot, multi-language, programmatic, legacy-theme | legacy | `T2 docs/Approaching an integration for Weglot and SlideCar 35aa41d3e45b8001b65ecef78241aee7.md` |
| ATC button from a custom app doesn't open Slide Cart | any | atc-button, custom-app, programmatic-open, programmatic | legacy | `T2 docs/ATC button from a custom app doesn't open Slide Ca 35aa41d3e45b8079a927da2bcf80d2d5.md` |
| ATC button from Replo not opening upsells app | any | atc-button, upsell, replo, third-party-page-builder | legacy | `T2 docs/ATC button from Replo not opening upsells app (1) 35aa41d3e45b80e3b799c55547186901.md` |
| ATC button redirects to the cart page | any | cart-redirect, atc-button | legacy | `T2 docs/ATC button redirects to the cart page (1) 35aa41d3e45b80dbb6cdf184e0394574.md` |
| ATC event listener for Kalles theme | Kalles | atc-button, programmatic-open, programmatic | legacy | `T2 docs/ATC event listener for Kalles theme (1) 35aa41d3e45b80d0a1fac7390e304ec9.md` |
| Attach Subtotal next to the Checkout button | any | checkout-button, styling, mobile-only | legacy | `T2 docs/Attach Subtotal next to the Checkout button (1) 35aa41d3e45b8026b8abf16a5de47fd0.md` |
| Auto Scroll Announcements In Upsell Cart | any | upsell, announcement | legacy | `T2 docs/Auto Scroll Announcements In Upsell Cart (1) 35aa41d3e45b807ebad7fb640c0b0e32.md` |
| Automatically Add BxGy Gift | any | styling, upsell, free-gift, rewards, custom-app, programmatic | legacy | `T2 docs/Automatically Add BxGy Gift (1) 35aa41d3e45b80d0a5a8df6226962a52.md` |
| Automatically Add Or Remove BxGy Gifts Priced At 0 | any | free-gift, checkout, custom-app | legacy | `T2 docs/Automatically Add Or Remove BxGy Gifts Priced At 0 35aa41d3e45b8065be75e47cacec5b73.md` |
| Automatically convert first tier reward currency | any | rewards, multi-currency, programmatic | legacy | `T2 docs/Automatically convert first tier reward currency ( 35aa41d3e45b806ab236d0e7393b99d7.md` |
| Avoid compare-at-price overlapping with the final price item | any | styling | legacy | `T2 docs/Avoid compare-at-price overlapping with the final  35aa41d3e45b80758674fc81289aed42.md` |
| BoGo / BxGy Discount Quantity Issues | any | programmatic | legacy | `T2 docs/BoGo BxGy Discount Quantity Issues (1) 35aa41d3e45b801598dcf7c3743015ca.md` |
| Button to Clear/Empty the Cart | any | cart-button, empty-cart, upsell, checkout | legacy | `T2 docs/Button to Clear Empty the Cart (1) 35aa41d3e45b80549a4eed8c12c54176.md` |
| Cart bubble count sync with Taste/Dawn/Denim theme | Dawn, Taste | cart-icon, cart-count, programmatic | legacy | `T2 docs/Cart bubble count sync with Taste Dawn Denim theme 35aa41d3e45b80388cffe00c9b000888.md` |
| Cart Count Sync Habitat theme | any | cart-count | legacy | `T2 docs/Cart Count Sync Habitat theme (1) 35aa41d3e45b806a8a9bfdee48c5d232.md` |
| Cart count sync with Be Yours theme | Be Yours | cart-count, programmatic | legacy | `T2 docs/Cart count sync with Be Yours theme (1) 35aa41d3e45b80ce8358df8eb5fed579.md` |
| Cart Count sync with Blum Theme | any | cart-icon, cart-count | legacy | `T2 docs/Cart Count sync with Blum Theme (1) 35aa41d3e45b8036a216ec954e5b22dd.md` |
| Cart count sync with Broadcast theme | Broadcast | cart-count, styling | legacy | `T2 docs/Cart count sync with Broadcast theme (1) 35aa41d3e45b8051a488cd1aa3f94ee6.md` |
| Cart count sync with Canopy theme | any | cart-count | legacy | `T2 docs/Cart count sync with Canopy theme (1) 35aa41d3e45b804d87cecacbc00061f1.md` |
| Cart count sync with Dawn/Spotlight theme | Dawn, Spotlight | cart-count | legacy | `T2 docs/Cart count sync with Dawn Spotlight theme (1) 35aa41d3e45b804bab1dedfc70a5cd6c.md` |
| Cart count sync with Debut theme | Debut | cart-count, programmatic | legacy | `T2 docs/Cart count sync with Debut theme (1) 35aa41d3e45b8042a307f00fcf800713.md` |
| Cart count sync with Debutify theme | any | cart-count, programmatic | legacy | `T2 docs/Cart count sync with Debutify theme (1) 35aa41d3e45b80c2870de645554c13f3.md` |
| Cart count sync with Empire theme | Empire | cart-icon, cart-count, programmatic | legacy | `T2 docs/Cart count sync with Empire theme (1) 35aa41d3e45b805dac62ebbe4d0022dd.md` |
| Cart count sync with Flow theme | any | cart-count | legacy | `T2 docs/Cart count sync with Flow theme (1) 35aa41d3e45b8034aca8f40ca17bb988.md` |
| Cart count sync with Horizon theme | any | cart-count, programmatic | legacy | `T2 docs/Cart count sync with Horizon theme (1) 35aa41d3e45b802491b8e19c60a8bb4f.md` |
| Cart count sync with Impact theme | Impact | cart-count, shipping-protection, programmatic | legacy | `T2 docs/Cart count sync with Impact theme (1) 35aa41d3e45b800d90d5ca8226b5b3dc.md` |
| Cart Count sync with Impulse Theme | Impulse | cart-icon, cart-count | legacy | `T2 docs/Cart Count sync with Impulse Theme (1) 35aa41d3e45b80a08a0de361e5736d26.md` |
| Cart Count sync with Impulse Theme | Impulse | cart-icon, cart-count | legacy | `T2 docs/Cart Count sync with Impulse Theme (1) 35aa41d3e45b80dfacbdec69999dafde.md` |
| Cart count sync with Impulse theme | Impulse | cart-count, programmatic | legacy | `T2 docs/Cart count sync with Impulse theme (1) 35aa41d3e45b8047a059e570192bf8f8.md` |
| Cart count sync with Ira theme | any | cart-count, programmatic | legacy | `T2 docs/Cart count sync with Ira theme (1) 35aa41d3e45b8021ae5fd6b7e30ed42e.md` |
| Cart count sync with Loft theme | Loft | cart-count, svg-icon, programmatic | legacy | `T2 docs/Cart count sync with Loft theme (1) 35aa41d3e45b807c89a6e65e49af49ae.md` |
| Cart count sync with Prestige theme | Prestige | cart-count, programmatic | legacy | `T2 docs/Cart count sync with Prestige theme (1) 35aa41d3e45b803cb723e509bdb006d0.md` |
| Cart count sync with Reformation theme | any | cart-count, programmatic | legacy | `T2 docs/Cart count sync with Reformation theme (1) 35aa41d3e45b8027a003e1f0304f4bec.md` |
| Cart count sync with Refresh theme | Refresh | cart-count | legacy | `T2 docs/Cart count sync with Refresh theme (1) 35aa41d3e45b803ea68cf4a14e842ed3.md` |
| Cart count sync with Release theme | any | cart-count, programmatic | legacy | `T2 docs/Cart count sync with Release theme (1) 35aa41d3e45b800db9cae41fd35c3f34.md` |
| Cart count sync with Showcase theme | Showcase | cart-icon, cart-count, programmatic | legacy | `T2 docs/Cart count sync with Showcase theme (1) 35aa41d3e45b80ecaa16e2c2f3818141.md` |
| Cart Count sync with Siletto Theme | any | cart-count, shipping-protection, programmatic | legacy | `T2 docs/Cart Count sync with Siletto Theme (1) 35aa41d3e45b8002805cfd4a87046bb8.md` |
| Cart Count sync with Streamline Theme | Streamline | cart-icon, cart-count | legacy | `T2 docs/Cart Count sync with Streamline Theme (1) 35aa41d3e45b80498d54cfa639397441.md` |
| Cart count sync with Streamline theme | Streamline | cart-count, programmatic | legacy | `T2 docs/Cart count sync with Streamline theme (1) 35aa41d3e45b80a38a39c264cd49d26e.md` |
| Cart count sync with Style theme | any | cart-count, programmatic-open, programmatic | legacy | `T2 docs/Cart count sync with Style theme (1) 35aa41d3e45b802aa6f4d3c7cd03c359.md` |
| Cart count sync with Superstore theme | any | cart-count, styling | legacy | `T2 docs/Cart count sync with Superstore theme (1) 35aa41d3e45b80e38d65e2735e651cd4.md` |
| Cart count sync with Themekit theme | any | cart-count, programmatic | legacy | `T2 docs/Cart count sync with Themekit theme (1) 35aa41d3e45b8060a7f9f681897350fa.md` |
| Cart count sync with Turbo theme | Turbo | cart-count, programmatic | legacy | `T2 docs/Cart count sync with Turbo theme (1) 35aa41d3e45b8061b437fd9972330394.md` |
| Cart count sync with Umino Theme | any | cart-count | legacy | `T2 docs/Cart count sync with Umino Theme (1) 35aa41d3e45b804e95f8d841b2536b23.md` |
| Cart Page Redirection in Showcase Theme | Showcase | cart-redirect, cart-icon, theme-js, programmatic-open, programmatic | legacy | `T2 docs/Cart Page Redirection in Showcase Theme (1) 35aa41d3e45b804abfdffe926c3c1703.md` |
| Change announcement text based on page location | any | announcement, theme-js, programmatic | legacy | `T2 docs/Change announcement text based on page location (1 35aa41d3e45b808dbfb8dd9d1f26bd59.md` |
| Change Appstle Subscription line properties within SlideCart. | any | subscriptions, programmatic | legacy | `T2 docs/Change Appstle Subscription line properties within 35aa41d3e45b800289b3d5a51dc1b761.md` |
| Change Gift Image when changing the variant option | any | programmatic | legacy | `T2 docs/Change Gift Image when changing the variant option 35aa41d3e45b80448722fa349b1c39a1.md` |
| Change Gift Image when changing the variant option | any | programmatic | legacy | `T2 docs/Change Gift Image when changing the variant option 35aa41d3e45b80988d26fc6b100895ea.md` |
| Change Reward Thresholds Based On Country | any | rewards, programmatic | legacy | `T2 docs/Change Reward Thresholds Based On Country (1) 35aa41d3e45b8089a261f61623d2062e.md` |
| Change rewards based on other countries. | any | styling, svg-icon, rewards, third-party-app | legacy | `T2 docs/Change rewards based on other countries (1) 35aa41d3e45b80edb4b2f23e0a07e154.md` |
| Change rewards condition to be available to the customer when they buy the same item twice. | any | cart-count, rewards, custom-app, programmatic | legacy | `T2 docs/Change rewards condition to be available to the cu 35aa41d3e45b80ffa6f8f1a4cb402cef.md` |
| Change Shipping rates dynamically based on a custom code | any | shipping, multi-currency, programmatic | legacy | `T2 docs/Change Shipping rates dynamically based on a custo 35aa41d3e45b80a5a7a0e76eb7921b54.md` |
| Change the reward module value based on the currency | any | rewards, multi-currency, programmatic-open, programmatic | legacy | `T2 docs/Change the reward module value based on the curren 35aa41d3e45b80908812c9fbe1bb3995.md` |
| Change X (remove item button) into a different text or image | any | styling, svg-icon | legacy | `T2 docs/Change X (remove item button) into a different tex 35aa41d3e45b8062a5a7fce264cac3f5.md` |
| Change X (remove item button) into text → Remove | any | styling, svg-icon | legacy | `T2 docs/Change X (remove item button) into text → Remove ( 35aa41d3e45b800482e5f82623ea6c81.md` |
| Change X (remove item button) into trash can icon | any | styling | legacy | `T2 docs/Change X (remove item button) into trash can icon  35aa41d3e45b808c9a06c25b8a2a1cf5.md` |
| Change, translate tiered rewards, and adjust shipping rates based on other currencies | any | shipping, rewards, multi-language, multi-currency, programmatic | legacy | `T2 docs/Change, translate tiered rewards, and adjust shipp 35aa41d3e45b80798ec1e1cd6ec31047.md` |
| Changed location of promotion and footer jumps up and down | any | styling, upsell | legacy | `T2 docs/Changed location of promotion and footer jumps up  35aa41d3e45b80eea5d9f9317ccab62a.md` |
| Changing the embedded upsell image on variant dropdown selection | any | upsell | legacy | `T2 docs/Changing the embedded upsell image on variant drop 35aa41d3e45b80f3a598e5c70396eab9.md` |
| Changing variation number to a string | any | programmatic | legacy | `T2 docs/Changing variation number to a string (1) 35aa41d3e45b80b4a9f1ee87737ebba3.md` |
| Closing variant pop up when opens slide cart, and sync header counter – Empire theme | Empire | atc-button, cart-icon | legacy | `T2 docs/Closing variant pop up when opens slide cart, and  35aa41d3e45b800cb0e5e2143766dfb5.md` |
| Compare price code stop working when a product with no discount is added to the cart | any | programmatic | legacy | `T2 docs/Compare price code stop working when a product wit 35aa41d3e45b8069be8beb093bb2430f.md` |
| Compare price with - District theme | District | styling, third-party-app, programmatic | legacy | `T2 docs/Compare price with - District theme (1) 35aa41d3e45b8055a5f6c3ae8cc9ab40.md` |
| Compare-At Price and Sale Price Overlapping in Mobile View | any | styling, mobile-only | legacy | `T2 docs/Compare-At Price and Sale Price Overlapping in Mob 35aa41d3e45b803dab30f2bb54a6bf56.md` |
| Configure AMP Upsells for Broadcast theme | Broadcast | atc-button, cart-icon, upsell | legacy | `T2 docs/Configure AMP Upsells for Broadcast theme (1) 35aa41d3e45b80cbadf1e6a60f13591a.md` |
| Configure SlideCart - Eurus theme | Eurus | atc-button, cart-icon, styling, programmatic-open, programmatic | legacy | `T2 docs/Configure SlideCart - Eurus theme (1) 35aa41d3e45b8004b02dfd0b64b68063.md` |
| Configure SlideCart - Eurus theme | Eurus | atc-button, cart-icon, styling, programmatic-open, programmatic | legacy | `T2 docs/Configure SlideCart - Eurus theme (1) 35aa41d3e45b80cfa118cc292d282f20.md` |
| Configure SlideCart - Shark theme | any | cart-redirect, atc-button, programmatic | legacy | `T2 docs/Configure SlideCart - Shark theme (1) 35aa41d3e45b80c98812dd78ffcee02d.md` |
| Configure SlideCart - Solodrop theme | any | cart-icon, styling, checkout | legacy | `T2 docs/Configure SlideCart - Solodrop theme (1) 35aa41d3e45b80028010f8c65a61566a.md` |
| Configure SlideCart - Streamline theme | Streamline | atc-button, cart-icon, styling, custom-app | legacy | `T2 docs/Configure SlideCart - Streamline theme (1) 35aa41d3e45b80448c2ee2111ae8e000.md` |
| Configure SlideCart - Yuva theme | any | atc-button, checkout | legacy | `T2 docs/Configure SlideCart - Yuva theme (1) 35aa41d3e45b80c18a98de0e81c410ba.md` |
| Configure SlideCart with Zipify add to cart buttons | any | atc-button, checkout, programmatic-open, programmatic | legacy | `T2 docs/Configure SlideCart with Zipify add to cart button 35aa41d3e45b80e3a643e00c8c4ec1c3.md` |
| Configure Upsells - Blum theme | any | cart-redirect, cart-icon, cart-count, upsell | legacy | `T2 docs/Configure Upsells - Blum theme (1) 35aa41d3e45b80dea12ce33bad4ef747.md` |
| Convert Announcement Text into a Link | any | announcement | legacy | `T2 docs/Convert Announcement Text into a Link (1) 35aa41d3e45b80db8637e336fb2672e9.md` |
| Converting an Announcement into a Link | any | styling, announcement, programmatic | legacy | `T2 docs/Converting an Announcement into a Link (1) 35aa41d3e45b8030bee2ed6261035f82.md` |
| Create a checkout button on Slide Cart | any | cart-redirect, checkout-button, theme-js, multi-language, programmatic | legacy | `T2 docs/Create a checkout button on Slide Cart (1) 35aa41d3e45b80159898f6fe54943441.md` |
| Create a Close button on Super Bar but only on mobile | any | styling, mobile-only | legacy | `T2 docs/Create a Close button on Super Bar but only on mob 35aa41d3e45b8013b114f7debff5b510.md` |
| Currency Bear integration | any | upsell, multi-currency, programmatic | legacy | `T2 docs/Currency Bear integration (1) 35aa41d3e45b808e8d19c3c44a5bfbe1.md` |
| Custom Icons for Rewards Bar | any | styling, svg-icon, rewards, theme-js, custom-app, programmatic | legacy | `T2 docs/Custom Icons for Rewards Bar (1) 35aa41d3e45b8053bfebfefe64d11392.md` |
| Customily Integration | any | programmatic | legacy | `T2 docs/Customily Integration (1) 35aa41d3e45b80bab257c0fa568c49a5.md` |
| Customize the Content of the Add Button in Upsell Options Selection | any | styling, svg-icon, upsell, custom-app, programmatic | legacy | `T2 docs/Customize the Content of the Add Button in Upsell  35aa41d3e45b80b8bccdfaf1dc1353ae.md` |
| Customize the error message when a product cannot be added | any | styling, custom-app, programmatic | legacy | `T2 docs/Customize the error message when a product cannot  35aa41d3e45b804089bbc82e5acc68da.md` |
| Disable Cart Drawer - Next theme | any | programmatic-open, programmatic | legacy | `T2 docs/Disable Cart Drawer - Next theme (1) 35aa41d3e45b80f19c22d8c5099b4724.md` |
| Disable native theme cart drawer - New york theme | any | styling, programmatic | legacy | `T2 docs/Disable native theme cart drawer - New york theme  35aa41d3e45b8079a6edc9365eb9a019.md` |
| Disable SC for products with GPO App | any | cart-icon, theme-js, programmatic | legacy | `T2 docs/Disable SC for products with GPO App (1) 35aa41d3e45b8016a6c2c62cb0f95c5c.md` |
| Disable Slide Cart Using Customer Tags | any | rewards, custom-app, programmatic | legacy | `T2 docs/Disable Slide Cart Using Customer Tags (1) 35aa41d3e45b80dd9137feb81c009b51.md` |
| Disable the theme built-in pop up - Pipline | any | untagged | legacy | `T2 docs/Disable the theme built-in pop up - Pipline (1) 35aa41d3e45b806898a3ee470621d3fc.md` |
| Disable the Upsells sections when a specific product is added to the cart. | any | upsell | legacy | `T2 docs/Disable the Upsells sections when a specific produ 35aa41d3e45b8031bec4dc1de3305f1e.md` |
| Discount Code not being removed | any | discount-code, checkout, programmatic | legacy | `T2 docs/Discount Code not being removed (1) 35aa41d3e45b80328f21d06f60ff7c6b.md` |
| Display different announcements depending on user location | any | announcement, programmatic | legacy | `T2 docs/Display different announcements depending on user  35aa41d3e45b80dcbd4ac2f3ffee8d6c.md` |
| Display price per unit on Slide Cart | any | cart-items, multi-currency, programmatic | legacy | `T2 docs/Display price per unit on Slide Cart (1) 35aa41d3e45b80b5a1e2cde9a6e870ff.md` |
| Display subtotal inside the Checkout button | any | checkout-button, programmatic | legacy | `T2 docs/Display subtotal inside the Checkout button (1) 35aa41d3e45b80d5b7fcd17287a33477.md` |
| Display subtotal plus the fixed shipping amount - Slide Cart | any | styling, shipping, checkout, programmatic | legacy | `T2 docs/Display subtotal plus the fixed shipping amount -  35aa41d3e45b80878b35db58bcf7c28c.md` |
| Display the options selected on slide cart when these are hidden using the _ (underscore sign) | any | styling, checkout, programmatic | legacy | `T2 docs/Display the options selected on slide cart when th 35aa41d3e45b80fd8902fe69f03310cc.md` |
| Displaying SKU value on cart items | any | cart-items, styling, programmatic | legacy | `T2 docs/Displaying SKU value on cart items (1) 35aa41d3e45b801c8b18ec3bab96f81c.md` |
| DOM Manipulation | any | cart-items, upsell | legacy | `T2 docs/DOM Manipulation (1) 35aa41d3e45b80c88e5bf1847dc72f7a.md` |
| Donations module on Slide Cart | any | checkout-button, styling | legacy | `T2 docs/Donations module on Slide Cart (1) 35aa41d3e45b805aa082c6b78ab38a8c.md` |
| Duplicated footer with class 'new-footer' not sticky | any | styling, checkout, programmatic-open, programmatic | legacy | `T2 docs/Duplicated footer with class 'new-footer' not stic 35aa41d3e45b80dd9f08dd570fe6dfd2.md` |
| Enable checkout button at all times regardless of T&C | any | checkout-button, terms-checkbox, programmatic-open, programmatic | legacy | `T2 docs/Enable checkout button at all times regardless of  35aa41d3e45b80f6ae98d3a1cf4752c8.md` |
| Ensure a Product is Always Added to Cart | any | programmatic | legacy | `T2 docs/Ensure a Product is Always Added to Cart (1) 35aa41d3e45b80a98ba6db6db0be44b6.md` |
| Exclude Shipping Protection from Cart Count | any | cart-icon, cart-count, shipping-protection, programmatic | legacy | `T2 docs/Exclude Shipping Protection from Cart Count (1) 35aa41d3e45b80daa07bfbdcd7333107.md` |
| Fetch Cart Object | any | untagged | legacy | `T2 docs/Fetch Cart Object (1) 35aa41d3e45b80f3a581e61c1623f63b.md` |
| Fix cart page redirection (Impulse theme) | Impulse | cart-redirect, atc-button, theme-js, programmatic-open, programmatic | legacy | `T2 docs/Fix cart page redirection (Impulse theme) (1) 35aa41d3e45b809b9bdbe2e4c019c285.md` |
| Fix cart page redirection (Impulse theme) | Impulse | cart-redirect, atc-button, theme-js | legacy | `T2 docs/Fix cart page redirection (Impulse theme) (1) 35aa41d3e45b80eda23bd3fc6f0bebd3.md` |
| Fix Cart Page redirection in Broadcast theme | Broadcast | cart-redirect, atc-button, theme-js, programmatic-open, programmatic | legacy | `T2 docs/Fix Cart Page redirection in Broadcast theme (1) 35aa41d3e45b80949941d516efb34fb1.md` |
| Fix discount tag format | any | discount-code, programmatic | legacy | `T2 docs/Fix discount tag format (1) 35aa41d3e45b80849a5bcc6fe0f91221.md` |
| Fix PageFly Redirection to Cart Page | any | cart-redirect, atc-button, checkout, pagefly, third-party-page-builder, programmatic | legacy | `T2 docs/Fix PageFly Redirection to Cart Page (1) 35aa41d3e45b80eb9e01fd3a65250678.md` |
| Fix SlideCart layout glitching | any | styling, ui-bug | legacy | `T2 docs/Fix SlideCart layout glitching (1) 35aa41d3e45b80058bebeeca98c0f9b7.md` |
| Fix stretched quantity selector | any | styling, upsell | legacy | `T2 docs/Fix stretched quantity selector (1) 35aa41d3e45b80e597ccc64c7583c7f7.md` |
| Fixing APD tabs on mobile | any | styling, mobile-only | legacy | `T2 docs/Fixing APD tabs on mobile (1) 35aa41d3e45b80db95a3e98de90a750b.md` |
| Fixing Compare-at Price for Subscription Products | any | subscriptions | legacy | `T2 docs/Fixing Compare-at Price for Subscription Products  35aa41d3e45b808b9345d07d53fc3af9.md` |
| Fixing SuperBar box on mobile – products with more than one variant selector | any | styling, mobile-only | legacy | `T2 docs/Fixing SuperBar box on mobile – products with more 35aa41d3e45b800793c6f50af9c6d592.md` |
| Fixing table formatting on mobile | any | styling, mobile-only | legacy | `T2 docs/Fixing table formatting on mobile (1) 35aa41d3e45b80628672d24b5590c925.md` |
| Format Money function (T2) | any | multi-currency | legacy | `T2 docs/Format Money function (T2) (1) 35aa41d3e45b80b38267cf8605748060.md` |
| Free Shipping with zero threshold | any | rewards, multi-currency, programmatic | legacy | `T2 docs/Free Shipping with zero threshold (1) 35aa41d3e45b80fdb348cf5cebf79498.md` |
| Get complete information about a product | any | custom-app, programmatic | legacy | `T2 docs/Get complete information about a product (1) 35aa41d3e45b804eaa25ccb407f2abd1.md` |
| Global function to update SLIDECART_STATE | any | rewards, announcement, multi-language, programmatic | legacy | `T2 docs/Global function to update SLIDECART_STATE (1) 35aa41d3e45b8038980ec633115df56e.md` |
| HelpHQ - Automatically scroll to the article section (scroll into view) | any | untagged | legacy | `T2 docs/HelpHQ - Automatically scroll to the article secti 35aa41d3e45b80138686ed3a810520cd.md` |
| Hide cart drawer and fix Cart Page redirection (Minimog Theme) | Minimog | cart-redirect, atc-button, programmatic, legacy-theme | legacy | `T2 docs/Hide cart drawer and fix Cart Page redirection (Mi 35aa41d3e45b80f59fcbd0fd21176fb2.md` |
| Hide Decimal Places in Prices if Possible | any | upsell, programmatic | legacy | `T2 docs/Hide Decimal Places in Prices if Possible (1) 35aa41d3e45b806fbfb4e9615d2d4e31.md` |
| Hide items properties on Slide Cart | any | cart-items, multi-language, programmatic | legacy | `T2 docs/Hide items properties on Slide Cart (1) 35aa41d3e45b807bad7bd85dffc9189a.md` |
| Hide product in Slide Cart using a custom product tag | any | programmatic | legacy | `T2 docs/Hide product in Slide Cart using a custom product  35aa41d3e45b800f80d2ca873392b127.md` |
| Hide Quantity Selector and remove button for Certain Product Types/Tags | any | cart-items | legacy | `T2 docs/Hide Quantity Selector and remove button for Certa 35aa41d3e45b80569b82e3d3cf07240d.md` |
| Hide Quantity Selector for Certain Product Types (Gifts, Hidden products, etc) | any | free-gift, programmatic | legacy | `T2 docs/Hide Quantity Selector for Certain Product Types ( 35aa41d3e45b8047b83af5c484f3a0be.md` |
| Hide Quantity Selector for Free Gifts with zero price | any | free-gift, programmatic | legacy | `T2 docs/Hide Quantity Selector for Free Gifts with zero pr 35aa41d3e45b801089eac625db8cd025.md` |
| Hide Quantity Selectors For Free Gifts In Cart | any | upsell, free-gift | legacy | `T2 docs/Hide Quantity Selectors For Free Gifts In Cart (1) 35aa41d3e45b8026987efc69a0ad0d58.md` |
| Hide scroll bar and show it only when scrolling | any | styling | legacy | `T2 docs/Hide scroll bar and show it only when scrolling (1 35aa41d3e45b8043868dd5fbbf82f1dc.md` |
| Hide shipping product from showing in collection page (And search bar) | any | shipping-protection | legacy | `T2 docs/Hide shipping product from showing in collection p 35aa41d3e45b800b88aeef6c816482e0.md` |
| Hide Shipping Protection Product And Fix Cart Count | any | cart-count, upsell, shipping-protection | legacy | `T2 docs/Hide Shipping Protection Product And Fix Cart Coun 35aa41d3e45b80f59eb0c97895b0b8a7.md` |
| Hide Shipping Protection Widget For Certain Countries in the AMP Upsell Cart | any | upsell, shipping-protection | legacy | `T2 docs/Hide Shipping Protection Widget For Certain Countr 35aa41d3e45b804aa7b4dd0890f37d7c.md` |
| Hide specific selling plans in the subscription option in the AMP cart | any | upsell, subscriptions | legacy | `T2 docs/Hide specific selling plans in the subscription op 35aa41d3e45b8037bf60ed5cb8d8160f.md` |
| Hide the product on Slide Cart and don’t apply its price to the Subtotal value | any | styling, programmatic | legacy | `T2 docs/Hide the product on Slide Cart and don’t apply its 35aa41d3e45b807598dfc76307eb7949.md` |
| Hide the Rewards Progress Bar when Tier is Reached | any | styling, rewards, programmatic | legacy | `T2 docs/Hide the Rewards Progress Bar when Tier is Reached 35aa41d3e45b800eb9efe0b6a0708a78.md` |
| Hide the subscription option with an asterisk (*) | any | subscriptions | legacy | `T2 docs/Hide the subscription option with an asterisk ( )  35aa41d3e45b8044a3bbc1d73c32dc71.md` |
| Hide tier rewards bar outside of US | any | rewards, custom-app, programmatic | legacy | `T2 docs/Hide tier rewards bar outside of US (1) 35aa41d3e45b8006bcbed5ed6947dffb.md` |
| Hide Tiered Rewards Based On Customer Tags | any | upsell, rewards, custom-app | legacy | `T2 docs/Hide Tiered Rewards Based On Customer Tags (1) 35aa41d3e45b8051b1ccd4f654aa9c83.md` |
| Hide/Disable Slide Cart on a specific country | any | rewards, programmatic | legacy | `T2 docs/Hide Disable Slide Cart on a specific country (1) 35aa41d3e45b8077be4ecf3e79c223c5.md` |
| Hide/Disable Slide Cart on a specific product page | any | theme-js, programmatic | legacy | `T2 docs/Hide Disable Slide Cart on a specific product page 35aa41d3e45b807e8dbac79130f4a29e.md` |
| Hide/Show Announcement bar whether cart is empty or not | any | announcement | legacy | `T2 docs/Hide Show Announcement bar whether cart is empty o 35aa41d3e45b8061bceeec23f0c6714d.md` |
| Hide/Show Tier Rewards and Checkout footer whether cart is empty or not | any | checkout-button, empty-cart, rewards | legacy | `T2 docs/Hide Show Tier Rewards and Checkout footer whether 35aa41d3e45b802eb81aead6a4905e33.md` |
| Highlight Reward Tier Label Upon Reaching the Threshold | any | styling, rewards, programmatic | legacy | `T2 docs/Highlight Reward Tier Label Upon Reaching the Thre 35aa41d3e45b80c1914cef86c09016a3.md` |
| Include product vendor in the upsells section | any | styling, upsell, programmatic | legacy | `T2 docs/Include product vendor in the upsells section (1) 35aa41d3e45b80489a46e831ab131b4f.md` |
| Including APD as a Block in the “Featured Product Section” | any | untagged | legacy | `T2 docs/Including APD as a Block in the “Featured Product  35aa41d3e45b802da626c22a7c9e5d21.md` |
| Insert product page (embedded) block | any | styling, upsell | legacy | `T2 docs/Insert product page (embedded) block (1) 35aa41d3e45b8057a082c54e4aca26fe.md` |
| Insert volume discount block | any | styling, upsell | legacy | `T2 docs/Insert volume discount block (1) 35aa41d3e45b80659b37d6851d415c30.md` |
| Installation guide to add Product page upsells block to themes that are not 2.0 | Debut | upsell, legacy-theme | legacy | `T2 docs/Installation guide to add Product page upsells blo 35aa41d3e45b8051ace7fea87b3815ea.md` |
| Installing in Sophie Theme | any | programmatic-open, programmatic | legacy | `T2 docs/Installing in Sophie Theme (1) 35aa41d3e45b80948704f3b9b1c0e614.md` |
| Integrate Prestige Theme's Sticky Add-to-cart Button With Slide Cart | Prestige | atc-button, programmatic-open, programmatic | legacy | `T2 docs/Integrate Prestige Theme's Sticky Add-to-cart Butt 35aa41d3e45b802f9cc2ef76c5c092a5.md` |
| Integrate Shipping Protection apps with Slide Cart | any | checkout-button, shipping-protection, third-party-app, programmatic | legacy | `T2 docs/Integrate Shipping Protection apps with Slide Cart 35aa41d3e45b8062a914f9f157167b5e.md` |
| Integrate SlideCart with Gokwik Checkout | any | checkout, programmatic | legacy | `T2 docs/Integrate SlideCart with Gokwik Checkout (1) 35aa41d3e45b80de823bd8ab369aaa10.md` |
| Integrate with Zepto Product Personalizer | any | atc-button, programmatic-open, programmatic | legacy | `T2 docs/Integrate with Zepto Product Personalizer (1) 35aa41d3e45b8000aa7ce7d9a929d5e8.md` |
| Integrate with Zepto Product Personalizer | any | atc-button, upsell | legacy | `T2 docs/Integrate with Zepto Product Personalizer (1) 35aa41d3e45b80dd858fd82e45704c43.md` |
| Integrating with King Product Options | any | cart-redirect, atc-button, programmatic-open, programmatic | legacy | `T2 docs/Integrating with King Product Options (1) 35aa41d3e45b80509262c950f4f3f0b3.md` |
| Integrating with Live Product Options | any | checkout, programmatic | legacy | `T2 docs/Integrating with Live Product Options (1) 35aa41d3e45b80e49f29f2404892bcdd.md` |
| Integrating with Teeinblue Customization App | any | programmatic-open, programmatic | legacy | `T2 docs/Integrating with Teeinblue Customization App (1) 35aa41d3e45b8095921fde5af38617ac.md` |
| Integrating with VO Product Options | any | cart-button, programmatic-open, programmatic | legacy | `T2 docs/Integrating with VO Product Options (1) 35aa41d3e45b8081bef9d62595a69e24.md` |
| Integration with Bundler app | any | styling, svg-icon, upsell | legacy | `T2 docs/Integration with Bundler app (1) 35aa41d3e45b808fb777e3ead8a308e4.md` |
| Integration with Easy Gift | any | untagged | legacy | `T2 docs/Integration with Easy Gift (1) 35aa41d3e45b80a791a0d824c129fca8.md` |
| Integration with Qikify Upsell Popup Cross Sell | any | upsell, programmatic | legacy | `T2 docs/Integration with Qikify Upsell Popup Cross Sell (1 35aa41d3e45b808caedcf1c494abcfcb.md` |
| Integration with Vimotia Videos app. | any | atc-button, programmatic-open, programmatic | legacy | `T2 docs/Integration with Vimotia Videos app (1) 35aa41d3e45b80f3ae73f2022aa08280.md` |
| Integration with Yampi Checkout | any | checkout, custom-app | legacy | `T2 docs/Integration with Yampi Checkout (1) 35aa41d3e45b80d7b659dbb1d4ace09c.md` |
| Limit a product to not be less than X quantity | any | programmatic | legacy | `T2 docs/Limit a product to not be less than X quantity (1) 35aa41d3e45b80388723f11f59e55f0e.md` |
| Limit a product to not be more than X quantity | any | programmatic | legacy | `T2 docs/Limit a product to not be more than X quantity (1) 35aa41d3e45b80f0bd71de82a56e291d.md` |
| Maintain the Aspect Ratio of Product Images | any | styling | legacy | `T2 docs/Maintain the Aspect Ratio of Product Images (1) 35aa41d3e45b80baa73ac60652a43da5.md` |
| Make Discount Box Sticky | any | styling, discount-code, programmatic | legacy | `T2 docs/Make Discount Box Sticky (1) 35aa41d3e45b80f99d1cfa837dd6eb2b.md` |
| Make empty cart display look like Slide Cart’s | any | empty-cart, styling, svg-icon, upsell, rewards, announcement | legacy | `T2 docs/Make empty cart display look like Slide Cart’s (1) 35aa41d3e45b80da8370da84684b645e.md` |
| Make the checkout footer sticky in Upsells cart | any | styling, upsell, checkout | legacy | `T2 docs/Make the checkout footer sticky in Upsells cart (1 35aa41d3e45b802b86d5d4e7d1cf111f.md` |
| Make the next/previous arrows in the upsell carousel more visible. | any | styling, upsell | legacy | `T2 docs/Make the next previous arrows in the upsell carous 35aa41d3e45b800e8fd7f3dbd2291360.md` |
| Make the Upsell image on the Product Page redirect to the product page | any | upsell, theme-js, custom-app | legacy | `T2 docs/Make the Upsell image on the Product Page redirect 35aa41d3e45b80e0bf69e15edcb93cd5.md` |
| Manually translating announcement | any | announcement, multi-language, custom-app | legacy | `T2 docs/Manually translating announcement (1) 35aa41d3e45b8011b927e2cda668e68e.md` |
| Metaobject translations for Rewards and announcements | any | rewards, announcement, multi-language | legacy | `T2 docs/Metaobject translations for Rewards and announceme 35aa41d3e45b809d9d9df2d41f6afda2.md` |
| Navidium Shipping Protection Integration | any | checkout-button, styling, shipping-protection | legacy | `T2 docs/Navidium Shipping Protection Integration (1) 35aa41d3e45b80739935ef845497778c.md` |
| Navidium Shipping Protection Integtation | any | upsell, shipping-protection, checkout | legacy | `T2 docs/Navidium Shipping Protection Integtation (1) 35aa41d3e45b80748247eb7e85d60100.md` |
| Not count gift as part of a item based reward tier | any | free-gift, rewards, custom-app, programmatic | legacy | `T2 docs/Not count gift as part of a item based reward tier 35aa41d3e45b80e58207c44e134e5a7c.md` |
| Offer Different Gift Rewards Based On Cart Value | any | free-gift, rewards, programmatic | legacy | `T2 docs/Offer Different Gift Rewards Based On Cart Value ( 35aa41d3e45b805992facbe68e45cec2.md` |
| Open AMP Cart after hovering over the cart icon from the header | any | cart-icon, hover | legacy | `T2 docs/Open AMP Cart after hovering over the cart icon fr 35aa41d3e45b80439f9ed94055ca5875.md` |
| Open Slide Cart instead of open the cart page when the customer clicks on the "/cart" page direct link | any | cart-redirect, theme-js, custom-app, programmatic-open, programmatic | legacy | `T2 docs/Open Slide Cart instead of open the cart page when 35aa41d3e45b806990b9e0c2e510513b.md` |
| Open Slide Cart on custom ATC buttons from a Subscription/Questionnaire Form | any | cart-redirect, atc-button, mobile-only, subscriptions, programmatic-open, programmatic | legacy | `T2 docs/Open Slide Cart on custom ATC buttons from a Subsc 35aa41d3e45b806ab770f2700ebd64a3.md` |
| Override scrollbar styling from SlideCart | any | styling, programmatic | legacy | `T2 docs/Override scrollbar styling from SlideCart (1) 35aa41d3e45b803ca977f4dda98cb760.md` |
| Payment Icons below checkout btn | any | styling, svg-icon, checkout | legacy | `T2 docs/Payment Icons below checkout btn (1) 35aa41d3e45b80a2bf01dba5e8fd381a.md` |
| Place widget above checkout button | any | checkout-button, styling, custom-app | legacy | `T2 docs/Place widget above checkout button (1) 35aa41d3e45b8024bcd2e45cf6b67b54.md` |
| Position the countdown timer above the checkout button. | any | checkout-button, programmatic-open, programmatic | legacy | `T2 docs/Position the countdown timer above the checkout bu 35aa41d3e45b80e1a1fcf13bb1389720.md` |
| Prevent SlideCart from opening when ATC button is clicked on specific Product Pages | any | atc-button, theme-js, programmatic | legacy | `T2 docs/Prevent SlideCart from opening when ATC button is  35aa41d3e45b800783aaf49a58fcee1a.md` |
| Pursuit Theme Cart Icon Redirecting to Cart Page | Pursuit | cart-redirect, cart-icon, theme-js, programmatic-open, programmatic | legacy | `T2 docs/Pursuit Theme Cart Icon Redirecting to Cart Page ( 35aa41d3e45b802581a8fcc55dc421c3.md` |
| Quantity Selector Hidden | any | styling | legacy | `T2 docs/Quantity Selector Hidden (1) 35aa41d3e45b80c6b213d525cc778f68.md` |
| Recharge subscription bundle integration with Slidecart. Avoid cart redirect | any | cart-redirect, atc-button, subscriptions, recharge, programmatic-open, programmatic | legacy | `T2 docs/Recharge subscription bundle integration with Slid 35aa41d3e45b8062acd1ebba34be60af.md` |
| Reduce the size of express checkout buttons on mobile view | any | checkout-button, styling, mobile-only | legacy | `T2 docs/Reduce the size of express checkout buttons on mob 35aa41d3e45b80beae86fc44aadfe5db.md` |
| Remove hyperlink from titles and images in SlideCart | any | upsell, programmatic | legacy | `T2 docs/Remove hyperlink from titles and images in SlideCa 35aa41d3e45b80a4a073c55f4524bc6e.md` |
| Remove hyperlink from titles in AMP Upsells Cart | any | upsell | legacy | `T2 docs/Remove hyperlink from titles in AMP Upsells Cart ( 35aa41d3e45b805195f6f9335c315c37.md` |
| Remove variant line from line item | any | custom-app | legacy | `T2 docs/Remove variant line from line item (1) 35aa41d3e45b809b8db2c99805798026.md` |
| Replace the native Countdown with one that doesn’t resets | any | styling, announcement, custom-app | legacy | `T2 docs/Replace the native Countdown with one that doesn’t 35aa41d3e45b80e78a24e0ce0800cc42.md` |
| Replicate Upcart Look | any | styling, rewards, announcement, checkout | legacy | `T2 docs/Replicate Upcart Look (1) 35aa41d3e45b808daa16c63f30d64ded.md` |
| Reset the countdown timers once they reach 00:00 | any | announcement, programmatic | legacy | `T2 docs/Reset the countdown timers once they reach 00 00 ( 35aa41d3e45b8053b6b8db4eff563f23.md` |
| Route Protection App Integration | any | checkout | legacy | `T2 docs/Route Protection App Integration (1) 35aa41d3e45b80f8b00cdedbe840b788.md` |
| Save Space on Mobile | any | styling, mobile-only, upsell, rewards | legacy | `T2 docs/Save Space on Mobile (1) 35aa41d3e45b80648591fc3c998e1dc8.md` |
| Savings tag on Slide Cart items (SAVE $X or SAVE X%) | any | cart-items, styling, discount-code | legacy | `T2 docs/Savings tag on Slide Cart items (SAVE $X or SAVE X 35aa41d3e45b80319fb0ccb16ad562e8.md` |
| Savings tag on Slide Cart items (SAVE $X or SAVE X%) (Original) | any | cart-items, discount-code | legacy | `T2 docs/Savings tag on Slide Cart items (SAVE $X or SAVE X 35aa41d3e45b80f49f39ea5b17221521.md` |
| Selleasy Bundle Discount Not Showing In Cart / Cart Not Opening | any | atc-button, svg-icon, upsell, programmatic-open, programmatic | legacy | `T2 docs/Selleasy Bundle Discount Not Showing In Cart Cart  35aa41d3e45b804f9ef4e1f38c905371.md` |
| SEOAnt Sticky Add To Cart Integration | any | atc-button, programmatic-open, programmatic | legacy | `T2 docs/SEOAnt Sticky Add To Cart Integration (1) 35aa41d3e45b802ab74cdff536228494.md` |
| Set Custom Free Shipping Reward Thresholds based on location | any | upsell, shipping, rewards, multi-currency | legacy | `T2 docs/Set Custom Free Shipping Reward Thresholds based o 35aa41d3e45b809099dce27b58040d26.md` |
| Set minimum cart quantity and amount to SlideCart | any | checkout-button, programmatic | legacy | `T2 docs/Set minimum cart quantity and amount to SlideCart  35aa41d3e45b80038681e4640edfc5d9.md` |
| Setup in Empire Theme | Empire | cart-count, programmatic-open, programmatic | legacy | `T2 docs/Setup in Empire Theme (1) 35aa41d3e45b8001b813cbb6b80b0929.md` |
| Setup in Porto Theme | any | styling | legacy | `T2 docs/Setup in Porto Theme (1) 35aa41d3e45b80338fb3e39b191cba75.md` |
| Shipping Protection Not Working | any | shipping-protection | legacy | `T2 docs/Shipping Protection Not Working (1) 35aa41d3e45b8021be62c8be5d3933bc.md` |
| Shiprocket Checkout Integration | any | checkout-button | legacy | `T2 docs/Shiprocket Checkout Integration (1) 35aa41d3e45b8060a7cef5353c436657.md` |
| Shiprocket Checkout Integration | any | checkout-button, styling | legacy | `T2 docs/Shiprocket Checkout Integration (1) 35aa41d3e45b80b9b708ddfb6b7ca83e.md` |
| Show a Pre-Order Tag in the Upsell Cart | any | styling, upsell | legacy | `T2 docs/Show a Pre-Order Tag in the Upsell Cart (1) 35aa41d3e45b809ba318d38bc6bda3d2.md` |
| Show cart icon bubble on first ATC for Expanse theme. | Expanse | atc-button, cart-icon, programmatic | legacy | `T2 docs/Show cart icon bubble on first ATC for Expanse the 35aa41d3e45b80e88efcf66e15f340ce.md` |
| Show Compare-at Price For Gift Priced At $0 | any | free-gift, discount-code, rewards, programmatic | legacy | `T2 docs/Show Compare-at Price For Gift Priced At $0 (1) 35aa41d3e45b80d6a5fce7546ce72f80.md` |
| Show custom Design File property from 3D design tool app | any | untagged | legacy | `T2 docs/Show custom Design File property from 3D design to 35aa41d3e45b8083b305e0770b5bae88.md` |
| Show local currency in SlideCart | any | multi-currency, programmatic | legacy | `T2 docs/Show local currency in SlideCart (1) 35aa41d3e45b801493a1df9940ad812a.md` |
| Show SKU number of upsells (Or related info) | any | styling, upsell, programmatic | legacy | `T2 docs/Show SKU number of upsells (Or related info) (1) 35aa41d3e45b808d8008de626ee8e74f.md` |
| Show the total compared price + total amount discounted from a discount code | any | discount-code, programmatic | legacy | `T2 docs/Show the total compared price + total amount disco 35aa41d3e45b80bea153e8305a0e7c44.md` |
| Show Upsells on Empty Cart | any | empty-cart, upsell | legacy | `T2 docs/Show Upsells on Empty Cart (1) 35aa41d3e45b8027aa12f0517746089f.md` |
| Showing a bit or hint of the next item in upsell carousel | any | styling, upsell | legacy | `T2 docs/Showing a bit or hint of the next item in upsell c 35aa41d3e45b80518d45e0e2db8cb052.md` |
| Showing APD as a Section Outside of Product Pages | any | custom-app | legacy | `T2 docs/Showing APD as a Section Outside of Product Pages  35aa41d3e45b80319ff1e3e617019fb6.md` |
| Showing compare at a price with Bold Custom Pricing app | any | custom-app, programmatic | legacy | `T2 docs/Showing compare at a price with Bold Custom Pricin 35aa41d3e45b80739c9bee2ce60a5e01.md` |
| Showing compare-at price in Slide Cart | any | third-party-app, programmatic | legacy | `T2 docs/Showing compare-at price in Slide Cart (1) 35aa41d3e45b8033aba5d5a9141bc899.md` |
| Showing the Compare-At Price Even After Discounts | any | programmatic | legacy | `T2 docs/Showing the Compare-At Price Even After Discounts  35aa41d3e45b80b291e7e4e577222edf.md` |
| Slide Cart - Click twice to go to the checkout page on iPhone. | any | styling, checkout | legacy | `T2 docs/Slide Cart - Click twice to go to the checkout pag 35aa41d3e45b80e6a0fede930a6a6144.md` |
| Slide Cart - Show the Fast Bundle discount as a discount tag | any | upsell, discount-code, programmatic-open, programmatic | legacy | `T2 docs/Slide Cart - Show the Fast Bundle discount as a di 35aa41d3e45b804fb0c8df1aafc36c15.md` |
| Slide cart and multicurrency not working with Shopify Markets | any | multi-currency | legacy | `T2 docs/Slide cart and multicurrency not working with Shop 35aa41d3e45b802192f6efab7190a503.md` |
| Slide Cart API | any | untagged | legacy | `T2 docs/Slide Cart API 35aa41d3e45b80cba4d7debfb2e01394.md` |
| Slide Cart Checkout page doesn't redirect to the Recharge checkout page | any | checkout-button, subscriptions, recharge | legacy | `T2 docs/Slide Cart Checkout page doesn't redirect to the R 35aa41d3e45b80f7aa3fd8a6d430a7dc.md` |
| Slide Cart disabled the "Add to Cart" button behavior when clicked. | any | atc-button, styling, programmatic | legacy | `T2 docs/Slide Cart disabled the Add to Cart button behavio 35aa41d3e45b8096b2e1ca17ba2d0b73.md` |
| Slide Cart hide section IF a product is on the cart | any | rewards, programmatic | legacy | `T2 docs/Slide Cart hide section IF a product is on the car 35aa41d3e45b80f09140e6f4036a5f36.md` |
| Slide Cart is not showing the right products added when you click on the "Go back" browser button | any | checkout, third-party-app, theme-js | legacy | `T2 docs/Slide Cart is not showing the right products added 35aa41d3e45b80099971d2f16d2f1650.md` |
| Slide Cart not loading when ATC"Quick Add" button from home and collections pages is clicked | any | cart-redirect, atc-button, theme-js, programmatic-open, programmatic | legacy | `T2 docs/Slide Cart not loading when ATC Quick Add button f 35aa41d3e45b80b586e1dd4301272c2b.md` |
| Slide Cart product links not working with multi-language Shopify markets | any | upsell, multi-language, custom-app, programmatic | legacy | `T2 docs/Slide Cart product links not working with multi-la 35aa41d3e45b80ed8b0df4dd2f490b95.md` |
| Slide Cart Route Protection plan | any | checkout-button, analytics, custom-app, programmatic | legacy | `T2 docs/Slide Cart Route Protection plan (1) 35aa41d3e45b80ef9df5c2b1ffe4814b.md` |
| Sort products inside Slide Cart | any | programmatic | legacy | `T2 docs/Sort products inside Slide Cart (1) 35aa41d3e45b80e48a11f35fa23276ee.md` |
| Stacking the ATC button below the description in upsell carousel | any | atc-button, styling, upsell | legacy | `T2 docs/Stacking the ATC button below the description in u 35aa41d3e45b807e8e90f7ea037feae2.md` |
| Static compare-at-price in cart items with total discount in footer | any | cart-items, styling, multi-currency, programmatic | legacy | `T2 docs/Static compare-at-price in cart items with total d 35aa41d3e45b8042a1e2c66c8bda6614.md` |
| Sticky Rewards Tier | any | styling, rewards, programmatic | legacy | `T2 docs/Sticky Rewards Tier (1) 35aa41d3e45b803d9669f0378df0c045.md` |
| Store header overlapping with Slide Cart on iOS devices | any | styling | legacy | `T2 docs/Store header overlapping with Slide Cart on iOS de 35aa41d3e45b80629b92f18bec213563.md` |
| Styling the Shipping Protection Switch Toggle | any | styling, shipping-protection | legacy | `T2 docs/Styling the Shipping Protection Switch Toggle (1) 35aa41d3e45b80838cebe45f0d3e375d.md` |
| Sync counter header using only JavaScript | any | cart-count, programmatic | legacy | `T2 docs/Sync counter header using only JavaScript (1) 35aa41d3e45b802e9936e927e74c54c6.md` |
| Target a Date for the Timer Countdown | any | announcement, programmatic | legacy | `T2 docs/Target a Date for the Timer Countdown (1) 35aa41d3e45b80fc8682d3f708605f31.md` |
| The app is not displayed properly | any | styling | legacy | `T2 docs/The app is not displayed properly (1) 35aa41d3e45b80b38998fb2d309baee4.md` |
| Total price with line-through when having discount applied | any | programmatic | legacy | `T2 docs/Total price with line-through when having discount 35aa41d3e45b80c3bf9ffb5178c08623.md` |
| Translate Announcements | any | upsell, rewards, announcement, multi-language | legacy | `T2 docs/Translate Announcements (1) 35aa41d3e45b8046af1bf42552339bb0.md` |
| Translate Announcements Module | any | announcement, multi-language | legacy | `T2 docs/Translate Announcements Module (1) 35aa41d3e45b805ebda7ee07cf20e881.md` |
| Translate apps not working on Slide Cart - Weglot/Langify | any | upsell, checkout, weglot, theme-js, multi-language, programmatic-open, programmatic | legacy | `T2 docs/Translate apps not working on Slide Cart - Weglot  35aa41d3e45b8002b8f2e4ddc04e4e3f.md` |
| Translate Reward Tier Labels | any | cart-count, upsell, rewards, multi-language | legacy | `T2 docs/Translate Reward Tier Labels (1) 35aa41d3e45b800d8f7ce1410ac65418.md` |
| Translate Reward Tier Labels | any | cart-count, rewards, multi-language, programmatic | legacy | `T2 docs/Translate Reward Tier Labels (1) 35aa41d3e45b80bb857bf3cee66371f2.md` |
| Translate rewards module in the Upsells cart | any | upsell, rewards, multi-language, custom-app | legacy | `T2 docs/Translate rewards module in the Upsells cart (1) 35aa41d3e45b80208f7de4d3a8fb156e.md` |
| Translate rewards, announcements and other custom elements | any | cart-button, shipping-protection, rewards, announcement, multi-language, multi-currency, custom-app, programmatic | legacy | `T2 docs/Translate rewards, announcements and other custom  35aa41d3e45b80ba971afd04ffe5901e.md` |
| Translate the "ADD" button and "Free" wording in the free gift section | any | styling, upsell, free-gift, multi-language, programmatic | legacy | `T2 docs/Translate the ADD button and Free wording in the f 35aa41d3e45b80f1a4a3d70ee09c6c61.md` |
| Translate the Subscription Options label and Select elemnts | any | subscriptions, programmatic | legacy | `T2 docs/Translate the Subscription Options label and Selec 35aa41d3e45b8052a042efad0a607c18.md` |
| Translate tiered rewards and adjust thresholds based on other currencies #2 | any | rewards, multi-language, multi-currency, programmatic | legacy | `T2 docs/Translate tiered rewards and adjust thresholds bas 35aa41d3e45b80daaf2cde6d6aec3a99.md` |
| Trim variant options for target cart items | any | cart-items, multi-currency | legacy | `T2 docs/Trim variant options for target cart items (1) 35aa41d3e45b80209ed4d916fcb057c9.md` |
| Untitled | any | untagged | legacy | `T2 docs/Untitled 35aa41d3e45b808ea6a6e1ce3635a8b2.md` |
| Update cart count with the Upsells cart | any | cart-count, upsell | legacy | `T2 docs/Update cart count with the Upsells cart (1) 35aa41d3e45b80c18da1d8567bd6f6ae.md` |
| Update Cart Dot when updating items from cart | any | cart-count, styling, programmatic | legacy | `T2 docs/Update Cart Dot when updating items from cart (1) 35aa41d3e45b801a8436de18d0332d79.md` |
| Update rewards module based on currencies. | any | shipping, rewards, multi-currency, programmatic | legacy | `T2 docs/Update rewards module based on currencies (1) 35aa41d3e45b80d2b8eed4c7d2bd159d.md` |
| Update shipping protection rate based on customer currency | any | shipping-protection, shipping, multi-currency, programmatic | legacy | `T2 docs/Update shipping protection rate based on customer  35aa41d3e45b8018a6d4fe4c766b9340.md` |
| Update Slide Cart based on Element Mutation | any | atc-button, announcement, programmatic-open, programmatic | legacy | `T2 docs/Update Slide Cart based on Element Mutation (1) 35aa41d3e45b807ea7b9d8276d38fa14.md` |
| Update tier rewards threshold whether the shipping protection product is added to the cart or not | any | free-gift, shipping-protection, rewards, multi-currency, programmatic-open, programmatic | legacy | `T2 docs/Update tier rewards threshold whether the shipping 35aa41d3e45b80f7b798e36beaf05dbb.md` |
| Updating product items language inside the drawer | any | checkout-button, multi-language, programmatic | legacy | `T2 docs/Updating product items language inside the drawer  35aa41d3e45b808d9483edca78080cb7.md` |
| Updating Weglot translation - Slidecart | any | announcement, weglot, multi-language | legacy | `T2 docs/Updating Weglot translation - Slidecart (1) 35aa41d3e45b80d2806ce2f91433204f.md` |
| Upsell Spacing / Alignment Issues | any | styling, upsell | legacy | `T2 docs/Upsell Spacing Alignment Issues (1) 35aa41d3e45b80c4ac75fad525dd5a6e.md` |
| Volume Boost by HulkApps Integration | any | checkout-button, styling, programmatic | legacy | `T2 docs/Volume Boost by HulkApps Integration (1) 35aa41d3e45b80cbb97bdb27b7dbdd42.md` |
| Window blocks scrolling after closing the slide cart on mobile devices | any | atc-button, cart-icon, mobile-only, third-party-app, programmatic | legacy | `T2 docs/Window blocks scrolling after closing the slide ca 35aa41d3e45b80fbbdb3f7ea85e4a715.md` |
| Wrapping 'add' button for upsell module - theme: Turbo 4.0.2 | Turbo | styling, upsell, multi-language | legacy | `T2 docs/Wrapping 'add' button for upsell module - theme Tu 35aa41d3e45b80a0b5e1d6b25b251655.md` |
| YMQ Product Options Integration | any | rewards, custom-app, programmatic | legacy | `T2 docs/YMQ Product Options Integration (1) 35aa41d3e45b8031bbe3c9e9687c80ec.md` |
 
 
### Bundles — full archive (auto-catalogued)
 
| Title | Themes | Tags | Status | File |
|---|---|---|---|---|
| Fix cart count when adding products created with Shopify Bundles app (And rewards based on item count) | any | cart-count, shipping-protection, rewards, programmatic | legacy | `T2 docs/Fix cart count when adding products created with S 35aa41d3e45b80af9ca0ef6040d1eb43.md` |
 
---
 
## Tag glossary
 
Use existing tags wherever possible. Avoid synonyms — pick one, stick with it. If you need a new tag, add it to this glossary.
 
| Tag | Meaning |
|---|---|
| `cart-redirect` | Clicking the cart icon or ATC sends customer to /cart instead of opening the drawer. |
| `atc-button` | Issues specific to Add-To-Cart button behavior. |
| `cart-icon` | Customizing or fixing the theme's cart icon (visibility, styling, behavior). |
| `cart-trigger` | Custom triggers for opening the drawer (hover, button, URL param). |
| `cart-count` | Cart count badge/bubble syncing or display. |
| `cart-button` | Custom buttons inside the drawer (continue shopping, clear cart, etc). |
| `cart-items` | Display/styling of line items in the drawer. |
| `empty-cart` | Empty-cart screen styling and content. |
| `checkout-button` | Checkout CTA styling, icons, or behavior. |
| `checkout` | Checkout flow issues (Recharge, custom redirects, post-cart behavior). |
| `discount-code` | Discount/promo code application. |
| `shipping-protection` | Shipping protection upsell widget. |
| `shipping` | Shipping thresholds, rates, or display. |
| `upsell` | Upsell-related fixes (embedded, auto, FBT). |
| `auto-upsell` | Auto-upsell / Aupsell specific. |
| `free-gift` | Free gift / GWP configuration. |
| `multi-product` | Adding multiple products in a single action. |
| `rewards` | Tiered rewards, progress bar, milestone unlocks. |
| `announcement` | Announcement bar / banner. |
| `terms-checkbox` | T&C / consent checkbox before checkout. |
| `svg-icon` | SVG icon insertion or styling. |
| `analytics` | Analytics, tracking, GTM, Shopify Analytics. |
| `atc-tracking` | ATC event not firing in analytics. |
| `programmatic-open` | Using SLIDECART_OPEN() / API from custom code. |
| `programmatic` | Other use of the Slide Cart JS API. |
| `race-condition` | Async / load-order timing issues. |
| `mobile-only` | Reproduces only on mobile. |
| `theme-js` | Fix requires editing theme JavaScript files. |
| `legacy-theme` | Older theme without modern Shopify theme editor support. |
| `third-party-app` | Conflict or integration with another Shopify app. |
| `third-party-page-builder` | PageFly, Replo, GemPages, etc. |
| `weglot` | Weglot translation integration. |
| `zapiet` | Zapiet store pickup integration. |
| `pagefly` | PageFly page builder. |
| `replo` | Replo page builder. |
| `gempages` | GemPages page builder. |
| `recharge` | Recharge subscriptions. |
| `subscriptions` | General subscription app integration. |
| `loox` | Loox reviews app. |
| `judgeme` | Judge.me reviews app. |
| `yotpo` | Yotpo reviews/loyalty. |
| `custom-app` | Merchant has a custom-built app or non-standard ATC source. |
| `console-error` | Visible JavaScript console error. |
| `javascript-error` | Underlying JS error causing breakage. |
| `quantity-bug` | Wrong quantity being added/displayed. |
| `ui-bug` | Visual or interaction glitch. |
| `styling` | CSS / visual customization. |
| `multi-language` | Multi-language storefront. |
| `multi-currency` | Multi-currency setup. |
| `notification-setup` | (BIS) Initial notification configuration. |
| `klaviyo-sync` / `klaviyo` | Klaviyo integration. |
| `mailchimp-sync` / `mailchimp` | Mailchimp integration. |
| `billing` | Plan, billing, or refund issue. |
| `url-param` | URL parameter handling. |
| `hover` | Hover-state interactions. |
| `untagged` | Heuristic couldn't classify — needs manual review. |
 
---
 
## Migration notes
 
The legacy archive is **fully catalogued** (306 docs) using heuristic classification. Theme and tag accuracy is approximately 80–90%. Expect to:
 
- Find docs in keyword searches that turn out to be only tangentially relevant — open the file to confirm.
- Occasionally encounter a doc tagged with the wrong theme (the script requires "theme" near an ambiguous name like Refresh or Impact, but some docs slip through).
- Notice over-tagged entries (e.g., `rewards` shows up frequently because tiered-reward code is everywhere in the codebase).
**Going-forward conversion to template format should happen lazily**, not in bulk:
 
- When a support agent uses a legacy doc, take 90 seconds to convert it to template format, save to `fixes/`, and move the catalog row up to the **Curated fixes** section.
- Quarterly, the CS lead reviews the catalog: drops dead entries (themes we no longer support, fixes superseded by in-product changes), normalizes tags.
- If you find a tag false positive that bugs you, fix it in the row directly — don't re-run the script (it would overwrite manual fixes).
**Re-running the classifier:** if you ever do need to rebuild the legacy section from scratch, `build_catalog.py` is in the working directory. Run it and replace the auto-catalogued section below.