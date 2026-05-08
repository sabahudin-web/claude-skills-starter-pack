# Email Content Patterns — Bucket Detection

How to categorize an email **by content**, not by sender domain. This is what makes the skill survive tool swaps (Weezly → Calendly, Tally → Typeform, etc).

**Order matters.** Apply patterns in the order listed for each bucket. First match wins. If no pattern matches → UNKNOWN.

---

## INBOUND (highest priority — leads & inbound bookings)

### 1. Form submission (any provider)
- **Body fingerprint**: contains structured form fields like `Name:` AND `Email:` AND (`LinkedIn:` OR `Company:` OR `Role:`)
- **OR sender domain**: `tally.so`, `typeform.com`, `paperform.co`, `jotform.com`
- **Action template**: "ICP fit: [HIGH/MEDIUM/LOW] — [reason]. Reply within 24h."
- **Special**: parse the form fields and run a quick ICP mini-score (see ICP context). One line in the report.

### 2. Calendar booking notification (any scheduling tool)
- **Subject regex**: `^(New |)?(event|booking|meeting) (scheduled|confirmed|booked)` OR contains `has booked` OR `has scheduled`
- **OR sender domain**: `weezly.com`, `calendly.com`, `cal.com`, `savvycal.com`, `tidycal.com`
- **Body must contain**: a date/time AND an invitee name
- **Action template**: "Meeting booked: [Name] on [Date Time] — run `operations-meeting-prep` 24h before."

### 3. Calendar invite **sent by** an external person (manual booking)
- **Subject regex**: `^Invitation: ` (Google Calendar `Invitation:` prefix)
- **AND sender is**: a personal email (not `noreply@`, not `notifications@`, not yourself)
- **AND body contains**: a Meet/Zoom/Teams link
- **Action template**: "[Name] invited you to a call: [Date Time]. Confirm or reschedule."
- **Note**: Higher intent than auto-booking — they took the action of putting you on their calendar.

### 4. Calendar invite with `(No Subject)` from personal Gmail
- **Subject regex**: `^Invitation: \(No Subject\)`
- **AND sender domain**: `gmail.com` (or other personal domain)
- **Action template**: "Likely intro/discovery call from [Name] — check what you know about them before."

### 5. Manual booking request (no tool — plain text)
- **Subject regex**: `^(Re: )?Booking|availability|book in` (case-insensitive)
- **AND sender is**: a personal/business email (not noreply)
- **AND body contains**: phrases like "do you have availability", "are you free", "when can we", "looking to book"
- **Action template**: "[Name] is asking to book — propose times."

---

## CLIENT (active paying clients)

### 1. Sender matches active client
- Sender email/domain matches anyone in Notion Client Deliverables DB with open rows
- Bucket = CLIENT regardless of subject

### 2. Client's assistant/delegate booking on their behalf
- Sender on a known client domain BUT name signature in body is a different person
- Body fingerprint: "Hi, [Chris/Assistant] here from [Client Name]'s team" or "[Client] asked me to book"
- Bucket = CLIENT (treat as if from client)
- **Action template**: "[Delegate] is booking for [Client] — confirm time."

### 3. Client logistics email out-of-band
- Sender matches active client + subject contains "coaching" / "session" / "Zoom" / "meeting" + body has a link inline
- Same-day reply needed even if calendar invite already exists
- Bucket = CLIENT

### 4. Fathom recap from a client session
- Sender domain = `fathom.video` AND recording is from a client meeting
- Bucket = CLIENT
- **Action template**: parse body for "commitments made by you" and "agreed next steps" — extract as separate action items: "From [Session]: [commitment]"

### 5. Zoom invite from existing client
- Subject starts `Invitation:` AND body contains `zoom.us/j/` AND sender matches active client
- Bucket = CLIENT (recurring session — distinct from new INBOUND bookings)

---

## REVENUE (prospects in pipeline)

### 1. Sender matches CRM prospect
- Sender email/domain matches Notion People DB (Status ≠ Lost / Cold)
- Bucket = REVENUE

### 2. Reply to your outbound (special-case override — see rubric)
- Sender NOT in CRM/clients
- BUT you sent the first message in thread (you are in the `from` field of the earliest message)
- Subject typically starts `Re:`
- Bucket = REVENUE, min score = 3, badge ≥ 🔴
- **Action template**: "Warm reply from [Name] — review thread, draft response."

### 3. Subject contains revenue keywords
- Subject contains: "proposal", "invoice", "payment", "interested", "pricing", "contract", "quote", "scope"
- Bucket = REVENUE

### 4. Calendar acceptance from external prospect
- Subject starts `Accepted: ` AND sender is external person (not you, not noreply)
- Bucket = REVENUE
- **Action template**: "[Name] confirmed [meeting] — prep 24h before."

### 5. Referral mention in body
- Body contains: "X referred me", "X said I should reach out", "X told me about you", "X mentioned", "introduce" + a known contact name
- Bumps to REVENUE bucket and adds +2 to score
- **Action template**: "Referral via [Referrer] — high context, fast reply."

---

## ADMIN (transactional, ops, time-bombed)

### 1. Time-bombed renewal/billing (sub-bucket)
- Subject regex: `subscription will renew|invoice is available|will automatically renew|credits running out|usage alert|overage`
- OR sender contains: `upcoming-invoice@`, `payments-noreply@`, `billing@`, `receipts@`
- Bucket = ADMIN, sub-bucket = "time-bombed"
- **Surface inline if renewal date is within 5 days.**
- **Action template (only if ≤5 days)**: "Renewing: [Service] on [Date] for [$amount]. Keep or cancel?"

### 2. Calendar reminders (existing meetings)
- Subject regex: `^Reminder:|reminder for your meeting`
- Bucket = ADMIN

### 3. Slack mention
- Sender = `notification@slack.com` AND subject `New messages from … in <workspace>`
- Bucket = ADMIN if the workspace is client-related, else FYI

### 4. Security / 2FA / login alert
- Subject regex: `verification code|sign-in attempt|new device|security alert|two-factor`
- Bucket = ADMIN
- **Note**: usually self-completed in seconds, but surface inline because they can't be missed.

### 5. Bank / payment confirmation
- Subject regex: `payment received|transaction|deposit|wire|transfer confirmed`
- Sender is a known bank/Stripe/PayPal/Wise domain
- Bucket = ADMIN

---

## FYI (low-signal informational)

### 1. Noise blocklist hit
- Sender domain matches anything in `noise-blocklist.md`
- Bucket = FYI (auto-filed, not scored)

### 2. SaaS-drip-pretending-to-be-human
- Sender pattern: `firstname@mail.*` / `firstname@email.*` / `firstname@notifications.*`
- Even with personalized "Hey [You]" body — still FYI
- Bucket = FYI

### 3. Newsletter / digest
- Body contains "unsubscribe" footer AND no personal greeting
- OR subject regex: `weekly digest|newsletter|roundup|the [day] [briefing|brief|wire]`
- Bucket = FYI

### 4. Course/system confirmation chains
- Sender pattern: `academy-support@`, `learn@`, `noreply@*.skilljar.com`, `noreply@*.maven.com`
- Subject regex: `Completion of|registration for|Welcome to|complete your signup`
- Bucket = FYI

### 5. Calendar accept WITH personal note
- Subject `Accepted:` AND body contains free-text beyond auto-RSVP
- Bucket = FYI but flag with `(human note)` next to the entry — soft signal

### 6. 3rd-party Substack/Beehiiv newsletters (not yours)
- Sender: `*@substack.com` (excluding your own) OR `*@mail.beehiiv.com`
- Bucket = FYI

---

## UNKNOWN (last resort)

If none of the above patterns match AND sender is:
- Not in Notion (not active client, not CRM prospect)
- Not on noise blocklist
- Not from a known scheduling/form/billing tool
- Not a clear newsletter

→ Bucket = UNKNOWN.

**Cap UNKNOWN at 5 emails per report.** If more, keep the 5 most recent and note "X more unclassified — review in inbox."

UNKNOWN is the feedback loop. You glance → tell the skill what to do with it → Claude adds a rule to this file. The brain compounds.

---

## Dropped-ball detection (separate query, not a bucket)

Run as a parallel Gmail query (see SKILL.md): `from:me older_than:3d newer_than:14d`

For each result:
- Get the thread → check if anyone replied AFTER your last message
- If no reply → it's a dropped ball
- Surface in 🟠 Dropped Balls section with: who, subject, days dormant, last action

Skip threads where your last message contained "ttyl", "no rush", "fyi", "thanks!" (closure language) — those don't need followup.
