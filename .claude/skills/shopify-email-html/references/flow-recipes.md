# Flow recipes

## Abandoned checkout, multi-send (built 2026-10-03, workflow "Recover abandoned checkout")

Created from Messaging → Automations → Create automation → **Recover abandoned checkout** →
**Edit email** (not "Turn on automation"). Shopify generates this Flow graph:

```
Trigger: Customer abandons checkout
Condition: abandoned on online store            (True ↓)
Condition: total price > $0.00                  (True ↓)
Wait 10 hours                                   → change to the first delay
Condition: customer hasn't placed an order or abandoned another checkout since starting
           = customerHasNoOrderSinceAbandonment == true AND hoursSinceLastAbandonedCheckout > 24
Condition: 1+ products available and in stock   (True ↓)
Send marketing email (email 1)
```

Extend it after email 1 for each further send:

```
Wait <n> (seconds if the unit select won't open)
Condition: abandonment.customerHasNoOrderSinceAbandonment == true   (True ↓)
Send marketing email (email k)  → Select template → Code your own
```

HSC timing (delays from abandonment): CR-1 +4 h, CR-2 +24 h (wait 72000 s), CR-3 +48 h (wait
86400 s), CR-4 +96 h (wait 172800 s).

The Send step's Abandonment field defaults to `abandonment.id` and Customer to `customer.id`;
leave them.

## Before turning a workflow on (needs explicit user approval)

1. Every Send step's email is complete and previewed; placeholders replaced.
2. Discount codes referenced in emails exist and are active.
3. No other abandoned-checkout sender is live (Shopify's built-in abandoned checkout email in
   Settings → Notifications, Customer.io, Klaviyo …) — otherwise customers get duplicates.
4. Send test of each email to the user's own address.
5. Turn on each email, then **Turn on workflow**.

## Asking Shopify Sidekick to build a workflow (2026-10-04)

Faster than building on the canvas. On the Flow page open Sidekick (or use "Tell me what you want to
create" on a blank workflow) and describe the workflow, the trigger, any guard and "do not turn
anything on". When it answers, **stay on the page**, click **Preview** on each workflow card, then
**Add to store** (top right of the preview). Workflows are saved inactive with a "sidekick" tag. Open
each and check the trigger, conditions and waits: Sidekick's conditions use "Tags is equal to", and
the Send step has no email yet ("Select template" → Blank → sections). Flow allows one trigger per
workflow, so "A or B" becomes two workflows.

## Built workflows (all inactive)

Welcome (W-1: newsletter sign-up OR first order, whichever comes first):

```
"Welcome email on email marketing subscribe"
  Trigger: Customer subscribed to email marketing
  Condition: Tags is equal to welcome-email-sent   (True: stop)
  Add customer tags: welcome-email-sent
  Send marketing email: W-1 (sections)

"Welcome email on first order"
  Trigger: Order created
  Condition: Customer number of orders = 1
  Wait 2 minutes                                   (so the subscribe workflow wins a race)
  Condition: Tags is equal to welcome-email-sent   (True: stop)
  Add customer tags: welcome-email-sent
  Send marketing email: W-1 (currently an older Code your own draft: needs a new Send step)
```

Win-back and reorder ("no newer order" guard). Flow has no "customer has no newer order" field, so
the check is a Get customer data step:

```
"WB win-back: 90 days without an order"            "RO reorder: 60 days after last purchase"
  Trigger: Order created                             Trigger: Order created
  Wait 7,776,000 s (90 days)                         Wait 5,184,000 s (60 days)
  Get customer data (Advanced query)                 Get customer data (Advanced query)
  Condition: at least one customer found             Condition: same
             whose id = order.customer.id            (no email step: RO-1 has no design)
  False branch (no newer order): Send WB-1
```

Advanced query: `id:{{ order.customer.id | split: "/" | last }} AND order_date:>='{{ order.createdAt | date: "%s" | plus: 86400 | date: "%Y-%m-%d" }}'`.
Condition operators are native selects that cannot be changed under automation, so the logic is
"at least one of get customer data" with the email on the False branch. **Untested**: run a test
customer through it (the `order_date` filter, the id extraction, and `customer.last_order` inside a
Flow email) before anyone turns the workflow on.

Typed Liquid in an ID field is rejected ("Invalid id format"): insert variables with the "</>" picker
(drill into the Get customer data group, then search "id").
