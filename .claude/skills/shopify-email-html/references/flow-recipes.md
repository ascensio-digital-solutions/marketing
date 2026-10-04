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
