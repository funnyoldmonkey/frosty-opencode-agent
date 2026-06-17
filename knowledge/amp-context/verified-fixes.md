# AMP Verified Fixes Log

This file is automatically maintained by Frosty. Each entry represents a troubleshooting fix that Jall has confirmed as verified and working. Frosty references this log to resolve similar issues faster in the future.

---

### [2026-06-02] BIS Button Template/Product Type Filtering & Flicker Fix
- **Store URL:** https://adj1cvsfyklpc9vsbiny.myshopify.com/
- **Issue:** Button appearing on excluded templates, "Digital Goods" products, and flickering on first variant selection.
- **Fix Description:** Updated integration script with early exits for specific body classes and product categories, and implemented a unified visibility manager to synchronize theme ATC state and BIS state, eliminating the flicker.
- **Script:**
\`\`\`javascript
// Updated integration script with early exits and unified visibility sync
// See session log for full implementation
\`\`\`
- **Verified by Jall:** Yes

### [2026-06-08] Slide Cart German Translation (Bomique)
- **Store URL:** https://bomique.nl/
- **Theme:** Copy of Bomique (Duplicate)
- **File:** `snippets/amp-slidecart.liquid` at line 72
- **Issue:** Slide Cart content appearing in Dutch when German language is selected. Standard Shopify translations don't cover all Slide Cart elements.
- **Fix Description:** Implemented a surgical translation script using CSS class-based targeting and a debounced MutationObserver. Uses `textContent` instead of `innerText` to handle CSS `text-transform: uppercase`. Targets specific elements by class name rather than text matching to avoid race conditions.
- **Translations Applied:**
  - `Verzekerde verzending` → `Versicherter Versand`
  - `tegen schade, verlies & diefstal` → `<strong>Schutz bei Beschädigung, Verlust & Diebstahl</strong>`
  - `Nog één item voor Gratis verzending!` → `Nur noch ein Artikel bis zum <strong>kostenlosen Versand</strong>!`
  - `2 items` → `2 Artikel`
  - `GRATIS VERZENDING` → `KOSTENLOSER VERSAND`
  - `Gratis verzending toegepast!` → `<strong>Kostenloser Versand</strong> aktiviert!`
- **Script:**
\`\`\`javascript
(function() {
  const isGerman = document.documentElement.lang === 'de' || window.Shopify?.locale === 'de';
  if (!isGerman) return;

  const translateCart = () => {
    const cart = document.querySelector('#slidecarthq');
    if (!cart) return;

    // 1. Handle "X items" -> "X Artikel"
    cart.querySelectorAll('.rewards-tiers-labels-item-amount').forEach(el => {
      const text = el.textContent;
      if (text.includes('items')) {
        const newText = text.replace(/\d+\s*items/, (match) => match.replace('items', 'Artikel'));
        if (el.textContent !== newText) el.textContent = newText;
      }
    });

    // 2. Handle rewards label (use textContent to avoid CSS uppercase)
    cart.querySelectorAll('.rewards-tiers-labels-item-label').forEach(el => {
      const text = el.textContent.trim();
      if (text === 'Gratis verzending') {
        if (el.innerHTML !== 'KOSTENLOSER VERSAND') el.innerHTML = 'KOSTENLOSER VERSAND';
      }
    });

    // 3. Handle pre-unlock text (one item left)
    cart.querySelectorAll('.rewards-pre-unlock-text').forEach(el => {
      const text = el.textContent.trim();
      if (text.includes('Nog één item voor') && !el.innerHTML.includes('kostenlosen Versand')) {
        el.innerHTML = '<p>Nur noch ein Artikel bis zum <strong>kostenlosen Versand</strong>!</p>';
      }
    });

    // 4. Handle post-unlock text (free shipping activated)
    cart.querySelectorAll('.rewards-post-unlock-text').forEach(el => {
      const text = el.textContent.trim();
      if (text.includes('Gratis verzending toegepast') && !el.innerHTML.includes('Kostenloser Versand')) {
        el.innerHTML = '<p><strong>Kostenloser Versand</strong> aktiviert!</p>';
      }
    });

    // 5. Handle shipping protection title
    cart.querySelectorAll('.shipping-protection-title').forEach(el => {
      const text = el.textContent.trim();
      if (text === 'Verzekerde verzending' || text === 'Verzekerde Verzending') {
        if (el.innerHTML !== 'Versicherter Versand') el.innerHTML = 'Versicherter Versand';
      }
    });

    // 6. Handle shipping protection description
    cart.querySelectorAll('.shipping-protection-description').forEach(el => {
      const text = el.textContent.trim();
      if (text.includes('schade, verlies & diefstal') && !el.innerHTML.includes('Schutz bei Beschädigung')) {
        el.innerHTML = '<strong>Schutz bei Beschädigung, Verlust & Diebstahl</strong>';
      }
    });
  };

  if (window.ampTranslationObserver) {
    window.ampTranslationObserver.disconnect();
  }

  const initTranslation = () => {
    const cart = document.querySelector('#slidecarthq');
    if (!cart) return;

    translateCart();

    windowPampTranslationObserver = new MutationObserver(() => {
      clearTimeout(window.ampTranslationTimeout);
      window.ampTranslationTimeout = setTimeout(() => {
        translateCart();
      }, 100);
    });

    window.ampTranslationObserver.observe(cart, { childList: true, subtree: true });
  };

  if (document.readyState === 'complete') {
    initTranslation();
  } else {
    window.addEventListener('load', initTranslation);
  }
})();
\`\`\`
- **Key Learnings:**
  - Use `textContent` instead of `innerText` when CSS `text-transform: uppercase` is applied, as `innerText` returns the visually transformed text.
  - Target specific CSS classes directly instead of relying on text matching to avoid race conditions with leaf-node vs. container translations.
  - Always disconnect previous observers before re-injecting to prevent duplicate observers.
- **Verified by Jall:** Yes

### [2026-06-09] Pre-order Button Alpine.js Override Fix
- **Store URL:** https://www.prenebags.com/
- **Issue:** Alpine.js dynamically rewrites the "Add to Cart" button inner HTML, overriding the AMP Pre-order label.
- **Fix Description:** Implemented a MutationObserver that monitors the button for DOM changes and forces the button text to match the dynamic `custom_button_copy` from AppPreOrdersConfig.
- **Script:**
\`\`\`javascript
(function() {
  const SELECTORS = {
    addToCart: [
      '[data-amp-add-to-cart]',
      'form[action*="/cart/add"] [type="submit"]',
      'button[name="add"]',
      '.product-form__cart-submit',
      '.add-to-cart'
    ]
  };
  function findElement(selectors) {
    return selectors.reduce((found, selector) => found || document.querySelector(selector), null);
  }
  function getVariantId() {
    const variantElement = document.querySelector('select[name="id"], input[name="id"]:checked, input[name="id"][type="hidden"]');
    const form = document.querySelector('form[action*="/cart/add"]');
    return variantElement?.value || form?.dataset?.variantId;
  }
  function applyFix() {
    const btn = findElement(SELECTORS.addToCart);
    if (!btn) return;
    const customText = window.AppPreOrdersConfig?.custom_button_copy;
    if (!customText) return;
    const variantId = getVariantId();
    const variant = window.LiquidPreOrdersConfig?.variants?.[variantId];
    if (variant && variant.oos && variant.inventory_policy === 'continue') {
      btn.querySelectorAll('span').forEach(span => {
        if (span.textContent.trim() !== customText) {
          span.textContent = customText;
        }
      });
    }
  }

  }
})();
\`\`\`
- **Verified by Jall:** Yes

### [2026-06-09] BIS Button in Quick-Add Popups (Variant Aware)
- **Store URL:** https://www.seedsnow.com/
- **Issue:** BIS button missing in collection page quick-add drawers, hide-until-hover behavior from theme CSS, and not updating variant in BIS modal when switching variants in the drawer.
- **Fix Description:** Spoofed `BIS.urlIsProductPage()` to enable popup logic on collection pages. Implemented a high-performance MutationObserver with strict state checking to prevent browser freezes. Used pure inline styles to override theme visibility issues and dynamically sync `data-variant-id` from the Shopify variant input to ensure the correct variant loads in the BIS modal.
- **Script:**
\`\`\`javascript
(function() {
  if (window.BIS && typeof window.BIS.urlIsProductPage === 'function') {
    var origUrl = window.BIS.urlIsProductPage;
    window.BIS.urlIsProductPage = function() {
      if (document.querySelector('quick-add-drawer .product-info__add-to-cart.flex')) return true;
      return origUrl.apply(this, arguments);
    };
  }

  function updateButtonVisibility() {
    var drawer = document.querySelector('quick-add-drawer');
    if (!drawer) return;
    var target = drawer.querySelector('.product-info__add-to-cart.flex');
    if (!target) return;
    var addBtn = target.querySelector('button[name="add"]');
    var isSoldOut = addBtn && (addBtn.disabled || addBtn.innerText.toLowerCase().includes('sold out'));
    var bisButton = document.getElementById('BIS_trigger');

    if (isSoldOut) {
      if (!bisButton) {
        bisButton = document.createElement('button');
        bisButton.id = 'BIS_trigger';
        bisButton.type = 'button';
        target.parentNode.insertBefore(bisButton, target);
      }
      var targetClass = 'BIS_trigger'; 
      if (bisButton.className !== targetClass) bisButton.className = targetClass;
      var targetStyle = 'background-color:rgb(77,195,124);color:rgb(255,255,255);font-size:12.8px;font-weight:700;padding:15px 26px;border-radius:29px;border:none;text-align:center;width:100%;min-height:45px;margin-bottom:25px;cursor:pointer;display:block;opacity:1;visibility:visible;box-sizing:border-box;transition:none;';
      if (bisButton.style.cssText !== targetStyle) bisButton.style.cssText = targetStyle;
      var targetText = (window.BIS && typeof window.BIS.currentButtonCaption === 'function') ? window.BIS.currentButtonCaption() : 'EMAIL WHEN AVAILABLE';
      if (bisButton.innerText !== targetText) bisButton.innerText = targetText;
      var productLink = drawer.querySelector('a[href*="/products/"]');
      if (productLink) {
        var url = new URL(productLink.href);
        var handle = url.pathname.split('/products/')[1].split('?')[0].split('/')[0];
        if (bisButton.getAttribute('data-product-handle') !== handle) bisButton.setAttribute('data-product-handle', handle);
      }
      var variantInput = drawer.querySelector('input[name="id"]');
      var currentVariantId = variantInput ? variantInput.value : '';
      if (bisButton.getAttribute('data-variant-id') !== currentVariantId) bisButton.setAttribute('data-variant-id', currentVariantId);
    } else {
      if (bisButton && bisButton.style.display !== 'none') bisButton.style.display = 'none';
    }
  }

  var updateQueued = false;
  var observer = new MutationObserver(function() {
    if (!updateQueued) {
      updateQueued = true;
      window.requestAnimationFrame(function() {
        updateButtonVisibility();
        updateQueued = false;
      });
    }
  });
  observer.observe(document.body, { childList: true, subtree: true });
  updateButtonVisibility();
})();
\`\`\`
- **Verified by Jall:** Yes

### [2026-06-10] Slide Cart App Embed Not Firing
- **Store URL:** https://41psxk-0d.myshopify.com/
- **Issue:** App embed active in Shopify admin but script not injected into storefront HTML.
- **Fix Description:** Implemented "Fast Mode" manual script injection in theme.liquid to bypass the broken app embed link.
- **Script:**
\`\`\`html
<script>
  window.SLIDECART = true;
  window.SLIDECART_FORMAT = "{{ shop.money_format }}";
</script>
<script src="https://cdn.jsdelivr.net/gh/apphq/slidecart-dist@master/slidecarthq.js" async></script>
\`\`\`
- **Verified by Jall:** Yes

### [2026-06-10] Slide Cart Checkout Button Vertical Centering
- **Store URL:** https://41psxk-0d.myshopify.com/
- **Issue:** Checkout button text not vertically centered due to fixed height and line-height conflicts.
- **Fix Description:** Implemented Flexbox centering and normalized line-height to ensure a perfectly centered call-to-action.
- **Script:**
\`\`\`css
#slidecart-checkout-form button.button.full {
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  line-height: normal !important;
  padding: 15px 20px !important;
  height: auto !important;
  min-height: 52px !important;
}
\`\`\`
- **Verified by Jall:** Yes

### [2026-06-12] BIS App Block Conflict & Modal Trigger Fix
- **Store URL:** https://m37o2oa50lmxergl-57712541891.shopifypreview.com/
- **Issue:** BIS button disappeared/flickered on variant change, and the modal wouldn't open. Caused by App Block "removal wars" and broken `BIS.detectVariant` API.
- **Fix Description:** Implemented a non-destructive sync strategy. Instead of deleting app buttons, it uses `[id^="BIS_trigger"]` to match any BIS button (App Block or custom). It bypasses `BIS.detectVariant` by reading radio buttons directly and uses `BIS.popup.show(vid)` for reliable modal triggering.
- **Script:**
\`\`\`javascript
if (BIS.urlIsProductPage() === true) {
  BIS.popup.ready.then(function () {
    if (BIS.popup.variants.length < 1) return;
    function getCheckedVariantId() {
      var radio = document.querySelector('input[type="radio"]:checked[data-option-value-id]');
      if (radio) return Number(radio.getAttribute('data-option-value-id'));
      var detected = BIS.detectVariant(BIS.popup);
      return detected ? detected.id : null;
    }
    function getBisButton() {
      return document.querySelector('[id^="BIS_trigger"]');
    }
    function syncBisButton() {
      try {
        var anchor = document.querySelector('.product-form__submit');
        if (!anchor) return;
        var btn = getBisButton();
        if (!btn) {
          btn = document.createElement('button');
          btn.setAttribute('id', 'BIS_trigger');
          btn.setAttribute('class', 'product-form__submit button button--full-width BIS_trigger');
          btn.setAttribute('type', 'button');
          var caption = BIS.currentButtonCaption() || 'NOTIFY ME';
          btn.textContent = caption;
          btn.setAttribute('aria-label', caption);
          anchor.insertAdjacentElement('afterend', btn);
        }
        var vId = getCheckedVariantId();
        var fullVariant = vId && BIS.popup.variants.find(function (v) {
          return v.id === vId;
        });
        if (fullVariant && BIS.popup.variantIsUnavailable(fullVariant)) {
          btn.setAttribute('data-variant-id', String(fullVariant.id));
          btn.style.display = 'block';
        } else {
          btn.style.display = 'none';
        }
      } catch (e) {
        console.log('BIS sync error:', e);
      }
    }
    syncBisButton();
    setInterval(syncBisButton, 500);
    document.addEventListener('change', function (e) {
      if (e.target && e.target.getAttribute('data-option-value-id')) {
        syncBisButton();
      }
    });
    document.addEventListener('click', function (e) {
      var trigger = e.target.closest('[id^="BIS_trigger"]');
      if (!trigger) return;
      e.preventDefault();
      e.stopPropagation();
      var vid = Number(trigger.getAttribute('data-variant-id'));
      if (!vid) return;
      if (BIS.popup && BIS.popup.form && BIS.popup.form.selectVariant) {
        BIS.popup.form.selectVariant(vid);
      }
      BIS.popup.show(vid);
    }, true);
  });
}
\`\`\`
- **Verified by Jall:** Yes

### [2026-06-17] Slide Cart Mobile Scroll Conflict (Theme Drawer Conflict)
- **Store URL:** https://youandyourshealth.com/
- **Issue:** After closing Slide Cart on mobile, the page became non-scrollable. This was caused by a conflict between the theme's native cart drawer and Slide Cart when Slide Cart was set to "Drawer" mode.
- **Fix Description:** Changed Slide Cart setting from "Drawer" to "Page" to eliminate the theme conflict (fixing the scroll issue). To prevent the "Add to Cart" action from navigating to the cart page, an integration script was implemented to intercept cart links and "Add to Cart" clicks, performing an AJAX add and then manually triggering `window.SLIDECART_OPEN()`.
- **Script:**
\`\`\`javascript
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
\`\`\`
- **Verified by Jall:** Yes

