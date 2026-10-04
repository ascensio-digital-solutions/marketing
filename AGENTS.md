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

Design rules every email must follow (enforced by the build):

1. Rounded corners on every component: cards 12px, insets 8px, buttons and pills 999px.
2. No gap between blocks: cards stack flush.
3. Transparent background behind the modules (body, wrapper, and Shopify Messaging's Content
   background).

## Rules

- Do not send, schedule, publish, or enable customer-facing email without explicit approval.
  Saving a Shopify notification template makes it live: that needs approval too.
- Preserve consent, purchase exits, suppression logic, and lifecycle state.
- Validate events, sender identity, links, mobile rendering, attribution, and rollback before release.
- Never render previews or commit fixtures with real customer data.
- Work on a branch and open a pull request; merging is never activation.
