---
name: slidecart-impulse-mobile-fix
description: Fix Slide Cart being shifted off-screen and sizing issues on the Impulse theme on mobile.
---

# Slide Cart Impulse Mobile Fix

On the Impulse theme, the Slide Cart drawer may remain off-screen on mobile even when the 'open' class is applied, due to a 	ransform: translateX or matrix property. Additionally, it may not fill the full width of the viewport.

## Troubleshooting Steps

1. **Diagnose Transform Issue**
   - Open the store on mobile (375px).
   - Trigger the cart and check if .slidecarthq has the open class.
   - Inspect computed styles for 	ransform. If it is matrix(1, 0, 0, 1, 375, 0) or similar, the drawer is shifted off-screen.

2. **Check Width/Height**
   - Verify if the drawer has an inline style (e.g., width: 80%) that prevents it from filling the screen.

## Implementation

Inject the following CSS into the App Custom CSS or 	heme.liquid:

`css
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
`

## Verification
- [ ] Slide Cart opens and is visible on mobile.
- [ ] Slide Cart fills 100% of the viewport width and height.
