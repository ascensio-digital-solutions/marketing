# Shopify Email Marketing Masterplan

## Source of truth

Notion is the strategy and operating source of truth. This repository is the implementation and version-control layer.

## Scope

This repository contains approved lifecycle-email implementation, templates, campaign assets, reporting definitions, and automation QA evidence for Hair Solutions Co.

## Rules

- Build only from an approved Notion blueprint.
- Preserve consent, purchase exits, suppression logic, and lifecycle state.
- Do not send, schedule, publish, or enable customer-facing email without explicit approval.
- Validate events, sender identity, links, mobile rendering, attribution, and rollback before release.
