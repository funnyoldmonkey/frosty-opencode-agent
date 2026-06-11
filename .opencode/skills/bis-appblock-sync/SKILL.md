---
name: bis-appblock-sync
description: Handle conflicts between custom integration scripts and BIS App Blocks, ensuring consistent variant sync and modal triggers.
---

# BIS App Block Sync Workflow

Use this skill when a store has both an App Block and a custom integration script for the Back in Stock app, causing "button wars" (infinite ID compounding), inconsistent visibility, or modals that won't open.

## Diagnosis Pattern
1. Check for buttons with IDs starting with `BIS_trigger-` (timestamped). This indicates an App Block is active.
2. Verify if `BIS.detectVariant` returns the correct ID after a variant switch. If not, the app's internal detection is broken.
3. Check if `BIS.popup.show(variantId)` is the available method to open the modal, rather than manipulating the iframe DOM.

## Implementation Steps

1. **Avoid DOM Deletion**: Never remove buttons with `id^="BIS_trigger"`. Instead, use a selector that matches any of them: `document.querySelector('[id^="BIS_trigger"]')`.
2. **Implement a Sync Heartbeat**:
   - Use `setInterval` (e.g., 500ms) to constantly check for the button.
   - If no button exists, create a fallback.
   - Always update the `data-variant-id` attribute of the button to match the currently checked radio button (`input[type="radio"]:checked[data-option-value-id"]`).
3. **Fast-Track Variant Changes**: Attach a `change` event listener to the product form to trigger the sync immediately, reducing the perceived lag of the interval.
4. **Capture Phase Click Interception**:
   - Use `document.addEventListener('click', handler, true)` (capture phase).
   - Use `.closest('[id^="BIS_trigger"]')` to find the trigger.
   - Execute the trigger sequence:
     1. `BIS.popup.form.selectVariant(vid)`
     2. `BIS.popup.show(vid)`

## Verification
- Switch variants rapidly and ensure the button visibility and `data-variant-id` update.
- Click the button for multiple variants and verify the modal opens with the correct variant selected.
