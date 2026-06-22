---
name: bis-webpush-init-fix
description: Fixes TypeError 'askPermission' of null in BIS modal when webpush is default channel
---

## Problem
When the Back in Stock (BIS) app is configured with "webpush" as the default notification channel, the `selectDefaultChannel()` method in the app's JS updates the channel state but fails to initialize the `bisWebpush` instance. This causes a crash in `handleSubmit()`: `Uncaught TypeError: Cannot read properties of null (reading 'askPermission')`.

## Workflow
1. **Identify the issue**: Check console for the `askPermission` TypeError upon BIS modal submission.
2. **Verify BIS location**: Confirm `window.BIS` exists on the main window object.
3. **Inject Patch**:
   Apply the following script to the store (e.g., via theme.liquid or a custom JS asset):
   \`\`\`javascript
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
   \`\`\`
4. **Verify**: Submit the BIS modal with webpush selected and ensure no console errors occur.

## Verification
- Open the product page.
- Trigger the BIS modal.
- Ensure "Notificaciones del navegador" (Webpush) is selected.
- Click "Notificarme".
- Confirm the notification is registered without a JS crash.
