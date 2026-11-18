# Page, keyword, title and H1 map

Canonical domain: `https://cherryappagency.com`. All URLs use trailing slashes.
Every indexable page has a self-referencing canonical and appears in `sitemap.xml`.

| URL | Primary focus | Supporting terms | Title | H1 |
|---|---|---|---|---|
| `/` | Cherry app agency | Cherry agency | Cherry App Agency \| Host & Agency Registration Guide | Cherry App Agency – Explore Host and Agency Opportunities |
| `/cherry-agency/` | Cherry agency registration | Cherry agency commission, Cherry app agency registration | Cherry Agency Registration, Commission & Payment Guide | Cherry Agency Registration and Commission Guide |
| `/cherry-app/` | Cherry app | Cherry app hosts and agencies, diamonds | Cherry App Overview: Video Chat, Diamonds, Hosts & Agencies | The Cherry App: How the Platform Works for Hosts and Agencies |
| `/cherry-host/` | Cherry host registration | Cherry app host, Cherry host earnings | Cherry Host Registration, Earnings & Eligibility | Cherry Host Registration and Earnings Guide |
| `/cherry-earnings/` | Cherry app earnings | Cherry diamonds to USD, Cherry diamond conversion | Cherry App Earnings: Diamonds to USD Conversion | Cherry App Earnings: Diamonds to USD Conversion |
| `/cherry-withdrawal/` | Cherry app withdrawal | Cherry minimum withdrawal, Cherry payment policy | Cherry App Withdrawal: Minimum, Review Time & Payment Policy | Cherry App Withdrawal Rules and Payment Policy |
| `/cherry-policy/` | Cherry app policy | Cherry agency policy, Cherry host rules | Cherry App Policy: Host Rules, Warnings & Account Bans | Cherry App Policy: Host Rules and Agency Conditions |
| `/about/` | About this website | Independent Cherry App information | About Cherry App Agency \| Independent Information Website | About Cherry App Agency |
| `/contact/` | Contact / WhatsApp enquiries | Cherry registration enquiry | Contact Cherry App Agency \| WhatsApp +91 9233262700 | Contact Cherry App Agency |
| `/404.html` | — (noindex, not in sitemap) | — | Page Not Found \| Cherry App Agency | Page not found |

Not created, on purpose: `/cherry-app-agency/` (it would duplicate the homepage or the
agency page), city pages, keyword-variant pages, an empty blog and a download page.

## Internal linking (as built)

- Home → agency, host, app, earnings, withdrawal and policy, all in body copy and cards
- Agency → withdrawal and policy
- Host → earnings, withdrawal and policy
- Earnings → withdrawal, plus host and agency
- App overview → host and agency guides
- Footer on every page → all guides, plus About and Contact

## Structured data

- Home: `WebSite`, `Organization` (name, URL, logo, WhatsApp enquiry ContactPoint only) and `WebPage`
- Inner pages: `WebPage` (`AboutPage` / `ContactPage` where relevant) with `BreadcrumbList`
- No `FAQPage`, `SoftwareApplication`, ratings, reviews, address or social profiles

FAQ answers are visible HTML (`<details>`) on each page, whatever the structured data says.
Meta descriptions and structured data help search engines understand the pages,
but they do not guarantee rankings or rich results.
