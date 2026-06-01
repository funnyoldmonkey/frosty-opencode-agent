# AMP Context Folder

This folder contains reference material for AMP (useamp.com) Shopify App troubleshooting. Frosty reads ALL files in this folder on startup.

## How This Folder Works

- **Jall adds** `.md` files here with AMP-related context: docs, notes, client-specific info, edge cases, etc.
- **Frosty maintains** `verified-fixes.md` — a growing log of confirmed fixes that helps resolve similar issues faster.
- **Everything here is loaded** into Frosty's context on session startup via the `read-knowledge` tool.

## File Conventions

- Use `.md` format for all files
- Name files descriptively (e.g., `amp-iframe-quirks.md`, `client-xyz-notes.md`)
- Frosty will reference all files here when troubleshooting AMP issues
