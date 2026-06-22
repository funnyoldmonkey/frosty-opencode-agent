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

### [2026-06-17] Slide Cart Mobile Layout & Whitespace Optimization
- **Store URL:** https://youandyourshealth.com/
- **Issue:** Excessive whitespace on mobile, horizontal scrollbar on rewards section, and tier icons misaligned/cutoff on small screens.
- **Fix Description:** Reduced padding in header, rewards, and footer. Hidden redundant footer rows. Fixed horizontal overflow using `overflow-x: clip` and centered rewards tier icons using `translateX`.
- **Script:**
\`\`\`css
/* Amp CS fix — 2026-06-17 — Slide Cart mobile layout and whitespace optimization */
@media (max-width: 750px) {
  /* Re-center the tier icons over their labels */
  #slidecarthq .rewards-tiers-item-icon {
    transform: translateX(-43px) !important;
  }

  /* Prevent the last tier node's box from creating a horizontal scrollbar */
  #slidecarthq,
  #slidecarthq .rewards {
    overflow-x: clip !important;
  }
  
  /* Reduce header space while keeping the close button */
  #slidecarthq .header {
    padding: 10px !important;
  }

  /* "Zoom out" rewards section */
  #slidecarthq .rewards {
    padding: 25px 5px !important;
    gap: 20px !important;
    padding-top: 10px !important;
  }

  #slidecarthq .rewards .rewards-post-unlock-text {
      margin-bottom: -5px !important;
  }

  /* Minimize main footer padding */
  #slidecarthq .footer {
    padding: 5px 5px !important;
  }

  /* Hide the Discounts row (any footer row that isn't the Total) */
  #slidecarthq .footer-row:not(.amp-sc__footer-row--subtotal) {
    display: none !important;
  }

  /* Always keep the Total row visible */
  #slidecarthq .footer-row.amp-sc__footer-row--subtotal {
    display: flex !important;
  }

  /* Remove borders between footer rows for a seamless look */
  #slidecarthq .footer-row + .footer-row {
    border-top: 0px solid rgba(0, 0, 0, .1) !important;
  }

  /* Minimize individual footer row padding (Zero bottom padding) */
  #slidecarthq .footer-row {
    padding: 5px 5px 0px !important;
  }

  /* Nudge the "X items" text up and the "X% off" text down */
  #slidecarthq .rewards-tiers-labels-item-amount {
    transform: translateY(-15px) !important;
  }
  #slidecarthq .rewards-tiers-labels-item-label {
    transform: translateY(15px) !important;
  }
}
\`\`\`
- **Verified by Jall:** Yes

### [2026-06-18] Slide Cart Dynamic Rewards Bar Multi-Language Translation
- **Store URL:** https://alveraine.com/
- **Issue:** Rewards bar translations in multiple languages (ES, IT, FR) were outdated and didn't reflect the new reward percentages (10/15/20%). Standard translation methods were insufficient for dynamic rewards content.
- **Fix Description:** Implemented a custom translation object and hooked into Slide Cart's `SLIDECART_LOADED` and `SLIDECART_UPDATED` events to dynamically overwrite the `SLIDECART_STATE().settings.rewards_tiers` configuration. This ensures that labels, pre-unlock, and post-unlock text are translated based on the current Shopify locale. Also added a helper function to translate the "items" string in the rewards labels.
- **Script:**
\`\`\`html
<style>
  #slidecarthq .rewards .rewards-tiers-labels .rewards-tiers-labels-item .rewards-tiers-labels-item-amount {
    white-space: nowrap;
  }
</style>
<script>
  {% raw %}
  const customSlideCartTranslations = {
    es: {
      rewards: [
        {
          tier: 1,
          label: '10% de descuento',
          pre_unlock_text: 'Añade {{ amount }} más y recibe un *{{ reward }}*',
          post_unlock_text: '{{ reward }} aplicado!',
        },
        {
          tier: 2,
          label: '15% de descuento',
          pre_unlock_text: 'Añade {{ amount }} más y recibe un *{{ reward }}*',
          post_unlock_text: '{{ reward }} aplicado!',
        },
        {
          tier: 3,
          label: '20% de descuento',
          pre_unlock_text: 'Añade {{ amount }} más y recibe un *{{ reward }}*',
          post_unlock_text: '{{ reward }} aplicado!',
        },
      ],
    },
    it: {
      rewards: [
        {
          tier: 1,
          label: '10% di sconto',
          pre_unlock_text: 'Aggiungi {{ amount }} altro articolo e ricevi il *{{ reward }}*',
          post_unlock_text: '{{ reward }} applicato!',
        },
        {
          tier: 2,
          label: '15% di sconto',
          pre_unlock_text: 'Aggiungi {{ amount }} altro articolo e ricevi il *{{ reward }}*',
          post_unlock_text: '{{ reward }} applicato!',
        },
        {
          tier: 3,
          label: '20% di sconto',
          pre_unlock_text: 'Aggiungi {{ amount }} altro articolo e ricevi il *{{ reward }}*',
          post_unlock_text: '{{ reward }} applicato!',
        },
      ],
    },
    fr: {
      rewards: [
        {
          tier: 1,
          label: '10% de réduction',
          pre_unlock_text: 'Ajoutez-en {{ amount }} de plus et recevez *{{ reward }}*',
          post_unlock_text: '{{ reward }} appliquée!',
        },
        {
          tier: 2,
          label: '15% de réduction',
          pre_unlock_text: 'Ajoutez-en {{ amount }} de plus et recevez *{{ reward }}*',
          post_unlock_text: '{{ reward }} appliquée!',
        },
        {
          tier: 3,
          label: '20% de réduction',
          pre_unlock_text: 'Ajoutez-en {{ amount }} de plus et recevez *{{ reward }}*',
          post_unlock_text: '{{ reward }} appliquée!',
        },
      ],
    },
  };
  {% endraw %}

  const UPDATE_CURRENCY_RATE = false;

  var BASE_REWARD_AMOUNT;
  window.SLIDECART_LOADED = (cart) => {
    BASE_REWARD_AMOUNT = SLIDECART_STATE()?.settings?.rewards_tiers.map((reward) => reward.amount);

    setTimeout(window.SLIDECART_UPDATE, 1200);
  };

  function translateRewardsSC(lang) {
    let rewardsTexts = customSlideCartTranslations[lang]?.rewards;
    let currencyRate = parseFloat(Shopify?.currency?.rate);

    if (!rewardsTexts) return console.log("Rewards Translations didn't found for this lang", lang);

    SLIDECART_STATE()?.settings?.rewards_tiers.forEach((reward, indx) => {
      let currentRewardTexts = rewardsTexts[indx];

      reward.label = currentRewardTexts.label;
      reward.post_unlock_text = currentRewardTexts.post_unlock_text;
      reward.pre_unlock_text = currentRewardTexts.pre_unlock_text;

      if (currentRewardTexts.amount) {
        reward.amount = currentRewardTexts.amount;
      } else if (UPDATE_CURRENCY_RATE && currencyRate && BASE_REWARD_AMOUNT) {
        reward.amount = BASE_REWARD_AMOUNT[indx] * currencyRate;
      }
    });
  }

  function scTranslateRewardLabels() {
    const labelTranslations = {
      es: 'artículos',
      it: 'articoli',
      fr: 'articles',
    };
    if (!window?.Shopify.locale) return;
    const newLabelText = labelTranslations[window.Shopify.locale];

    if (!newLabelText) {
      console.log(\`Slide Cart: reward label translation for \${window.Shopify.locale} not found.\`);
      return;
    }

    const scRewardLabels = document.querySelectorAll('#slidecarthq .rewards .rewards-tiers-labels-item .rewards-tiers-labels-item-amount');
    scRewardLabels.forEach((label) => {
      label.textContent = label.textContent.replace('items', newLabelText);
    });
  }

  window.SLIDECART_UPDATED = (cart) => {
    let customerLenguage = window.Shopify?.locale;
    scTranslateRewardLabels();
    translateRewardsSC(customerLenguage);
  };
</script>
\`\`\`
- **Verified by Jall:** Yes

### [2026-06-19] Slide Cart Two-Column Layout with Styled Upsells (A Perfect Nomad)
- **Store URL:** https://www.aperfectnomad.com/
- **Issue:** Merchant wanted a redesigned slide cart: two-column desktop layout with "Why not add..." upsells on the left (portrait images, italic serif headers, outline ADD buttons) and the cart on the right. Mobile should show upsells inside the cart. Multiple sub-issues discovered and fixed: upsell images capped at 80px by CSS variable `--amp-sc-outside-upsell-thumb-size`, carousel overlap from `flex-wrap: wrap` + `flex-direction: column`, pro-upsells flickering on cart update (app removes/re-adds element), variant selector popups stacking on mobile, cart overflowing narrow phones.
- **Fix Description:** CSS-only fix (v11). Desktop: pro-upsells sidebar at 280px flush against cart using `.slidecarthq-overlay.open .pro-upsells.amp-sc { right: 360px }`, fade-in animation on re-render, `flex-wrap: nowrap` + `overflow-x: hidden` to prevent carousel, hidden scrollbar, `margin-top: auto` on discount-box to pin footer. Mobile: cart capped to `100%` width, overlay/option popups hidden with `display: none`, in-cart upsells shown with full-width aligned items, portrait images at 80×110px, consistent row layout. Both: italic serif headers, portrait product images, 4px corner rounding on buttons, outline-style ADD buttons.
- **Key Learnings:**
  - `--amp-sc-outside-upsell-thumb-size` CSS variable caps upsell image height at 80px via `max-height`. Override to `none` and add `max-height: none !important` with `.amp-sc` specificity.
  - Pro-upsells container has `flex-wrap: wrap` by default — combined with `flex-direction: column`, items wrap horizontally creating a broken carousel. Fix with `flex-wrap: nowrap`.
  - App removes and re-adds `.pro-upsells` on every cart update. CSS `animation` on the element triggers on re-insertion, providing a smooth fade-in.
  - Use `.slidecarthq-overlay.open` to scope pro-upsells visibility to cart-open state, and `:not(.open)` to fully hide when closed.
  - Mobile upsells (`.upsells.mobile-only`) contain fixed-position `.upsell-options` and `.upsell-options-overlay` elements (10 each) that all become visible when parent is forced to display. Must explicitly hide these.
  - Cart title text is inside an `<a>` tag — selector needs `#slidecarthq .slidecarthq.amp-sc .item .title a` for italic to work.
  - Pro-upsells lives inside `.slidecarthq-overlay`, NOT as a sibling of the cart panel. Using `::before` pseudo on the cart to create a background behind pro-upsells will cover the pro-upsells content due to stacking context.
- **Placement:** Slide Cart app → Custom CSS field (CSS-only, no JS needed)
- **CSS:**
```css
/* AMP Fix: Slide Cart two-column layout with styled upsells — v11 (CSS-only) */
/* Store: aperfectnomad.com */
/* Placement: Slide Cart app > Custom CSS field */
@keyframes amp-upsells-fade-in {
  from { opacity: 0; }
  to { opacity: 1; }
}
/* ===================== DESKTOP ===================== */
@media (min-width: 769px) {
  #slidecarthq .pro-upsells.amp-sc {
    --amp-sc-outside-upsell-thumb-size: none !important;
  }
  #slidecarthq .slidecarthq.amp-sc { border-radius: 0 !important; }
  #slidecarthq .pro-upsells { animation: amp-upsells-fade-in 0.15s ease-out !important; }
  #slidecarthq .slidecarthq .header > span {
    font-style: italic !important;
    font-family: "Times New Roman", Times, serif !important;
  }
  #slidecarthq .slidecarthq.amp-sc .item .title,
  #slidecarthq .slidecarthq.amp-sc .item .title a { font-style: italic !important; }
  #slidecarthq .slidecarthq .rewards-unlock-text,
  #slidecarthq .slidecarthq .rewards-unlock-text p,
  #slidecarthq .slidecarthq .rewards-post-unlock-text,
  #slidecarthq .slidecarthq .rewards-post-unlock-text p,
  #slidecarthq .slidecarthq .rewards-pre-unlock-text,
  #slidecarthq .slidecarthq .rewards-pre-unlock-text p { font-style: italic !important; }
  #slidecarthq .slidecarthq .item .item-image-anchor {
    width: 110px !important; height: 160px !important; flex-shrink: 0 !important;
  }
  #slidecarthq .slidecarthq .item .item-image-anchor img {
    width: 100% !important; height: 100% !important; object-fit: cover !important;
    border-radius: 4px !important; aspect-ratio: auto !important;
  }
  #slidecarthq .pro-upsells {
    width: 280px !important;
    background-color: rgb(251, 251, 248) !important;
    border-radius: 0 !important;
    border-right: 1px solid rgba(0, 0, 0, 0.08) !important;
    padding: 30px 24px 24px !important;
    height: auto !important;
    display: flex !important;
    flex-direction: column !important;
    align-items: stretch !important;
    margin: 0 !important;
  }
  #slidecarthq .slidecarthq-overlay.open .pro-upsells.amp-sc {
    right: 360px !important;
    top: 16px !important;
    bottom: 16px !important;
  }
  #slidecarthq .slidecarthq-overlay:not(.open) .pro-upsells {
    display: none !important;
    visibility: hidden !important;
    opacity: 0 !important;
    pointer-events: none !important;
  }
  #slidecarthq .pro-upsells .container {
    gap: 30px !important;
    overflow-y: auto !important;
    overflow-x: hidden !important;
    flex-wrap: nowrap !important;
    flex: 1 !important;
    scrollbar-width: none !important;
    -ms-overflow-style: none !important;
  }
  #slidecarthq .pro-upsells .container::-webkit-scrollbar {
    display: none !important; width: 0 !important; height: 0 !important;
  }
  #slidecarthq .pro-upsells .upsells-header { margin-bottom: 20px !important; }
  #slidecarthq .pro-upsells .upsells-header span {
    font-style: italic !important; font-size: 22px !important; font-weight: 400 !important;
    font-family: "Times New Roman", Times, serif !important;
  }
  #slidecarthq .pro-upsells .upsell-image,
  #slidecarthq .pro-upsells.amp-sc .upsell-image {
    width: 100% !important; height: auto !important; max-height: none !important; margin: 0 !important;
  }
  #slidecarthq .pro-upsells .upsell-image a,
  #slidecarthq .pro-upsells.amp-sc .upsell-image a {
    display: block !important; width: 100% !important; height: auto !important;
  }
  #slidecarthq .pro-upsells .upsell-image img,
  #slidecarthq .pro-upsells.amp-sc .upsell-image img {
    width: 100% !important; height: auto !important; max-height: none !important;
    aspect-ratio: 2 / 3 !important; object-fit: cover !important; border-radius: 0 !important;
  }
  #slidecarthq .pro-upsells .upsell-item {
    flex-direction: column !important; align-items: stretch !important; gap: 6px !important;
  }
  #slidecarthq .pro-upsells .upsell-text {
    flex-direction: column !important; align-items: flex-start !important; text-align: left !important;
  }
  #slidecarthq .pro-upsells .upsell-text p {
    font-style: italic !important; font-size: 13px !important; margin: 0 !important;
  }
  #slidecarthq .pro-upsells .upsell-text-prices { font-size: 14px !important; }
  #slidecarthq .pro-upsells .upsell-add { width: 100% !important; }
  #slidecarthq .pro-upsells .upsell-add button {
    background-color: transparent !important; color: #000 !important;
    border: 1px solid #000 !important; border-radius: 0 !important;
    width: 100% !important; padding: 10px 14px !important; font-size: 11px !important;
    text-transform: uppercase !important; letter-spacing: 0.08em !important;
    cursor: pointer !important; transition: background-color 0.2s, color 0.2s !important;
  }
  #slidecarthq .pro-upsells .upsell-add button:hover {
    background-color: #000 !important; color: #fff !important;
  }
  #slidecarthq .slidecarthq .discount-box { margin-top: auto !important; }
  #slidecarthq .slidecarthq .footer { margin-top: 0 !important; }
  #slidecarthq .slidecarthq .footer .button.full { border-radius: 4px !important; }
  #slidecarthq .slidecarthq .discount-box input,
  #slidecarthq .slidecarthq .discount-box button { border-radius: 4px !important; }
  #slidecarthq .slidecarthq .header { border-radius: 0 !important; }
}
/* ===================== MOBILE ===================== */
@media (max-width: 768px) {
  #slidecarthq .pro-upsells { display: none !important; }
  #slidecarthq .slidecarthq.amp-sc { max-width: 100% !important; width: 100% !important; }
  #slidecarthq .slidecarthq .upsells .upsell-options-overlay {
    display: none !important; opacity: 0 !important; pointer-events: none !important;
  }
  #slidecarthq .slidecarthq .upsells .upsell-options { display: none !important; }
  #slidecarthq .slidecarthq .upsells.mobile-only,
  #slidecarthq .slidecarthq .upsells.upsells-stacked-container {
    display: flex !important; flex-direction: column !important;
    padding: 16px !important; border-top: 1px solid rgba(0, 0, 0, 0.08) !important;
  }
  #slidecarthq .slidecarthq .upsells-header.mobile-only {
    display: block !important; margin-bottom: 12px !important; text-align: center !important;
  }
  #slidecarthq .slidecarthq .upsells-header span {
    font-style: italic !important; font-size: 18px !important; font-weight: 400 !important;
    font-family: "Times New Roman", Times, serif !important;
  }
  #slidecarthq .slidecarthq .upsells-stacked.mobile-only {
    display: flex !important; flex-direction: column !important; gap: 12px !important;
  }
  #slidecarthq .slidecarthq .upsells .upsell.multi { display: block !important; width: 100% !important; }
  #slidecarthq .slidecarthq .upsells .upsell-item {
    display: flex !important; flex-direction: row !important; gap: 10px !important;
    align-items: center !important; width: 100% !important; padding: 12px !important;
    background: rgba(0, 0, 0, 0.02) !important; border-radius: 4px !important;
  }
  #slidecarthq .slidecarthq .upsells .upsell-image {
    width: 80px !important; height: 110px !important; flex-shrink: 0 !important; overflow: hidden !important;
  }
  #slidecarthq .slidecarthq .upsells .upsell-image a {
    display: block !important; width: 100% !important; height: 100% !important;
  }
  #slidecarthq .slidecarthq .upsells .upsell-image img {
    width: 80px !important; height: 110px !important; object-fit: cover !important;
    border-radius: 0 !important; max-height: none !important;
  }
  #slidecarthq .slidecarthq .upsells .upsell-text { flex: 1 !important; min-width: 0 !important; }
  #slidecarthq .slidecarthq .upsells .upsell-text p {
    font-style: italic !important; font-size: 13px !important;
  }
  #slidecarthq .slidecarthq .upsells .upsell-add { flex-shrink: 0 !important; }
  #slidecarthq .slidecarthq .upsells .upsell-add button {
    background-color: transparent !important; color: #000 !important;
    border: 1px solid #000 !important; border-radius: 0 !important;
    padding: 8px 14px !important; font-size: 11px !important; text-transform: uppercase !important;
  }
  #slidecarthq .slidecarthq .item .item-image-anchor {
    width: 80px !important; height: 110px !important; flex-shrink: 0 !important;
  }
  #slidecarthq .slidecarthq .item .item-image-anchor img {
    width: 100% !important; height: 100% !important; object-fit: cover !important; max-height: none !important;
  }
  #slidecarthq .slidecarthq.amp-sc .item .title,
  #slidecarthq .slidecarthq.amp-sc .item .title a { font-style: italic !important; }
  #slidecarthq .slidecarthq .rewards-unlock-text,
  #slidecarthq .slidecarthq .rewards-unlock-text p,
  #slidecarthq .slidecarthq .rewards-post-unlock-text p,
  #slidecarthq .slidecarthq .rewards-pre-unlock-text p { font-style: italic !important; }
  #slidecarthq .slidecarthq .header > span {
    font-style: italic !important; font-family: "Times New Roman", Times, serif !important;
  }
  #slidecarthq .slidecarthq.amp-sc { border-radius: 0 !important; }
  #slidecarthq .slidecarthq .footer .button.full { border-radius: 4px !important; }
  #slidecarthq .slidecarthq .discount-box input,
  #slidecarthq .slidecarthq .discount-box button { border-radius: 4px !important; }
  #slidecarthq .slidecarthq .header { border-radius: 0 !important; }
}
```
- **Verified by Jall:** Yes

### [2026-06-19] Slide Cart shifted off-screen and sizing on Impulse theme
- **Store URL:** https://modaavenueplzen.com/collections/elegantni-saty/products/melis-grace-kleid
- **Issue:** Slide Cart drawer remained off-screen on mobile due to `transform: matrix` and didn't fill 100% width.
- **Fix Description:** Forced `transform: none` and `width: 100%` using specific selectors and breakpoints for the Impulse theme.
- **Script:**
```css
@media screen and (max-width: 749px) {
  #slidecarthq .slidecarthq.open {
    transform: none !important;
  }
}
@media (max-width: 768px) {
  #slidecarthq .slidecarthq {
    max-width: 100% !important;
    width: 100% !important;
  }
}
```
- **Verified by Jall:** Yes

### [2026-06-22] BIS 'askPermission' TypeError on Webpush
- **Store URL:** https://lasretro.com/products/camiseta-portugal-visitante-2026
- **Issue:** Uncaught TypeError: Cannot read properties of null (reading 'askPermission') when submitting the BIS modal with 'webpush' as the default channel. This happens because `selectDefaultChannel()` sets the channel to "webpush" but fails to initialize the `bisWebpush` instance.
- **Fix Description:** Patch `window.BIS.Form.prototype.handleSubmit` to check if the current channel is 'webpush' and `bisWebpush` is null. If so, call `initWebPush()` before proceeding with the original submission logic.
- **Script:**
```javascript
(function() {
  if (window.BIS && window.BIS.Form && window.BIS.Form.prototype) {
    const originalHandleSubmit = window.BIS.Form.prototype.handleSubmit;
    window.BIS.Form.prototype.handleSubmit = function() {
      if (this.currentChannel === 'webpush' && !this.bisWebpush && typeof this.initWebPush === 'function') {
        this.initWebPush();
      }
      return originalHandleSubmit.apply(this, arguments);
    };
  }
})();
```
- **Verified by Jall:** Yes

### [2026-06-22] Slide Cart GWP Auto-Add Fix
- **Store URL:** https://neutraliz.com
- **Issue:** Slide Cart's gift-with-purchase (GWP) isn't auto-adding when a reward tier is reached. Instead, it shows manual "AJOUTER" buttons.
- **Fix Description:** Injected a script to listen to `SLICECART_UPDATED` and `SLICECART_LOADED`, check reward tiers via `SLIDECART_STATE()`, and automatically add/remove GWP items via Shopify AJAX API.
- **Script:**
\`\`\`javascript
<!-- AMP Fix: Slide Cart auto-add gift-with-purchase when tier reached (and auto-remove below) -->
<script>
(function () {
  if (window.__ampGiftFix) return;
  window.__ampGiftFix = true;

  var BUSY = false, TIMER = null, GIFT_PROP = '_amp_gift';
  // Tracks variant IDs we know are/were free gifts, so they can be safely removed if the tier locks.
  window.__ampGiftManaged = window.__ampGiftManaged || {};

  // Read the free-gift reward tiers straight from Slide Cart's own settings.
  function getGiftTiers() {
    try {
      var s = window.SLIDECART_STATE();
      if (!s || !s.settings) return null;
      var useCount = s.settings.rewards_count === true; // false = threshold measured by cart total
      var gifts = [];
      (s.settings.rewards_tiers || []).forEach(function (t) {
        if (t.rewards_type !== 'free_gift' || !t.free_gifts) return;
        var g; try { g = JSON.parse(t.free_gifts); } catch (e) { return; }
        (g.items || []).forEach(function (it) {
          (it.variants || []).forEach(function (v) {
            var vid = parseInt(String(v.id).split('/').pop(), 10);
            if (vid) gifts.push({ threshold: parseFloat(t.amount), variantId: vid });
          });
        });
      });
      return { useCount: useCount, gifts: gifts };
    } catch (e) { return null; }
  }

  // cart: the Shopify cart object Slide Cart passes into SLICECART_LOADED / SLICECART_UPDATED.
  async function reconcile(cart) {
    if (BUSY) return;
    var cfg = getGiftTiers();
    if (!cfg || !cfg.gifts.length) return;

    if (!cart || !cart.items) {
      try { cart = await fetch('/cart.js', { headers: { 'Accept': 'application/json' } }).then(function (r) { return r.json(); }); }
      catch (e) { return; }
    }

    var items = cart.items || [];
    var giftIds = cfg.gifts.map(function (g) { return g.variantId; });

    // Qualifying amount excludes every gift line, so gifts never count toward the threshold.
    var qualCents = 0, qualCount = 0;
    items.forEach(function (it) {
      if (giftIds.indexOf(it.id) > -1) return;
      qualCents += it.final_line_price;
      qualCount += it.quantity;
    });

    // Remember any gift line that is currently free (tagged by us OR discounted to 0 by the app).
    items.forEach(function (it) {
      if (giftIds.indexOf(it.id) === -1) return;
      if ((it.properties && it.properties[GIFT_PROP]) || it.final_price === 0) {
        window.__ampGiftManaged[it.id] = true;
      }
    });

    var adds = [], removes = [];
    cfg.gifts.forEach(function (g) {
      var unlocked = cfg.useCount ? (qualCount >= g.threshold) : (qualCents >= Math.round(g.threshold * 100));
      var lines = items.filter(function (it) { return it.id === g.variantId; });
      if (unlocked) {
        if (lines.length === 0) adds.push(g.variantId);
        else if (lines.length > 1) for (var k = 1; k < lines.length; k++) removes.push(lines[k].key); // de-dupe
      } else if (window.__ampGiftManaged[g.variantId]) {
        // Tier locked: pull the gift so the customer is never charged for it (the discount drops off below threshold).
        lines.forEach(function (l) { removes.push(l.key); });
        delete window.__ampGiftManaged[g.variantId];
      }
    });

    if (!adds.length && !removes.length) return;

    BUSY = true;
    try {
      for (var i = 0; i < removes.length; i++) {
        await fetch('/cart/change.js', {
          method: 'POST', headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ id: removes[i], quantity: 0 })
        });
      }
      for (var j = 0; j < adds.length; j++) {
        await fetch('/cart/add.js', {
          method: 'POST', headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ items: [{ id: adds[j], quantity: 1, properties: { _amp_gift: '1' } }] })
        });
        window.__ampGiftManaged[adds[j]] = true;
      }
    } catch (e) {
      console.log('[AMP gift fix]', e);
    } finally {
      // Re-render Slide Cart so the gift line shows/clears immediately.
      await new Promise(function (res) { try { window.SLIDECART_UPDATE(res); } catch (e) { res(); } });
      BUSY = false;
    }
  }

  // Small debounce: a single user action can fire SLICECART_UPDATED more than once.
  function schedule(cart) { clearTimeout(TIMER); TIMER = setTimeout(function () { reconcile(cart); }, 200); }

  // Event-driven: Slide Cart calls SLICECART_UPDATED on every cart change (add, remove, quantity change),
  // and SLICECART_LOADED once on first load. We chain any handler already assigned to them so we don't clobber it.
  var prevLoaded = window.SLICECART_LOADED, prevUpdated = window.SLICECART_UPDATED;
  window.SLICECART_LOADED = function (cart) {
    if (typeof prevLoaded === 'function') { try { prevLoaded(cart); } catch (e) {} }
    schedule(cart);
  };
  window.SLICECART_UPDATED = function (cart) {
    if (typeof prevUpdated === 'function') { try { prevUpdated(cart); } catch (e) {} }
    schedule(cart);
  };
})();
</script>
<!-- End of AMP Fix: Slide Cart auto-add gift-with-purchase when tier reached (and auto-remove below) -->
\`\`\`
- **Verified by Jall:** Yes
```
