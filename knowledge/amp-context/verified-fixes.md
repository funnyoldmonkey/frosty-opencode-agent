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

  // Clear any existing observer
  if (window.ampTranslationObserver) {
    window.ampTranslationObserver.disconnect();
  }

  const initTranslation = () => {
    const cart = document.querySelector('#slidecarthq');
    if (!cart) return;

    translateCart();

    window.ampTranslationObserver = new MutationObserver(() => {
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



