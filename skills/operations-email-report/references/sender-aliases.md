# Sender Aliases

Same person, multiple email addresses. The skill unifies them when running VIP detection and active-client lookup.

**How to add an alias:** When you notice a duplicate (same person writing from a second email), add a row below.

**When to audit:** Quarterly, or when a known client's emails start scoring as UNKNOWN. Cross-reference last 30 days of Gmail senders against your People CRM — if one person sends from two different addresses, alias them.

**Format:**

```yaml
- canonical_name: "Display Name"
  primary_email: "main@domain.com"
  aliases:
    - "alt1@domain.com"
    - "alt2@otherdomain.com"
```

---

## Aliases

Add your own contacts here. Example format (remove this and add real entries):

```yaml
# - canonical_name: "Jane Smith"
#   primary_email: "jane@company.com"
#   aliases:
#     - "jane.smith@gmail.com"
#     - "jane@oldcompany.com"
```

No entries yet — add them as you discover people writing from multiple addresses.

---

## How the skill uses this

When scoring an email:
1. Take the sender email
2. Look up in this file — if it's an alias, replace with `primary_email`
3. Use `primary_email` for active-client check, CRM lookup, VIP thread counting

This means a contact writing from either address counts as the same person — VIP threshold of 3 threads/30d catches them even if they split across both.
