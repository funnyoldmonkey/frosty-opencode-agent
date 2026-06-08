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

### [2026-06-08] Slide Cart German Translation
- **Store URL:** https://bomique.nl/
- **Issue:** Slide Cart content appearing in Dutch when German language is selected.
- **Fix Description:** Implemented a targeted translation script with a debounced MutationObserver to translate specific reward, shipping, and item count strings while preserving bold formatting.
- **Script:**
\`\`\`javascript
(function() {
  const isGerman = document.documentElement.lang === 'de' || window.Shopify?.locale === 'de';
  if (!isGerman) return;

  const translations = {
    'Verzekerde verzending': 'Versicherter Versand',
    'Verzekerde Verzending': 'Versicherter Versand',
    'tegen schade, verlies & diefstal': '<strong>Schutz bei Beschädigung, Verlust & Diebstahl</strong>',
    'Tegen schade, verlies & diefstal': '<strong>Schutz bei Beschädigung, Verlust & Diebstahl</strong>',
    'Nog één item voor Gratis verzending!': 'Nur noch ein Artikel bis zum <strong>kostenlosen Versand</strong>!',
    'Gratis verzending toegepast!': '<strong>Kostenloser Versand</strong> aktiviert!',
    'Gratis verzending': 'KOSTENLOSER VERSAND'
  };

  const translateCart = () => {
    const cart = document.querySelector('#slidecarthq');
    if (!cart) return;

    cart.querySelectorAll('.rewards-tiers-labels-item-amount').forEach(el => {
      const text = el.innerText;
      if (text.includes('items')) {
        const newText = text.replace(/\d+\s*items/, (match) => match.replace('items', 'Artikel'));
        if (el.innerText !== newText) el.innerText = newText;
      }
    });

    const allElements = cart.querySelectorAll('p, span, div, strong');
    allElements.forEach(el => {
      if (el.children.length === 0 && el.innerText.trim()) {
        const text = el.innerText.trim();
        for (const [oldText, newText] of Object.entries(translations)) {
          if (text === oldText) {
            if (el.innerHTML !== newText) el.innerHTML = newText;
            break;
          }
        }
      }
    });

    const containers = ['.rewards-pre-unlock-text', '.rewards-post-unlock-text', '.shipping-protection-description'];
    containers.forEach(selector => {
      cart.querySelectorAll(selector).forEach(container => {
        const text = container.innerText.trim();
        for (const [oldText, newText] of Object.entries(translations)) {
          if (text === oldText) {
            if (container.innerHTML !== newText) container.innerHTML = newText;
            break;
          }
        }
      });
    });
  };

  const initTranslation = () => {
    const cart = document.querySelector('#slidecarthq');
    if (!cart) return;

    translateCart();

    const observer = new MutationObserver(() => {
      clearTimeout(window.ampTranslationTimeout);
      window.ampTranslationTimeout = setTimeout(() => {
        translateCart();
      }, 100);
    });

    observer.observe(cart, { childList: true, subtree: true });
  };

  if (document.readyState === 'complete') {
    initTranslation();
  } else {
    window.addEventListener('load', initTranslation);
  }
})();
\`\`\`
- **Verified by Jall:** Yes


