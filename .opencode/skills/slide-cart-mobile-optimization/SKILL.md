---
name: slide-cart-mobile-optimization
description: Optimize Slide Cart mobile layout by reducing whitespace, fixing horizontal overflow, and aligning reward tier icons.
---

# Slide Cart Mobile Layout Optimization

This skill outlines the process for reducing excessive whitespace and fixing layout glitches (like horizontal scrolling and icon misalignment) in the Slide Cart mobile view.

## Workflow

### 1. Identify Whitespace Culprits
- Use Chrome DevTools to inspect the `.slidecarthq.right` drawer.
- Check computed styles for `.header`, `.rewards`, and `.footer`.
- Look for large `padding` or `margin` values that create empty gaps.

### 2. Reduce Header & Footer Padding
- Apply reduced padding to `.header` (e.g., `10px`) to reclaim space while keeping the close button visible.
- Minimize `.footer` padding.
- Identify redundant footer rows (e.g., Discount rows) and hide them using `:not(.amp-sc__footer-row--subtotal) { display: none !important; }` to ensure only the Total remains.

### 3. Fix Horizontal Overflow
- If the rewards section or the drawer itself allows horizontal scrolling:
  - Inspect the `.rewards-tiers` container.
  - Apply `overflow-x: clip !important` to `#slidecarthq` and `#slidecarthq .rewards` to prevent the layout from shifting horizontally on small screens.

### 4. Align Reward Tier Icons
- If icons are cut off or offset on mobile:
  - Target `.rewards-tiers-item-icon`.
  - Use `transform: translateX(-43px) !important` (or a similar value based on the specific theme/width) to center the icons over their respective labels.

### 5. Refine Label Positioning
- To optimize the vertical space in the rewards section:
  - Nudge the "X items" label up: `.rewards-tiers-labels-item-amount { transform: translateY(-15px) !important; }`.
  - Nudge the "X% off" label down: `.rewards-tiers-labels-item-label { transform: translateY(15px) !important; }`.

## Verification
- Emulate a mobile device (max-width: 750px).
- Verify no horizontal scrollbars appear.
- Ensure the close button is still accessible.
- Confirm reward icons are perfectly centered over labels.
- Check that the footer is compact and only shows the Total.
