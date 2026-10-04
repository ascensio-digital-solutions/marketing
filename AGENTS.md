# Shopify Email Marketing

## Source of truth

This repository is the **only source of truth for Hair Solutions Co. email marketing** (decided by
Vincent, 2026-10-03). Notion pages (masterplan, "Shopify Email Sections", "Shopify Email
Templates") are references or mirrors; when they disagree with this repository, this repository
wins. Older projects (marketing-os, MailerLite, HubSpot, Resend) are not sources.

## Scope

This repository contains the lifecycle-email strategy, the email library (sections and templates),
campaign assets, reporting definitions, and automation QA evidence for Hair Solutions Co.

## Design system

Visual design comes from [`vincent-laroche/brand-design-system`](https://github.com/vincent-laroche/brand-design-system),
folder [`email/`](https://github.com/vincent-laroche/brand-design-system/tree/main/email): the HSC
email design system (React email blocks, tokens, assembly guides) and the Figma library
"HSC Email Design System" (`hpen3ExIfmyI7xBEqC6i2h`). Do not invent colours, type roles or
components that are not there.

## Email library

- Sections database: `templates/email-blocks/` (one folder per section: `section.html`,
  `section.json`, `preview.png`).
- Templates database: `templates/emails/` (one folder per email: `template.json` with the ordered
  `sections` recipe, plus generated install files and preview).
- Build, check and preview with `.claude/skills/shopify-email-html/scripts/build_library.py`.
  Never edit generated files by hand.
- Skill: `.claude/skills/shopify-email-html/SKILL.md` — read it before building or installing any
  Shopify email.

**Build rule (Vincent, 2026-10-04):** every email template, whether new or rebuilt from earlier
sections, is built in the Shopify Messaging email editor by creating and assembling HTML sections one
at a time (Add section → Custom → Custom Liquid; each one becomes a reusable section in Shopify).
Use recipe surface `messaging-sections`. Do **not** build new emails as one "Code your own" document
unless Vincent asks. Emails already installed as Code your own (CR-2 to CR-4, NL-01, WB-1) predate
this rule; rebuild them as sections only when Vincent asks. A Flow step's email cannot change type,
so a step that holds a Code your own draft needs a new Send step (ask before deleting the old one).

Design rules every email must follow (enforced by the build):

1. Rounded corners on every component: cards 12px, insets 8px, buttons and pills 999px.
2. No gap between blocks: cards stack flush.
3. Transparent background behind the modules (body, wrapper, and Shopify Messaging's Content
   background).

## Key locations

| What | Where |
|---|---|
| Shopify store | `admin.shopify.com/store/oneheadhair`. Files CDN: `https://cdn.shopify.com/s/files/1/0276/9115/5508/files/` |
| Design (Figma) | "Email Design System", page "v6 · Reference": https://www.figma.com/design/9Il504CQE8jLaUTBVzphqc/Email-Design-System?node-id=557-7295 |
| Tokens and components | `vincent-laroche/brand-design-system` → `email/` (local: `~/01_hair_solutions_co/design/brand/brand-design-system`) |
| Skill and scripts | `.claude/skills/shopify-email-html/` (installed globally through a symlink at `~/.claude/skills/shopify-email-html`) |
| Handoff prompt for new agents | [`HANDOFF.md`](HANDOFF.md) |
| Notion | "Shopify Email Marketing Masterplan" (read-only); "Shopify Email Sections" and "Shopify Email Templates" databases (records of this library) and "Messaging Journeys" (https://app.notion.com/p/d3802cf29293450cad97d24a04e64b49, one row per Shopify workflow). The repo wins when they disagree; keep them current as you build |
| What is missing | GitHub issue #7 (every Figma email not yet in Shopify); #3 button destinations, #4 RO-3 metafields, #5 copy and facts to confirm |
| Old Resend/Customer.io worker | `~/01_hair_solutions_co/marketing/resend-customerio-archive` (archive, not a source; holds PII in `data/`) |

## Current state (2026-10-04)

| Email | Surface | Shopify state |
|---|---|---|
| PP-1 Order confirmation | Notification template | **Live** |
| CR-1 Your cart's still here | Messaging · Custom Liquid sections | Draft, matches repo |
| CR-2 / CR-3 / CR-4 | Messaging · Code your own | Draft, match repo (re-synced 2026-10-03) |
| "Recover abandoned checkout" Flow | Flow workflow (CR-1 to CR-4) | **Inactive**; turning it on needs Vincent's approval |
| NL-01 Education | Messaging campaign · Code your own | Draft (no segment, not scheduled) |
| WB-1 | Flow workflow "WB win-back" · Code your own | Draft, matches repo; workflow **inactive**, check step untested |
| "RO reorder" Flow | Flow workflow | **Inactive**, no email step (RO-1 has no design) |
| W-1 | Flow workflows "Welcome email on email marketing subscribe" and "…on first order" · Custom Liquid sections | Draft in the subscribe workflow (sections); first-order workflow still holds a Code your own draft; both workflows **inactive** |
| WB-2, RO-3 | Messaging | In the library, not installed in Shopify; recipes still say `messaging-code-your-own`: switch to `messaging-sections` before installing |
| C-0 Consultation recap | Messaging · Code your own | In the library only; not to be created in Shopify |

Each `templates/emails/*/template.json` holds the authoritative per-email state.

## Working in parallel (several agents)

- One agent per journey or assignment, on its own branch (`<journey>-emails`), with its own Flow
  workflow. Do not edit another agent's workflow or templates.
- New section folders are named `<code>-<slug>` (for example `w-1-hero`); never take the next
  number. Shared sections (email head, logo header, cart contents, footers, trust strip) are
  reused, never copied. Change a shared section only in its own pull request.
- Copy comes word for word from the Figma frames; when it is missing, ask Vincent.
- No placeholders ever reach Shopify: names, quotes and photos are real values or Liquid.

## Rules

- Marketing emails are built from Custom Liquid sections one at a time (see the build rule above).
  Ask Shopify Sidekick to build Flow workflows (Preview, then **Add to store**); never turn them on.
- Never delete a Flow step, workflow or email without approval; list leftover drafts for Vincent.
- Post-consultation emails (C-0 and the C series) are not created in Shopify.

- Do not send, schedule, publish, or enable customer-facing email without explicit approval.
  Saving a Shopify notification template makes it live: that needs approval too.
- Preserve consent, purchase exits, suppression logic, and lifecycle state.
- Validate events, sender identity, links, mobile rendering, attribution, and rollback before release.
- Never render previews or commit fixtures with real customer data.
- Work on a branch and open a pull request; merging is never activation.
- Never pan the Flow canvas by dragging on a step (it moves the step). Never click "Turn on".
