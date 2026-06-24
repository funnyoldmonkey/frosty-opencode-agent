---
name: bis-proxy-path-rewrite
description: Fixes BIS 404 errors caused by a mismatch between the client-side proxy path and the registered Shopify App Proxy subpath.
---

## Problem
The Back in Stock (BIS) app client is often hardcoded to send requests to `/apps/bis/`. However, in some Shopify store installations, the App Proxy is registered under a different subpath (e.g., `/apps/backinstock/`). 

When this mismatch occurs, any request to the "wrong" path returns a Shopify 404 HTML page. Because the BIS app expects a JSON/JS response (JSONP), the script load fails (`net::ERR_ABORTED 404`), and the "Notify me when available" button does nothing.

## Workflow
1. **Identify the Mismatch:**
   - Open the Network tab in Chrome DevTools.
   - Trigger a BIS signup submission.
   - Look for the failed request (404) to `/apps/bis/signups/create.json`.
   - Test alternative paths (e.g., `/apps/backinstock/signups/create.json`) via the browser or `fetch` to find the working proxy path.

2. **Implement the Proxy Rewrite:**
   - Define the `WRONG` path (`/apps/bis/`) and the `RIGHT` path (the working one).
   - Monkey-patch `window.BIS.request` and `window.BIS.requestJSONP`.
   - Intercept the URL argument and replace the wrong subpath with the right one before the original request function is called.
   - Use a flag (e.g., `__ampProxyPatched`) to ensure the patch is idempotent.

3. **Handle Asynchronous Initialization:**
   - Since `window.BIS` may be initialized after the fix script runs, implement a polling mechanism (e.g., `setInterval`) that attempts to apply the patch every 200ms until successful or a safety timeout is reached.

## Verification
1. **Network Check:** Trigger a signup and verify the request URL now uses the `RIGHT` path.
2. **Status Check:** Ensure the response status is `200 OK` and the response body contains the expected success message.
3. **UI Check:** Verify the BIS modal correctly displays the success state to the user.
