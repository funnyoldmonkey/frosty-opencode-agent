# CS Agent Handbook
 
Your guide to handling Amp support tickets using the knowledge base. Read this once during onboarding; refer back when you need a reminder. The Quick Reference section at the bottom is what you'll actually use day-to-day.
 
## What this is
 
A working knowledge base of every documented Amp support fix across Slide Cart, BIS, Bundles, and Lifetimely. The previous T2 team built up around 300 fix docs over the years; all of them are now catalogued and searchable. You'll be using Claude to triage incoming tickets — paste the ticket, get back a draft reply grounded in a real past fix, polish it, ship.
 
The goal is two to three minutes per ticket instead of twenty. You stay the one who decides what goes to the merchant; Claude does the search and the first draft.
 
## Getting started
 
You'll work inside a Claude.ai project that your CS lead set up. Everything you need is loaded as project knowledge — the catalog, the legacy archive, the API reference, the company context. You don't need to install anything.
 
A normal ticket flow looks like this:
 
1. Open the Amp Support project in Claude.ai (your CS lead will share the link).
2. Start a new conversation.
3. Paste the merchant's ticket in full — including any video or screenshot links and what previous agents already tried.
4. Ask Claude to find the fix and draft a reply. Good prompts are listed below.
5. Read the draft carefully. Adapt theme-specific selectors or paths to this merchant's actual store. Match your normal voice for the sign-off.
6. Paste into Helpscout and send.
Step five is where most agents get into trouble. Claude pulls fixes from the catalog, but the catalog's heuristic classification gets the theme right about 85% of the time — meaning roughly one in seven fixes will need the selector or file path swapped before it works. Don't skip the review.
 
## The triage flow
 
Knowing what Claude is doing under the hood helps you spot when it's going off-track.
 
When Claude follows the playbook, it identifies the basics first — which Amp app is involved, what theme the merchant is on, what category the issue falls into (cart-redirect, styling, upsell config, notification setup, etc.). If any of those aren't clear from the ticket, it should ask you rather than guessing. If you notice Claude proceeding without asking when the ticket is ambiguous, stop it and clarify.
 
Next, Claude searches the catalog by app, theme, and tag, pulling the top one to three candidate fixes. It then reads each candidate file in full — this is non-negotiable. The catalog row is a summary; the file is the source of truth. If a fix doesn't apply, Claude should say so. If you spot Claude quoting a catalog summary without reading the actual file, ask: *"Did you read the file or just the catalog row?"*
 
Finally, Claude drafts a reply with four parts: an accurate acknowledgement of the issue, a one-or-two-sentence explanation of the cause, the fix (code or steps), and what the merchant should expect after applying it. If any of those four parts is missing, push back and ask Claude to fill it in.
 
## How to prompt Claude well
 
These prompts work:
 
- *"Here's a ticket [paste full ticket]. Find the relevant fix from the catalog and draft a reply."*
- *"The merchant is on the Impulse theme. They report the cart icon redirects to /cart on tap. What's our documented fix and is it different for mobile vs desktop?"*
- *"Is there a documented fix for this exact symptom: [paste]? If yes, give me the code. If no, say so explicitly — I'll escalate."*
These produce worse results:
 
- *"What should I tell this merchant?"* — Too vague, Claude will guess.
- *"Fix this for me."* — Without ticket context, Claude doesn't know what "this" is.
- *"Write a generic CSS fix for cart drawers."* — Don't ask for generic. Ask for the specific documented fix that matches the theme.
The pattern that works: be specific about the symptom, the theme, the platform (mobile vs desktop), and what you've already tried. Treat Claude like a colleague who didn't see the ticket — give it context, not commands.
 
## When Claude drafts code (verified vs. invented)
 
Claude won't always find an exact match in the catalog. For novel issues, Claude can draft code based on related fix docs, the Slide Cart JS API reference, and standard Shopify patterns. Your job is to test before sending — see the next section.
 
The critical rule: **Claude must label what's documented versus invented.** A good draft starts with something like *"This is adapted from `fixes/cart-icon-redirects-to-cart-page-on-mobile-refresh.md` and the SLIDECART_LOADED API — it hasn't been verified on this exact theme. Test before sending."* If Claude gives you code with no provenance, push back: *"What did you base this on? Cite the source — catalog row, API ref, or general pattern."*
 
Three categories of Claude output you'll see:
 
- **Verified fix** — pulled directly from a curated or legacy doc with no substantive changes. Lower testing burden; the previous team validated it on a real store.
- **Adapted fix** — based on a documented fix but with theme-specific selectors, file paths, or variable names swapped to match this merchant's theme. Test the swaps; the structure is sound.
- **Invented fix** — no exact doc match, drafted from the API reference and general patterns. Highest testing burden. Treat it as a starting point, not a final answer.
The honest answer remains valid: if Claude can't draft something it has reasonable confidence in, *"no fix in our knowledge base matches and the standard patterns don't apply cleanly — recommend escalating"* is better than an invented snippet held together with hope.
 
## What Claude should never do
 
A few things stay off-limits regardless of confidence level.
 
If Claude claims a behavior is "intended" when it's a known race condition or bug, double-check against the catalog before accepting that. The previous team made this exact mistake on the mobile cart refresh issue — the answer in the catalog is now precise about it being a race condition, not intended behavior.
 
If Claude promises a product change or a refund on the company's behalf, strip those lines from the draft. Those are commitments only the lead or Anoop can make.
 
If Claude gives the same generic styling fix for very different theme contexts, that's a red flag — themes have different DOM structures, so a CSS selector that works for Dawn won't work for Minimog. If Claude doesn't say which theme its fix is scoped to, ask before sending.
 
If Claude drafts code that touches checkout flow, payments, billing, or anything requiring live deployment to the merchant's store (collaborator access, theme code published live, etc.), escalate to tech team. The blast radius of a broken checkout for a Plus merchant is much larger than what CS should absorb to save tech-team time.
 
## Testing protocols
 
"Test before sending" means different things for different fix categories. Use this as your testing checklist — match the protocol to the riskiest part of the code Claude gave you.
 
**CSS-only fixes** (color, font, padding, layout tweaks, no JavaScript). Lowest risk. Open the merchant's storefront in your browser, open DevTools, paste the CSS into the Styles pane on the target element. Confirm it does what the merchant wants without breaking adjacent elements. Five-minute test. If it works in DevTools, it'll work when pasted into the theme.
 
**JS that touches the cart drawer but not checkout** (SLIDECART_OPEN, SLIDECART_UPDATE, cart-icon click interception, drawer styling, upsell display). Medium risk — can break the drawer itself but won't lose money. Get a Shopify theme preview link if you have collaborator access, or ask the merchant to duplicate their live theme and apply the change to the copy. Test the specific user flow the fix addresses (e.g., refresh + quick tap on mobile for the cart-redirect race fix). Test one adjacent flow too — adding an item to cart, opening the drawer normally — to confirm you haven't broken something else.
 
**JS that uses the Slide Cart API but on a non-standard flow** (programmatic discount application, custom triggers, third-party app integrations). Medium-high risk. Same protocol as the drawer category, but explicitly test the integration point with the third-party app or custom flow before sending. Read `slide-cart-api.md` to confirm the API methods Claude used actually exist and accept the arguments Claude passed them.
 
**Anything touching ATC button behavior across the storefront** (overriding theme ATC handlers, custom add-to-cart flows). High risk. Test on a preview theme. Add to cart from at least three places — product page, collection page, quick-add — to confirm the fix doesn't break any of them. The previous team had repeated tickets where an ATC fix worked on the product page but broke quick-add on collections.
 
**Anything that touches checkout, payments, billing, or live deployment.** Don't test, escalate. This is not where CS should be experimenting.
 
If a fix Claude drafted breaks during testing, don't try to debug it yourself — escalate to tech team and flag it to the CS lead. A broken fix in the field is the kind of thing that turns into a Helpscout escalation; better to catch it in your testing.
 
## Reading a fix doc
 
Fix docs come in two formats and you'll see both.
 
**Legacy format** lives in `T2 docs/` and is what the previous team wrote — a Description section and a Solution section, often with code blocks but sometimes referencing screenshots that didn't transfer cleanly. Short and direct but inconsistent. Around 300 docs are in this format.
 
**Template format** lives in `fixes/` and is the new standard — structured into Symptom / Cause / Solution / Code / Scope / Merchant-ready reply / Related sections, with YAML frontmatter on top. Easier to read and easier to extract from. Only a few docs are in this format today; the count grows as the team converts legacy docs lazily.
 
For legacy docs, expect to read both sections in full. If the doc references screenshots for the actual code, you may need to escalate or look at the original Notion source — sometimes critical code lived only in images that didn't survive the export.
 
## Adapting code to the merchant
 
The fix doc gives you code. Almost never paste it as-is — selectors, IDs, class names, and file paths vary per theme. The things to check before sending:
 
CSS selectors for the cart icon often need swapping. The fix might use `#cart-icon-bubble` (Dawn) but the merchant is on Impulse where it's `.cart-link`. Use DevTools on the merchant's actual store to grab the right selector. If you don't have collaborator access yet, you can still inspect the public store.
 
File paths differ by theme version. Older themes have `theme.js`; newer ones have a `theme.dev.js` (the source) plus a minified `theme.js` (the deployed version) — edits go in `theme.dev.js` and need to be minified back. If the fix doc references one but the merchant has the other, adjust the instructions.
 
Variable names in JavaScript snippets can collide with the merchant's existing custom code. If a snippet declares `var slidecartReady` and the merchant happens to have another `slidecartReady` somewhere, things break. Wrap snippets in an IIFE pattern — `(function () { ... })()` — if they aren't already. Most of our newer fix docs do this; older ones may not.
 
If you're not confident which selector to use, ask Claude to walk you through the inspection. Paste the merchant's store URL and ask: *"Based on the Impulse theme structure, which selector should I use for the cart icon in this fix?"* Claude can reason about the standard theme DOM even without scraping the live site.
 
## Drafting the merchant reply
 
Match the CS team's voice — warm, direct, no jargon padding. Read a few of your team's recent Helpscout replies if you're new and need calibration.
 
A good reply has four parts. First, acknowledge the issue accurately — *"You've spotted a real edge case"* beats *"this is intended behavior"* every time. Merchants notice precision. Second, explain the cause in one sentence. Most merchants don't want the full diagnosis, but giving them a one-line cause prevents the follow-up question. Third, give the fix clearly — code block, file paths, line ranges. Specifics save back-and-forth. Fourth, set expectations — *"After publishing, the cart icon will open the drawer even on a fast tap"* — so the merchant knows what success looks like and doesn't ping you with *"is it working?"* an hour later.
 
Don't sign as "the team." Sign with your name, the way you normally would. Claude's drafts don't include a signature so you can add your own.
 
## When to escalate (and not use Claude)
 
Some tickets shouldn't run through Claude at all. Escalate to tech team or hand back to a senior agent when:
 
The merchant is on a fully custom theme that doesn't match any documented fix. Heuristic selectors won't work and there's real risk of breaking their store.
 
The fix requires running code directly on the merchant's store — collaborator access, theme copy creation, code deployment, etc. That's tech team work. Claude can help you understand *what* the fix is, but the application step is human and needs Shopify access.
 
The merchant is angry, has compounding issues across multiple tickets, or is threatening to uninstall. Those need a human voice and judgement. Claude's drafts are competent but not calibrated for de-escalation.
 
The issue touches billing, refunds, plan changes, or anything contractual. Don't let Claude commit to those.
 
For each of these, paste the ticket and your initial assessment into the right channel and tag the right person.
 
## When you find a new fix
 
If you solve a ticket whose fix isn't already in the catalog, you've made the knowledge base richer — but only if you write it down before the context fades. While the fix is fresh:
 
1. Open `_template-fix.md` and copy it.
2. Save as `fixes/<short-descriptive-name>.md`. Use kebab-case, no spaces, no special characters.
3. Fill in the YAML frontmatter — title, app, themes, tags, severity, date, your name.
4. Fill in the body — Symptom, Cause, Solution, Code, Scope, Merchant-ready reply, Related.
5. Add a row to `catalog.md` under the relevant app's Curated fixes section.
6. Tell the CS lead. They'll upload the new file to the Claude.ai project at the next sync.
Don't skip this even if the fix felt small. The whole point of this project is that the next agent doesn't have to solve the same problem twice. Ninety seconds of writing now saves thirty minutes of debugging the next time the ticket comes in.
 
## Troubleshooting
 
**Claude says "no documented fix matches" but the issue feels familiar.** Don't accept this at face value. Try rephrasing the symptom — *"cart drawer doesn't open"* might miss what *"cart icon redirects"* finds. Search the catalog directly by keyword or tag. If you find a likely candidate, point Claude at the specific file: *"Read fixes/cart-icon-redirects-to-cart-page-on-mobile-refresh.md and tell me whether it applies to this ticket."*
 
**Claude gives code that doesn't work in your test.** Stop and don't send it. Two cases: if Claude pulled the code from a documented fix doc, the doc may have a typo or the merchant's theme has diverged since it was written — flag the broken doc to the CS lead so it gets corrected. If Claude invented the code from scratch, that's the testing step doing its job. Escalate to tech team for a verified solution, and ask Claude to add a note to the catalog flagging this pattern as "tried in [ticket #], didn't work for [theme]" — that prevents the next agent from trying the same dead-end.
 
**Claude pulls a fix for a different theme than the merchant has.** The catalog's theme detection misclassified — it happens around 15% of the time. Tell Claude the merchant's actual theme and ask it to search again. If no theme-matched fix exists, escalate or apply a generic fix with a note to the merchant that it's untested for their theme.
 
**The catalog has too many results for one tag.** Use multiple tags together. *"Show me cart-redirect fixes that also have the theme-js tag"* narrows from twenty to five results.
 
**A fix doc references a screenshot you can't see.** This happens with legacy docs whose images didn't survive the Notion export. Tell the lead — the doc needs to be backfilled or the missing code needs to be recovered. In the meantime, escalate the ticket.
 
## Quick reference
 
| When you want to... | Open this |
|---|---|
| Find a documented fix | `catalog.md` |
| Get Amp product / company context | `amp-context.md` |
| Look up a Slide Cart JS API call | `slide-cart-api.md` |
| Document a new fix you just solved | Copy `_template-fix.md` into `fixes/` |
| Read this guide again | `cs-agent-handbook.md` |
| Find the full legacy archive | `T2 docs/` folder |
| Read about how the project is maintained | `cs-lead-handbook.md` (CS lead's file) |
 
Prompt patterns that work, copy-paste ready:
 
> *Here's a ticket [paste]. Search the catalog and draft a reply. Label the code as verified, adapted, or invented — I'll match the testing protocol to that.*
 
> *Merchant is on the [theme name] theme reporting [symptom]. Adapt our documented fix to their theme, and call out any selector or path swaps that need verification.*
 
> *Read `fixes/[file].md` and tell me whether it applies to this ticket: [paste]. If not, draft a new fix from the API reference and the closest related docs.*
 
> *No exact match for [symptom] in the catalog. Draft a candidate fix from `slide-cart-api.md` and similar patterns, and tell me which parts are highest risk to test.*
 
That's the whole flow. Claude drafts, you test, you ship — or you escalate when the testing protocol calls for it.