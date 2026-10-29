# Content verification notes

Last reviewed: 29 October 2026.

## Sources used

The source documents were **not** in the repository when the site was built.
"Recruiting Policy - Cherry.pdf" and the salary-plan image were not available.
The website content is based on the policy details written out in the project brief.
In the brief's priority order, those details stand for:

1. Original supplied recruiting PDF
2. Separately supplied salary-plan image
3. Owner's pasted policy summary
4. Earlier draft copy

**Before launch, check every figure on the site against the original PDF and salary image.**
In particular, check the exact eligibility wording, the commission table, the
withdrawal-review wording and the UTC+8 settlement section.

## Open questions shown on the site

Each item is flagged next to the relevant claim and listed in the table at
`/cherry-policy/#clarifications`.

| # | Topic | What is unresolved | Where it is flagged |
|---|---|---|---|
| 1 | Commission rate | The table lists 15%–40%, but the PDF's worked examples use 10% | Home, Agency, Policy |
| 2 | Below $300/week | No rate is stated below the Level A threshold | Home, Agency (FAQ), Policy |
| 3 | Tier mechanics | Whether a rate applies to the whole week's earnings or only above each threshold. No calculator was built for this reason | Agency, Policy |
| 4 | Sub-agent minimum | "Qualifying" sub-agents are mentioned, but the minimum is unclear | Agency, Policy |
| 5 | Video-call counting | Wording about the first 30 seconds and the second minute is unclear | Home, Host, Earnings, App |
| 6 | Salary plan status | Not confirmed as currently active | Home, Host, Policy |
| 7 | Salary working duration | 3–5 hours, but not stated whether daily or weekly | Host, Policy |
| 8 | Registration procedure | The current application steps and any fees are unconfirmed | Home, Host, Agency, Policy |
| 9 | Download destination | The official app source is unverified. No store links, badges or APKs are shown | App, Home (FAQ) |
| 10 | Agency minimum withdrawal | Only the $10 host minimum is stated | Withdrawal, Agency |
| 11 | Withdrawal details | Fees, exchange rates, KYC documents, supported countries, other payment methods and bank-arrival time are not stated | Withdrawal |
| 12 | Earnings-withholding clauses | Reported as stated platform rules only, with no view on enforceability | Policy |
| 13 | Paid-call types | Which call types count as "paid calls" for agency commission | Agency |

## Statement types used on the site

- **Policy statements** say "the policy states/says/describes".
- **Maths** (for example $0.10/min from 1,000 diamonds, or 7:30 AM IST = 10:00 AM UTC+8)
  is labelled as a conversion, not a policy promise.
- **Unknowns** are labelled "Not confirmed", "Clarification pending" or "Not stated in the source".

## Deliberately excluded

- No official-partner claims, reviews, testimonials, download counts, user totals or trust badges.
- No guaranteed income, approval or payment timing.
- No INR conversions. The exchange method is unverified.
- No FAQPage, SoftwareApplication, rating or address structured data.
- Cherry's separate support details from the policy are not published. The only contact
  is the website's WhatsApp enquiry number, +91 9233262700.
- No forms and no requests for identity documents.

## When something is confirmed

1. Update the relevant text in `src/pages/*.html`, and remove or rewrite its caveat.
2. Update the clarification table in `src/pages/policy.html` and this file.
3. Change that page's `reviewed` date in `tools/build.py`, then rebuild.
