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

### [2026-06-23] Slide Cart: Shipping Protection Price and Translation fix for PLN
- **Store URL:** https://maja-bizuteria.pl
- **Issue:** Shipping protection showed the raw Euro price (2,95 zł) instead of the converted Polish Zloty price (~13,00 zł). Also, the "Discounts" footer label was in English.
- **Fix Description:** Implemented a script that fetches the actual price of the protection variant from the Shopify product JSON and translates the "Discounts" label to "Rabaty". The script hooks into Slide Cart's lifecycle events and uses a MutationObserver for persistence.
- **Script:**
\`\`\`liquid
{%- comment -%}
  AMP Slide Cart fixes for maja-bizuteria.pl (yqi2tr-vk.myshopify.com)
  Store base currency: EUR — displayed currency: PLN (Shopify Markets, rate ~4.3)

  Contains two fixes:
    1. Shipping protection price shows the real charged amount (13,00 zł) instead of
       the raw EUR setting value (2,95 zł).
    2. The cart "Discounts" footer label is translated to Polish ("Rabaty").

  NOTE: the <script> is wrapped in {% raw %} so Liquid does not strip the price
  format tokens, and the money format is read at runtime so it works no matter how
  early the snippet loads. Render this snippet from theme.liquid.
{%- endcomment -%}

<!-- AMP Fix: Slide Cart PLN protection price + Polish "Discounts" label -->
{% raw %}
<script>
(function () {
  if (window.__ampPlnFix) { window.__ampPlnFix.run(); return; }

  // Shipping-protection product on this store (handle + variant id from app settings)
  var PROTECTION_HANDLE = 'ochrona-przesylki';
  var PROTECTION_VARIANT_ID = 57758956224860;
  var DISCOUNTS_LABEL_PL = 'Rabaty';

  // Format cents into the store's money format. Read SLIDECART_FORMAT at call time
  // (not once at load) so it is always available, and fall back to "<amount> zł".
  function formatMoney(cents) {
    var fmt = window.SLIDECART_FORMAT ||
              (window.Shopify && window.Shopify.money_format) || '';
    var parts = (cents / 100).toFixed(2).split('.');     // comma decimal, dot thousands
    parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, '.');
    var amount = parts.join(',');
    if (/\{\{[^}]*\}\}/.test(fmt)) return fmt.replace(/\{\{[^}]*\}\}/, amount);
    return amount + ' zł';
  }

  // Fetch the protection variant's REAL price in the active (displayed) currency once.
  var protectionPriceCents = null;
  function loadProtectionPrice() {
    if (protectionPriceCents != null) return Promise.resolve(protectionPriceCents);
    return fetch('/products/' + PROTECTION_HANDLE + '.js', { headers: { Accept: 'application/json' } })
      .then(function (r) { return r.json(); })
      .then(function (p) {
        var v = (p.variants || []).filter(function (x) { return x.id === PROTECTION_VARIANT_ID; })[0] || (p.variants || [])[0];
        protectionPriceCents = v ? v.price : null;
        return protectionPriceCents;
      })
      .catch(function () {
        // Fallback: convert the configured base amount by the active currency rate.
        try {
          var amt = parseFloat(window.SLIDECART_STATE().settings.shipping_protection_amount);
          var rate = parseFloat((window.Shopify && window.Shopify.currency && window.Shopify.currency.rate) || 1);
          protectionPriceCents = Math.round(amt * rate) * 100;
        } catch (e) { protectionPriceCents = null; }
        return protectionPriceCents;
      });
  }

  function applyFixes() {
    var root = document.querySelector('#slidecarthq');
    if (!root) return;

    // Fix 1: show the real charged protection price (13,00 zł, not 2,95 zł)
    try {
      var priceEl = root.querySelector('.shipping-protection .price');
      if (priceEl && protectionPriceCents != null) {
        var correct = formatMoney(protectionPriceCents);
        if (priceEl.textContent.trim() !== correct) priceEl.textContent = correct;
      }
    } catch (e) {}

    // Fix 2: translate the "Discounts" footer label to Polish
    try {
      var discRow = root.querySelector('.amp-sc__footer-row--discount');
      if (discRow && discRow.firstChild && discRow.firstChild.nodeType === 3 &&
          discRow.firstChild.textContent.trim() === 'Discounts') {
        discRow.firstChild.textContent = DISCOUNTS_LABEL_PL;
      }
    } catch (e) {}
  }

  var t;
  function run() { loadProtectionPrice().then(applyFixes); }
  function scheduled() { clearTimeout(t); t = setTimeout(applyFixes, 50); }

  // Chain Slide Cart's own callbacks so we don't clobber existing handlers.
  var pl = window.SLIDECART_LOADED, pu = window.SLIDECART_UPDATED, po = window.SLIDECART_OPENED;
  window.SLIDECART_LOADED  = function (c) { if (typeof pl === 'function') { try { pl(c); } catch (e) {} } run(); };
  window.SLIDECART_UPDATED = function (c) { if (typeof pu === 'function') { try { pu(c); } catch (e) {} } scheduled(); };
  window.SLIDECART_OPENED  = function ()  { if (typeof po === 'function') { try { po(); } catch (e) {} } scheduled(); };

  // Safety net: re-apply on any DOM change inside the drawer (debounced, scoped).
  function attachObserver() {
    var host = document.querySelector('#slidecarthq');
    if (!host) { return setTimeout(attachObserver, 500); }
    new MutationObserver(scheduled).observe(host, { childList: true, subtree: true, characterData: true });
  }
  attachObserver();

  window.__ampPlnFix = { run: run, apply: applyFixes };
  run();
})();
</script>
{% endraw %}
\`\`\`
- **Verified by Jall:** Yes

### [2026-06-24] BIS Proxy Subpath Rewrite
- **Store URL:** https://glamrgear.com
- **Issue:** BIS signup submission fails with 404 because the client requests `/apps/bis/signups/create.json` but the store's App Proxy is registered at `/apps/backinstock`.
- **Fix Description:** Monkey-patched `window.BIS.request` and `window.BIS.requestJSONP` to rewrite the `/apps/bis/` subpath to `/apps/backinstock/` dynamically. Included a polling mechanism to ensure the patch is applied after `window.BIS` is initialized.
- **Script:**
\`\`\`javascript
(function () {
  var WRONG = '/apps/bis/';
  var RIGHT = '/apps/backinstock/';

  function fixUrl(u) {
    return (typeof u === 'string' && u.indexOf(WRONG) !== -1) ? u.replace(WRONG, RIGHT) : u;
  }

  function patch() {
    if (!window.BIS) return false;
    ['requestJSONP', 'request'].forEach(function (fn) {
      if (typeof window.BIS[fn] === 'function' && !window.BIS[fn].__ampProxyPatched) {
        var orig = window.BIS[fn];
        window.BIS[fn] = function () {
          var args = Array.prototype.slice.call(arguments);
          if (args.length && typeof args[0] === 'string') args[0] = fixUrl(args[0]);
          return orig.apply(this, args);
        };
        window.BIS[fn].__ampProxyPatched = true;
      }
    });
    return !!(window.BIS.requestJSONP && window.BIS.requestJSONP.__ampProxyPatched);
  }

  if (!patch()) {
    var tries = 0;
    var iv = setInterval(function () {
      if (patch() || ++tries > 100) clearInterval(iv);
    }, 200);
  }
})();
\`\`\`
- **Verified by Jall:** Yes

### [2026-06-24] Force-show BIS button on in-stock PDPs (Custom OOS Logic)
- **Store URL:** https://dirtylabs.com
- **Issue:** BIS button not showing on products with custom out-of-stock logic (Shopify reports available: true, but merchant suppresses Add to Cart). _BISConfig.button.visible = true is insufficient.
- **Fix Description:** Overrode `BIS.popup.variantIsUnavailable` to return true and forced `popup.createUI()` call. Hid the native floating button and injected a custom inline button styled to match the theme's purchase button, triggered via a merchant allow-list of URLs.
- **Script:**
```html
<script>
(function () {
  var AMP_BIS_FORCE_SHOW = [
    "https://dirtylabs.com/products/aestival-bio-enzyme-liquid-dish-soap?variant=43324222505096",
  ];
  var INLINE_ID = "amp-bis-inline";
  function currentHandle() {
    var m = location.pathname.match(/\/products\/([^\/?#]+)/);
    return m ? m[1] : null;
  }
  function matchEntry() {
    var h = currentHandle();
    if (!h) return null;
    for (var i = 0; i < AMP_BIS_FORCE_SHOW.length; i++) {
      var e = AMP_BIS_FORCE_SHOW[i];
      if (typeof e === "string") {
        if (e === h || e.indexOf("/products/" + h) !== -1) return { handle: h, variants: null };
      } else if (e && e.handle === h) {
        return { handle: h, variants: (e.variants || []).map(Number) };
      }
    }
    return null;
  }
  var entry = matchEntry();
  if (!entry) return;
  function whenReady(cb) {
    var tries = 0;
    (function poll() {
      if (window.BIS && BIS.popup && BIS.popup._variantsById &&
          Object.keys(BIS.popup._variantsById).length) { cb(); return; }
      if (tries++ > 200) return;
      setTimeout(poll, 100);
    })();
  }
  function eligibleVariants(popup) {
    var all = Object.keys(popup._variantsById).map(function (k) { return popup._variantsById[k]; });
    if (!entry.variants || !entry.variants.length) return all;
    return all.filter(function (v) { return entry.variants.indexOf(Number(v.id)) !== -1; });
  }
  function currentVariantId(popup) {
    var input = document.querySelector('form[action*="/cart/add"] [name="id"]');
    if (input && input.value) return Number(input.value);
    var u = new URLSearchParams(location.search).get("variant");
    if (u) return Number(u);
    var ev = eligibleVariants(popup);
    return ev.length ? ev[0].id : null;
  }
  function hideNativeButton() {
    if (document.getElementById("amp-bis-hide-native")) return;
    var st = document.createElement("style");
    st.id = "amp-bis-hide-native";
    st.textContent = ".bis-button{display:none !important;}";
    document.head.appendChild(st);
  }
  function isVisible(el) {
    if (!el) return false;
    var r = el.getBoundingClientRect();
    return el.offsetParent !== null && r.width > 1 && r.height > 1;
  }
  function widestVisible(sel) {
    var els = Array.prototype.slice.call(document.querySelectorAll(sel)).filter(isVisible);
    els.sort(function (a, b) { return b.getBoundingClientRect().width - a.getBoundingClientRect().width; });
    return els[0] || null;
  }
  function getAnchorAndRef() {
    var soldOut = widestVisible("#sold-out, .sold-out button");
    if (soldOut && soldOut.getBoundingClientRect().width < 100) soldOut = null;
    var addBtn = widestVisible('#add, [name="add"]');
    if (addBtn && addBtn.getBoundingClientRect().width < 100) addBtn = null;
    var payBtn = widestVisible(".shopify-payment-button");
    var ref = soldOut || addBtn;
    if (!ref) return { anchor: null, ref: null };
    var anchor;
    if (soldOut) {
      anchor = soldOut.closest(".sold-out") || soldOut;
    } else if (payBtn) {
      anchor = payBtn;
    } else {
      anchor = addBtn.closest(".quantity-cart-row, .details-row, .add-to-cart") || addBtn;
    }
    return { anchor: anchor, ref: ref };
  }
  function makeInlineButton(popup) {
    var ar = getAnchorAndRef();
    if (!ar.anchor || !ar.ref) return false;
    var cs = getComputedStyle(ar.ref);
    var copy = ["backgroundColor", "color", "borderRadius",
      "borderTopWidth", "borderTopStyle", "borderTopColor",
      "borderRightWidth", "borderRightStyle", "borderRightColor",
      "borderBottomWidth", "borderBottomStyle", "borderBottomColor",
      "borderLeftWidth", "borderLeftStyle", "borderLeftColor",
      "fontFamily", "fontSize", "fontWeight", "fontStyle", "letterSpacing",
      "textTransform", "lineHeight", "textAlign", "height", "minHeight",
      "paddingTop", "paddingBottom", "paddingLeft", "paddingRight"];
    var btn = document.createElement("button");
    btn.type = "button";
    btn.id = INLINE_ID;
    copy.forEach(function (p) { btn.style[p] = cs[p]; });
    btn.style.setProperty("background-color", "#000000", "important");
    btn.style.setProperty("color", "#ffffff", "important");
    btn.style.setProperty("border", "none", "important");
    btn.style.display = "flex";
    btn.style.alignItems = "center";
    btn.style.justifyContent = "center";
    btn.style.width = "100%";
    btn.style.boxSizing = "border-box";
    btn.style.cursor = "pointer";
    btn.style.marginTop = "10px";
    btn.textContent = (window.BIS.currentButtonCaption && window.BIS.currentButtonCaption()) || "NOTIFY ME WHEN AVAILABLE";
    btn.addEventListener("click", function (e) {
      e.preventDefault();
      e.stopPropagation();
      var vid = currentVariantId(popup);
      if (vid) popup.show(vid);
    });
    ar.anchor.insertAdjacentElement("afterend", btn);
    return true;
  }
  function build() {
    var popup = window.BIS.popup;
    if (!popup || !popup._variantsById) return;
    popup.variantIsUnavailable = function () { return true; };
    eligibleVariants(popup).forEach(function (v) {
      if (!popup.variants.some(function (x) { return x.id === v.id; })) popup.variants.push(v);
    });
    if (!popup.variants.length) return;
    if (!popup.form) { try { popup.createUI(); } catch (e) { /* no-op */ } }
    hideNativeButton();
    if (!document.getElementById(INLINE_ID)) makeInlineButton(popup);
  }
  whenReady(function () {
    build();
    var guard = setInterval(function () {
      if (!document.getElementById(INLINE_ID)) build();
    }, 750);
    setTimeout(function () { clearInterval(guard); }, 30000);
  });
})();
</script>
- **Verified by Jall:** Yes
```

### [2026-06-24] Slide Cart Market-Based GWP (dynamic per-market load)
- **Store URL:** beauty-of-joseon-global.myshopify.com
- **Issue:** GWP program needed to differ per Shopify Market (UK, US, EU, ROW) with correct currency conversion, and avoid Liquid stripping of tokens like `{{ amount }}` and `{{ reward }}`.
- **Fix Description:** Implemented a self-contained liquid snippet (`snippets/amp-slidecart.liquid`) that detects market via `window.Shopify.country`, lazy-loads the corresponding gift products, converts thresholds using `Shopify.currency.rate`, and injects them into `window.SLIDECART_STATE().settings.rewards_tiers`. Wrapped in `{% raw %}` to prevent Liquid processing of JS tokens.
- **Script:**
\`\`\`liquid
<!-- AMP Fix: Slide Cart market-based GWP (dynamic per-market load) — Beauty of Joseon Global -->
{% raw %}
<script>
(function () {
  if (window.__ampMarketGwp) return;          // run once
  window.__ampMarketGwp = true;

  /* ---- 1. Per-market gifts (EDIT HERE) ----------------------
     handle = gift product URL handle
     base   = unlock threshold in USD (auto-converted to local currency) */
  var MARKET_GIFTS = {
    uk: [
      { handle: 'relief-sun-mini-10ml-copy',                  base: 1   }, // 82BU002
      { handle: 'uk-test-calming-serum-green-tea-panthenol',  base: 65  }, // 82BS008
      { handle: 'glow-deep-serum-rice-alpha-arbutin-copy-2',  base: 105 }  // 82BS032
    ],
    us:  [ { handle: 'day-dew-sunscreen-10ml-copy-1',         base: 1   } ], // 01BU015
    eu:  [ { handle: 'light-on-serum-mini-10ml-copy',         base: 1   } ], // 82BS019
    row: [ { handle: 'revive-eye-serum-mini-10ml-copy',       base: 1   } ]  // 82BS020
  };
  var EU_COUNTRIES = ['FR', 'DE', 'NL', 'BE', 'ES', 'IT', 'IE'];

  // Fallback unlock text, used only if no dashboard free-gift tier is found.
  var DEFAULT_TEXT = {
    label: 'FREE item',
    pre_unlock_text: 'Spend {{ amount }} more and get *{{ reward }}*',
    post_unlock_text: '{{ reward }} applied!'
  };

  /* ---- internals ------------------------------------------- */
  var builtCache = {};        // market -> built tier array (fetched once)
  var nonGiftTiers = null;    // any non-free-gift reward tiers, preserved
  var textTemplate = null;    // label + unlock text reused from dashboard
  var busy = false;           // re-entrancy guard for our own re-render

  function getMarket() {
    var c = '';
    try { c = (window.Shopify && window.Shopify.country) ? String(window.Shopify.country).toUpperCase() : ''; } catch (e) {}
    if (c === 'GB') return 'uk';
    if (c === 'US') return 'us';
    if (EU_COUNTRIES.indexOf(c) !== -1) return 'eu';
    return 'row';
  }

  function currencyRate() {
    try {
      var r = parseFloat(window.Shopify && window.Shopify.currency && window.Shopify.currency.rate);
      return (r && r > 0) ? r : 1;
    } catch (e) { return 1; }
  }

  // Capture the label + unlock text from the merchant's existing free-gift
  // tier (prefer the pristine settingsBackup, which keeps the tokens intact),
  // so our injected tiers read exactly like the dashboard config.
  function captureTemplate(st) {
    if (textTemplate) return;
    var sources = [];
    if (st.settingsBackup && Array.isArray(st.settingsBackup.rewards_tiers)) sources = sources.concat(st.settingsBackup.rewards_tiers);
    if (Array.isArray(st.settings.rewards_tiers)) sources = sources.concat(st.settings.rewards_tiers);
    var gt = sources.filter(function (t) { return t && t.rewards_type === 'free_gift' && /\{\{/.test(t.pre_unlock_text || ''); })[0]
          || sources.filter(function (t) { return t && t.rewards_type === 'free_gift'; })[0];
    textTemplate = gt
      ? { label: gt.label, pre_unlock_text: gt.pre_unlock_text, post_unlock_text: gt.post_unlock_text }
      : DEFAULT_TEXT;
  }

  // Build a free-gift reward tier from a /products/<handle>.js payload.
  function buildTier(product, cfg, rate) {
    var v = product.variants && product.variants[0];
    if (!v) return null;
    var img = (product.featured_image || '').replace(/^\/\//, 'https://');
    var vImg = (v.featured_image && v.featured_image.src) ? v.featured_image.src : '';
    var localAmount = (parseFloat(cfg.base) * rate).toFixed(2);   // convert USD -> active currency
    var freeGifts = {
      discount_percentage: 100,
      items: [{
        id: 'gid://shopify/Product/' + product.id,
        handle: product.handle,
        image: img,
        title: product.title,
        variants: [{
          id: 'gid://shopify/ProductVariant/' + v.id,
          image: vImg, position: 1, sku: v.sku, title: v.title
        }]
      }]
    };
    return {
      tier: 1,
      amount: String(localAmount),
      free_gifts: JSON.stringify(freeGifts),
      label: textTemplate.label,
      pre_unlock_text: textTemplate.pre_unlock_text,
      post_unlock_text: textTemplate.post_unlock_text,
      rewards_type: 'free_gift',
      shipping_text: ''
    };
  }

  // Lazy-fetch + build the active market's gift tiers (cached per market).
  function loadMarketTiers(market, rate) {
    if (builtCache[market]) return Promise.resolve(builtCache[market]);
    var gifts = MARKET_GIFTS[market] || [];
    return Promise.all(gifts.map(function (g) {
      return fetch('/products/' + g.handle + '.js', { headers: { Accept: 'application/json' } })
        .then(function (r) { return r.ok ? r.json() : null; })
        .then(function (p) { return p ? buildTier(p, g, rate) : null; })
        .catch(function () { return null; });
    })).then(function (tiers) {
      tiers = tiers.filter(Boolean);
      builtCache[market] = tiers;
      return tiers;
    });
  }

  function tierSkus(t) {
    try {
      return JSON.parse(t.free_gifts).items.reduce(function (a, it) {
        return a.concat((it.variants || []).map(function (v) { return v.sku; }));
      }, []);
    } catch (e) { return []; }
  }
  function signature(arr) {
    return arr.map(function (t) {
      return (t.rewards_type === 'free_gift' ? tierSkus(t).join('+') + '@' + t.amount : (t.rewards_type + ':' + t.amount));
    }).join('|');
  }
  function clone(t) { var c = {}; for (var k in t) { if (Object.prototype.hasOwnProperty.call(t, k)) c[k] = t[k]; } return c; }

  function apply(giftTiers) {
    var st;
    try { st = window.SLIDECART_STATE(); } catch (e) { return; }
    if (!st || !st.settings || !Array.isArray(st.settings.rewards_tiers)) return;

    // Capture any NON free-gift reward tiers once, so we preserve them.
    if (nonGiftTiers === null) {
      nonGiftTiers = st.settings.rewards_tiers.filter(function (t) { return t.rewards_type !== 'free_gift'; });
    }

    var desired = nonGiftTiers.concat(giftTiers)
      .sort(function (a, b) { return parseFloat(a.amount) - parseFloat(b.amount); })
      .map(function (t, i) { var c = clone(t); c.tier = i + 1; return c; });

    if (signature(st.settings.rewards_tiers) === signature(desired)) return;   // idempotent
    st.settings.rewards_tiers = desired;
    busy = true;
    try { window.SLIDECART_UPDATE(function () { busy = false; }); } catch (e) { busy = false; }
  }

  function gate() {
    if (busy) return;
    var st;
    try { st = window.SLIDECART_STATE(); } catch (e) { return; }
    if (!st || !st.settings) return;
    captureTemplate(st);
    loadMarketTiers(getMarket(), currencyRate()).then(apply);
  }

  /* ---- 2. Hook Slide Cart lifecycle (chain existing) -------- */
  var pLoaded = window.SLIDECART_LOADED, pUpdated = window.SLIDECART_UPDATED, pOpened = window.SLIDECART_OPENED;
  window.SLIDECART_LOADED  = function (c) { if (typeof pLoaded  === 'function') { try { pLoaded(c); }  catch (e) {} } gate(); };
  window.SLIDECART_UPDATED = function (c) { if (typeof pUpdated === 'function') { try { pUpdated(c); }  catch (e) {} } gate(); };
  window.SLIDECART_OPENED  = function ()  { if (typeof pOpened  === 'function') { try { pOpened(); }   catch (e) {} } gate(); };

  /* ---- 3. Self-init if Slide Cart already loaded ------------ */
  (function poll(n) {
    if (typeof window.SLIDECART_STATE === 'function') { gate(); return; }
    if (n > 100) return;
    setTimeout(function () { poll(n + 1); }, 150);
  })(0);
})();
</script>
{% endraw %}
<!-- End of AMP Fix: Slide Cart market-based GWP (dynamic per-market load) — Beauty of Joseon Global -->
\`\`\`
- **Verified by Jall:** Yes

### [2026-06-24] UPDATED: Slide Cart Market-Based GWP (dynamic per-market load + auto-add)
- **Store URL:** beauty-of-joseon-global.myshopify.com
- **Issue:** GWP program needed to differ per Shopify Market (UK, US, EU, ROW) with correct currency conversion, auto-add/remove functionality, and prevention of Liquid token stripping.
- **Fix Description:** Implemented a sophisticated liquid snippet (`snippets/amp-slidecart.liquid`) that:
    1. Detects market via `window.Shopify.country`.
    2. Lazy-loads the corresponding gift products via `.js` endpoints.
    3. Injects reward tiers into `window.SLIDECART_STATE().settings.rewards_tiers`.
    4. **Auto-Add Logic**: Automatically adds/removes gifts via cart AJAX API based on unlocked tiers, hiding the native claim UI.
    5. **Progress Bar Fix**: Sets `rewards_final_total = true` to ensure the progress bar measures spend excluding the free gifts.
    6. Wrapped in `{% raw %}` to prevent Liquid processing.
- **Script:**
\`\`\`liquid
<!-- AMP Fix: Slide Cart market-based GWP (dynamic per-market load + auto-add) — Beauty of Joseon Global -->
{% raw %}
<script>
/* ============================================================
   AMP Fix — Beauty of Joseon Global — Market-based GWP (dynamic)
   Store: beauty-of-joseon-global.myshopify.com (Shopify Plus)

   WHAT THIS DOES
   1) Based on the shopper's active Shopify Market (window.Shopify.country),
      lazy-loads ONLY that market's gift product(s) and shows them as Slide
      Cart reward tiers — no cross-market overlap, nothing piled into the
      dashboard.
   2) AUTO-ADD: when a tier is reached the gift is added to the cart
      automatically and the "Free gift" claim section is hidden (no manual
      "Add" click). It AUTO-REMOVES a gift if the cart later drops below that
      tier, and it also removes any gift left over from a DIFFERENT market
      (e.g. after a market switch) so market discounts never collide.

   THRESHOLDS / CURRENCY
   `base` is the threshold in the store's BASE currency (USD); it is converted
   at runtime via Shopify.currency.rate, matching Shopify's auto-converted
   discount minimums. Example (GB, rate ~0.776): base 65 -> ~£50.45.

   WHY {% raw %}
   The unlock text uses {{ amount }} / {{ reward }} tokens. In a .liquid file
   Shopify would evaluate and strip them server-side; {% raw %} stops that.
   The label + unlock text are reused from your Slide Cart dashboard tier.

   DEPENDENCIES (outside this script)
   - Gift products must be "Continue selling when out of stock" (or in stock),
     or the add fails and checkout hits the stock-problems page.
   - The 100%-off is delivered by your Shopify automatic discounts (all-customer,
     cumulative). This script loads/adds the right gift; it does not discount.

   MAINTENANCE
   Edit MARKET_GIFTS (handle + USD threshold). EU = listed countries; ROW = rest.
   Set AUTO_ADD = false to instead show the manual "Add" claim UI.
============================================================ */
(function () {
  if (window.__ampMarketGwp) return;          // run once
  window.__ampMarketGwp = true;

  /* ---- 1. Per-market gifts (EDIT HERE) ----------------------
     handle = gift product URL handle
     base   = unlock threshold in USD (auto-converted to local currency) */
  var MARKET_GIFTS = {
    uk: [
      { handle: 'relief-sun-mini-10ml-copy',                  base: 1   }, // 82BU002
      { handle: 'uk-test-calming-serum-green-tea-panthenol',  base: 65  }, // 82BS008
      { handle: 'glow-deep-serum-rice-alpha-arbutin-copy-2',  base: 105 }  // 82BS032
    ],
    us:  [ { handle: 'day-dew-sunscreen-10ml-copy-1',         base: 1   } ], // 01BU015
    eu:  [ { handle: 'light-on-serum-mini-10ml-copy',         base: 1   } ], // 82BS019
    row: [ { handle: 'revive-eye-serum-mini-10ml-copy',       base: 1   } ]  // 82BS020
  };
  var EU_COUNTRIES = ['FR', 'DE', 'NL', 'BE', 'ES', 'IT', 'IE'];

  var AUTO_ADD = true;   // true = auto-add gift + hide claim UI; false = manual "Add" button

  // Fallback unlock text, used only if no dashboard free-gift tier is found.
  var DEFAULT_TEXT = {
    label: 'FREE item',
    pre_unlock_text: 'Spend {{ amount }} more and get *{{ reward }}*',
    post_unlock_text: '{{ reward }} applied!'
  };

  /* ---- internals ------------------------------------------- */
  var builtCache = {};        // market -> built tier array (fetched once)
  var nonGiftTiers = null;    // any non-free-gift reward tiers, preserved
  var textTemplate = null;    // label + unlock text reused from dashboard
  var busy = false;           // re-entrancy guard for tier re-render
  var reconciling = false;    // re-entrancy guard for gift add/remove
  var reconcileTimer = null;
  var failedAdds = {};        // gift variants that couldn't be added (e.g. sold out) — don't retry forever

  // Every gift handle across ALL markets — used to drop a gift left over from
  // another market (which would otherwise collide with this market's discount).
  var ALL_GIFT_HANDLES = Object.keys(MARKET_GIFTS).reduce(function (a, k) {
    return a.concat((MARKET_GIFTS[k] || []).map(function (g) { return g.handle; }));
  }, []);

  function getMarket() {
    var c = '';
    try { c = (window.Shopify && window.Shopify.country) ? String(window.Shopify.country).toUpperCase() : ''; } catch (e) {}
    if (c === 'GB') return 'uk';
    if (c === 'US') return 'us';
    if (EU_COUNTRIES.indexOf(c) !== -1) return 'eu';
    return 'row';
  }

  function currencyRate() {
    try {
      var r = parseFloat(window.Shopify && window.Shopify.currency && window.Shopify.currency.rate);
      return (r && r > 0) ? r : 1;
    } catch (e) { return 1; }
  }

  function captureTemplate(st) {
    if (textTemplate) return;
    var sources = [];
    if (st.settingsBackup && Array.isArray(st.settingsBackup.rewards_tiers)) sources = sources.concat(st.settingsBackup.rewards_tiers);
    if (Array.isArray(st.settings.rewards_tiers)) sources = sources.concat(st.settings.rewards_tiers);
    var gt = sources.filter(function (t) { return t && t.rewards_type === 'free_gift' && /\{\{/.test(t.pre_unlock_text || ''); })[0]
          || sources.filter(function (t) { return t && t.rewards_type === 'free_gift'; })[0];
    textTemplate = gt
      ? { label: gt.label, pre_unlock_text: gt.pre_unlock_text, post_unlock_text: gt.post_unlock_text }
      : DEFAULT_TEXT;
  }

  // Build a free-gift reward tier from a /products/<handle>.js payload.
  function buildTier(product, cfg, rate) {
    var v = product.variants && product.variants[0];
    if (!v) return null;
    var img = (product.featured_image || '').replace(/^\/\//, 'https://');
    var vImg = (v.featured_image && v.featured_image.src) ? v.featured_image.src : '';
    var localAmount = (parseFloat(cfg.base) * rate).toFixed(2);   // convert USD -> active currency
    var freeGifts = {
      discount_percentage: 100,
      items: [{
        id: 'gid://shopify/Product/' + product.id,
        handle: product.handle,
        image: img,
        title: product.title,
        variants: [{
          id: 'gid://shopify/ProductVariant/' + v.id,
          image: vImg, position: 1, sku: v.sku, title: v.title
        }]
      }]
    };
    return {
      tier: 1,
      amount: String(localAmount),
      free_gifts: JSON.stringify(freeGifts),
      label: textTemplate.label,
      pre_unlock_text: textTemplate.pre_unlock_text,
      post_unlock_text: textTemplate.post_unlock_text,
      rewards_type: 'free_gift',
      shipping_text: ''
    };
  }

  // Lazy-fetch + build the active market's gift tiers (cached per market).
  function loadMarketTiers(market, rate) {
    if (builtCache[market]) return Promise.resolve(builtCache[market]);
    var gifts = MARKET_GIFTS[market] || [];
    return Promise.all(gifts.map(function (g) {
      return fetch('/products/' + g.handle + '.js', { headers: { Accept: 'application/json' } })
        .then(function (r) { return r.ok ? r.json() : null; })
        .then(function (p) { return p ? buildTier(p, g, rate) : null; })
        .catch(function () { return null; });
    })).then(function (tiers) {
      tiers = tiers.filter(Boolean);
      builtCache[market] = tiers;
      return tiers;
    });
  }

  function tierSkus(t) {
    try {
      return JSON.parse(t.free_gifts).items.reduce(function (a, it) {
        return a.concat((it.variants || []).map(function (v) { return v.sku; }));
      }, []);
    } catch (e) { return []; }
  }
  function signature(arr) {
    return arr.map(function (t) {
      return (t.rewards_type === 'free_gift' ? tierSkus(t).join('+') + '@' + t.amount : (t.rewards_type + ':' + t.amount));
    }).join('|');
  }
  function clone(t) { var c = {}; for (var k in t) { if (Object.prototype.hasOwnProperty.call(t, k)) c[k] = t[k]; } return c; }

  function apply(giftTiers) {
    var st;
    try { st = window.SLIDECART_STATE(); } catch (e) { return; }
    if (!st || !st.settings || !Array.isArray(st.settings.rewards_tiers)) return;

    if (nonGiftTiers === null) {
      nonGiftTiers = st.settings.rewards_tiers.filter(function (t) { return t.rewards_type !== 'free_gift'; });
    }

    // Progress bar must measure spend on the FINAL total (gifts are £0), not the
    // pre-discount subtotal — otherwise an auto-added gift's original price
    // inflates the bar and a higher tier shows "unlocked" before it's earned.
    st.settings.rewards_final_total = true;

    var desired = nonGiftTiers.concat(giftTiers)
      .sort(function (a, b) { return parseFloat(a.amount) - parseFloat(b.amount); })
      .map(function (t, i) { var c = clone(t); c.tier = i + 1; return c; });

    if (signature(st.settings.rewards_tiers) === signature(desired)) return;   // idempotent
    st.settings.rewards_tiers = desired;
    busy = true;
    try { window.SLIDECART_UPDATE(function () { busy = false; }); } catch (e) { busy = false; }
  }

  /* ---- Auto-add / auto-remove gifts + hide the claim section ---- */
  function ensureGiftSectionHidden() {
    if (!AUTO_ADD || document.getElementById('amp-gwp-hide')) return;
    var s = document.createElement('style');
    s.id = 'amp-gwp-hide';
    s.textContent = '#slidecarthq [data-testid="FreeGifts"]{display:none !important;}';
    (document.head || document.documentElement).appendChild(s);
  }

  // The active market's gift tiers as { vid, cents (threshold in active currency) }.
  function managedGiftVariants() {
    var st;
    try { st = window.SLIDECART_STATE(); } catch (e) { return []; }
    if (!st || !st.settings || !Array.isArray(st.settings.rewards_tiers)) return [];
    return st.settings.rewards_tiers
      .filter(function (t) { return t.rewards_type === 'free_gift'; })
      .map(function (t) {
        try {
          var g = JSON.parse(t.free_gifts);
          var v = g.items[0].variants[0];
          return { vid: parseInt(String(v.id).split('/').pop(), 10), cents: Math.round(parseFloat(t.amount) * 100) };
        } catch (e) { return null; }
      })
      .filter(Boolean);
  }

  // Add gifts whose tier is unlocked; remove gifts whose tier is no longer met,
  // and remove gifts belonging to other markets. "Qualifying" total excludes
  // every gift line, and all decisions share that one rule, so they can't loop.
  function reconcileGifts() {
    if (!AUTO_ADD || reconciling) return;
    var gifts = managedGiftVariants();
    if (!gifts.length) return;
    reconciling = true;
    fetch('/cart.js', { headers: { Accept: 'application/json' } })
      .then(function (r) { return r.json(); })
      .then(function (cart) {
        var vids = gifts.map(function (g) { return g.vid; });
        var qualifying = (cart.items || [])
          .filter(function (i) { return ALL_GIFT_HANDLES.indexOf(i.handle) === -1; })
          .reduce(function (a, i) { return a + i.final_line_price; }, 0);
        var adds = [], removes = [];
        // 1) Drop any gift that belongs to a DIFFERENT market (stale / market switch).
        (cart.items || []).forEach(function (i) {
          if (ALL_GIFT_HANDLES.indexOf(i.handle) !== -1 && vids.indexOf(i.id) === -1) removes.push(i.key);
        });
        // 2) Add unlocked gifts; remove this market's gifts whose tier is no longer met.
        gifts.forEach(function (g) {
          var line = (cart.items || []).filter(function (i) { return i.id === g.vid; })[0];
          var unlocked = qualifying >= g.cents;
          if (unlocked && !line && !failedAdds[g.vid]) adds.push(g.vid);
          else if (!unlocked && line) removes.push(line.key);
        });
        if (!adds.length && !removes.length) { reconciling = false; return; }
        var chain = Promise.resolve();
        removes.forEach(function (key) {
          chain = chain.then(function () {
            return fetch('/cart/change.js', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ id: key, quantity: 0 }) });
          });
        });
        adds.forEach(function (vid) {
          chain = chain.then(function () {
            return fetch('/cart/add.js', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ id: vid, quantity: 1 }) })
              .then(function (r) { if (!r.ok) failedAdds[vid] = true; });   // sold out / not oversellable — stop retrying
          });
        });
        chain
          .then(function () { return new Promise(function (res) { try { window.SLIDECART_UPDATE(res); } catch (e) { res(); } }); })
          .then(function () { reconciling = false; })
          .catch(function () { reconciling = false; });
      })
      .catch(function () { reconciling = false; });
  }
  function scheduleReconcile() {
    if (!AUTO_ADD) return;
    clearTimeout(reconcileTimer);
    reconcileTimer = setTimeout(reconcileGifts, 350);
  }

  function gate() {
    if (busy) return;
    var st;
    try { st = window.SLIDECART_STATE(); } catch (e) { return; }
    if (!st || !st.settings) return;
    ensureGiftSectionHidden();
    captureTemplate(st);
    loadMarketTiers(getMarket(), currencyRate()).then(function (tiers) { apply(tiers); scheduleReconcile(); });
  }

  /* ---- 2. Hook Slide Cart lifecycle (chain existing) -------- */
  var pLoaded = window.SLIDECART_LOADED, pUpdated = window.SLIDECART_UPDATED, pOpened = window.SLIDECART_OPENED;
  window.SLIDECART_LOADED  = function (c) { if (typeof pLoaded  === 'function') { try { pLoaded(c); }  catch (e) {} } gate(); scheduleReconcile(); };
  window.SLIDECART_UPDATED = function (c) { if (typeof pUpdated === 'function') { try { pUpdated(c); }  catch (e) {} } gate(); scheduleReconcile(); };
  window.SLIDECART_OPENED  = function ()  { if (typeof pOpened  === 'function') { try { pOpened(); }   catch (e) {} } gate(); scheduleReconcile(); };

  /* ---- 3. Self-init if Slide Cart already loaded ------------ */
  (function poll(n) {
    if (typeof window.SLIDECART_STATE === 'function') { gate(); scheduleReconcile(); return; }
    if (n > 100) return;
    setTimeout(function () { poll(n + 1); }, 150);
  })(0);
})();
</script>
{% endraw %}
<!-- End of AMP Fix: Slide Cart market-based GWP (dynamic per-market load + auto-add) — Beauty of Joseon Global -->
\`\`\`
- **Verified by Jall:** Yes

### [2026-06-26] Slide Cart Drawer Not Rendering (Overlay Only)
- **Store URL:** staging-workoutmeals.myshopify.com
- **Issue:** The page goes dark (theme overlay appears) when clicking the cart icon, but the Slide Cart drawer does not render. This was caused by `SLIDECART_STATE().settings.enabled` being `null` and the theme's native drawer state blocking interaction.
- **Fix Description:** Forced `SLIDECART_STATE().settings.enabled` to `true` using a polling mechanism and intercepted theme cart triggers to clear theme overlay classes and trigger `window.SLIDECART_OPEN()`.
- **Script:**
\`\`\`javascript
(function () {
  if (window.__ampSlideCartFix) return;
  window.__ampSlideCartFix = true;

  var slidecartReady = false;
  var pendingOpen = false;

  // Theme triggers that should open Slide Cart instead of the theme's own (empty) cart drawer.
  var CART_TRIGGER_SELECTOR =
    '.js-drawer-open-button-right, #cart-icon-bubble, .header-cart, .btn-to-drawer';

  // This store ships with Slide Cart's internal setting "enabled" === null, which makes the
  // drawer render nothing (the React app mounts but returns null). Force it true so it renders.
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
    // Clear any theme cart-drawer state (the page "fade") if the theme toggled it first.
    document.body.classList.remove('js-drawer-open', 'active-pop-up');
    ensureEnabled();
    if (slidecartReady && typeof window.SLIDECART_OPEN === 'function') {
      window.SLIDECART_OPEN();
    } else {
      pendingOpen = true; // queued: fires the moment Slide Cart finishes loading
    }
  }

  // Capture phase so we run BEFORE the theme's native cart-drawer handlers and link navigation.
  document.addEventListener('click', function (e) {
    var trigger = e.target.closest && e.target.closest(CART_TRIGGER_SELECTOR);
    if (!trigger) return;
    e.preventDefault();
    e.stopImmediatePropagation();
    openSlideCart();
  }, true);

  // Chain SLIDECART_LOADED (don't overwrite) — enable + flush any queued open once ready.
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

  // Re-assert "enabled" on every open in case the app resets it.
  var prevOpened = window.SLIDECART_OPENED;
  window.SLIDECART_OPENED = function () {
    ensureEnabled();
    if (typeof prevOpened === 'function') { try { prevOpened(); } catch (e) {} }
  };

  // Safety net: if the snippet runs before Slide Cart loads, poll briefly to set the flag early.
  var tries = 0;
  var poll = setInterval(function () {
    tries++;
    if (typeof window.SLIDECART_OPEN === 'function') slidecartReady = true;
    var ok = ensureEnabled();
    if ((ok && slidecartReady) || tries > 60) clearInterval(poll); // ~6s max
  }, 100);
})();
\`\`\`
- **Verified by Jall:** Yes

### [2026-06-26] Restore Original Compare-at Price for Subscriptions in Slide Cart
- **Store URL:** osenra.com
- **Issue:** When Kaching "Automatic Refills" (or similar subscription plans) are applied, Shopify's Cart API sets `selling_plan_allocation.compare_at_price` to the one-time price instead of the variant's actual compare-at price. This causes Slide Cart to show a reduced savings amount.
- **Fix Description:** Intercept `SLIDECART_UPDATED`, fetch product JSON to calculate the `compare_at_price / price` ratio for the variant, and apply this ratio to the presentment `compare_at_price` in the cart. This ensures the correct strikethrough price is displayed across all currencies/markets.
- **Script:**
\`\`\`javascript
(function () {
  var ratioCache = {}; 
  var inFlight = {};   
  var TOL = 2;         
  window.__ampCompareGuardBusy = false;

  function loadProduct(handle) {
    if (inFlight[handle]) return inFlight[handle];
    inFlight[handle] = fetch('/products/' + handle + '.js')
      .then(function (r) { return r.json(); })
      .then(function (p) {
        (p.variants || []).forEach(function (v) {
          ratioCache[v.id] = (v.compare_at_price && v.price)
            ? (v.compare_at_price / v.price)
            : null;
        });
        return p;
      })
      .catch(function () { return null; });
    return inFlight[handle];
  }

  window.SLIDECART_UPDATED = function (cart) {
    if (window.__ampCompareGuardBusy) return;
    if (!cart || !cart.items) return;

    var pending = [];
    cart.items.forEach(function (it) {
      if (!it.selling_plan_allocation) return;
      if (!ratioCache.hasOwnProperty(it.variant_id)) pending.push(loadProduct(it.handle));
    });

    Promise.all(pending).then(function () {
      var changed = false;
      cart.items.forEach(function (it) {
        var spa = it.selling_plan_allocation;
        if (!spa) return;
        var ratio = ratioCache[it.variant_id];
        if (!ratio) return;
        var target = Math.round(spa.compare_at_price * ratio);
        if (target && Math.abs((spa.compare_at_price || 0) - target) > TOL) {
          spa.compare_at_price = target;
          it.compare_at_price = target;
          changed = true;
        }
      });
      if (changed) {
        window.__ampCompareGuardBusy = true;
        window.SLIDECART_SET_CART(cart);
        setTimeout(function () { window.__ampCompareGuardBusy = false; }, 50);
      }
    });
  };
})();
\`\`\`
- **Verified by Jall:** Yes
