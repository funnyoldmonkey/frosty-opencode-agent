---
name: alpine-dom-override
description: Handle cases where Alpine.js or other reactive frameworks override app-injected DOM changes.
---

# Skill: Alpine.js DOM Override Fix

## Problem
Modern Shopify themes using Alpine.js or Vue often use reactive templates that rewrite the inner HTML of elements (like the Add to Cart button) whenever a state change occurs (e.g., variant selection). This wipes out any modifications made by AMP scripts.

## Workflow

### 1. Identification
- Use `evaluate_script` to check if the element is being modified by a framework.
- Look for `x-data`, `x-if`, or `x-text` attributes in the DOM.
- Observe the button text changing back to default immediately after a script modification.

### 2. Implementation
- Use a `MutationObserver` targeting the parent element of the reactive content.
- Set `subtree: true` and `childList: true` to catch internal template re-renders.
- Inside the observer callback, re-apply the desired modification (text change, class addition, etc.).

### 3. Code Pattern
\`\`\`javascript
const target = document.querySelector('.reactive-element');
if (target) {
  const applyFix = () => {
    // Your modification logic here
    const span = target.querySelector('span');
    if (span && span.textContent !== 'Desired Text') {
      span.textContent = 'Desired Text';
    }
  };
  const observer = new MutationObserver(() => applyFix());
  observer.observe(target, { childList: true, subtree: true, characterData: true });
  applyFix();
}
\`\`\`

### 4. Verification
- Change variants to trigger a re-render.
- Confirm the modification persists.
- Take screenshots of both states.
