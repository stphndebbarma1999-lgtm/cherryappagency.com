#!/usr/bin/env python3
"""Build the static Cherry App Agency website.

Page bodies live in src/pages/*.html. This script wraps each body in the
shared layout (head metadata, header, footer, structured data) and writes
plain HTML into site/, which is the folder you upload to the web host.

Usage:  python3 tools/build.py
No third-party packages are required.
"""
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src" / "pages"
OUT = ROOT / "site"

DOMAIN = "https://cherryappagency.com"
SITE_NAME = "Cherry App Agency"
ASSET_VERSION = "2"

WA_BASE = "https://wa.me/919233262700"
WA = {
    "host": WA_BASE + "?text=Hi%2C%20I%20want%20information%20about%20joining%20Cherry%20App%20as%20a%20host.",
    "agency": WA_BASE + "?text=Hi%2C%20I%20want%20information%20about%20Cherry%20agency%20registration.",
    "general": WA_BASE + "?text=Hi%2C%20I%20have%20a%20question%20about%20Cherry%20App.",
}
PHONE_DISPLAY = "+91 9233262700"

# Change a page's "reviewed" value only when its content is actually reviewed
# or edited. It feeds the visible review date, dateModified and sitemap lastmod.
PAGES = [
    {
        "src": "home.html", "path": "/", "reviewed": "2026-10-29", "wa": "general",
        "title": "Cherry App Agency | Host & Agency Registration Guide",
        "description": "Independent Cherry app agency guide: agency commission tiers, host earnings, diamond value, withdrawal rules and policy conditions, with WhatsApp registration enquiries.",
        "crumb": None, "type": "WebPage",
    },
    {
        "src": "agency.html", "path": "/cherry-agency/", "reviewed": "2026-10-29", "wa": "agency",
        "title": "Cherry Agency Registration, Commission & Payment Guide",
        "description": "Cherry agency commission tiers from 15% to 40%, eligible earning categories, the Monday calculation schedule, sub-agency commission and registration enquiry steps.",
        "crumb": "Agency guide", "type": "WebPage",
    },
    {
        "src": "app.html", "path": "/cherry-app/", "reviewed": "2026-10-29", "wa": "general",
        "title": "Cherry App Overview: Video Chat, Diamonds, Hosts & Agencies",
        "description": "What the Cherry app is according to its recruiting policy: a video-chat platform where hosts earn diamonds and agencies earn commission. Roles, earnings and download status explained.",
        "crumb": "Cherry app overview", "type": "WebPage",
    },
    {
        "src": "host.html", "path": "/cherry-host/", "reviewed": "2026-10-29", "wa": "host",
        "title": "Cherry Host Registration, Earnings & Eligibility",
        "description": "Cherry host eligibility, video-call and match-call diamond rates, 70% gift share, the $10 minimum withdrawal, conditional weekly salary details and working rules.",
        "crumb": "Host guide", "type": "WebPage",
    },
    {
        "src": "earnings.html", "path": "/cherry-earnings/", "reviewed": "2026-10-29", "wa": "general",
        "title": "Cherry App Earnings: Diamonds to USD Conversion",
        "description": "How Cherry app earnings are measured in diamonds: 10,000 diamonds = $1, a conversion table, a diamond-to-USD converter and the stated host earning rates.",
        "crumb": "Earnings and diamonds", "type": "WebPage",
    },
    {
        "src": "withdrawal.html", "path": "/cherry-withdrawal/", "reviewed": "2026-10-29", "wa": "general",
        "title": "Cherry App Withdrawal: Minimum, Review Time & Payment Policy",
        "description": "Cherry app withdrawal rules: the $10 host minimum, review within three working days, payment after approval, bank transfer, holiday delays and what is not yet confirmed.",
        "crumb": "Withdrawals", "type": "WebPage",
    },
    {
        "src": "policy.html", "path": "/cherry-policy/", "reviewed": "2026-10-29", "wa": "general",
        "title": "Cherry App Policy: Host Rules, Warnings & Account Bans",
        "description": "A plain-language summary of the Cherry app policy for hosts and agencies: working-time conduct, warning limits, serious violations and immediate-ban rules.",
        "crumb": "Policy summary", "type": "WebPage",
    },
    {
        "src": "about.html", "path": "/about/", "reviewed": "2026-10-29", "wa": "general",
        "title": "About Cherry App Agency | Independent Information Website",
        "description": "Why this independent Cherry App information website exists, which sources it uses, what it does not claim, and how to report an error.",
        "crumb": "About", "type": "AboutPage",
    },
    {
        "src": "contact.html", "path": "/contact/", "reviewed": "2026-10-29", "wa": "general",
        "title": "Contact Cherry App Agency | WhatsApp +91 9233262700",
        "description": "Contact Cherry App Agency on WhatsApp at +91 9233262700 for host or agency registration enquiries and general Cherry App questions.",
        "crumb": "Contact", "type": "ContactPage",
    },
    {
        "src": "404.html", "path": "/404.html", "reviewed": "2026-10-29", "wa": "general",
        "title": "Page Not Found | Cherry App Agency",
        "description": "The page you requested could not be found on Cherry App Agency.",
        "crumb": None, "type": None, "noindex": True,
    },
]

NAV = [
    ("/cherry-app/", "Cherry App"),
    ("/cherry-host/", "Host Guide"),
    ("/cherry-agency/", "Agency Guide"),
    ("/cherry-earnings/", "Earnings"),
    ("/cherry-withdrawal/", "Withdrawal"),
    ("/cherry-policy/", "Policy"),
    ("/contact/", "Contact"),
]

FOOTER_GUIDES = [
    ("/cherry-host/", "Host registration guide"),
    ("/cherry-agency/", "Agency registration guide"),
    ("/cherry-app/", "Cherry app overview"),
    ("/cherry-earnings/", "Earnings and diamond value"),
    ("/cherry-withdrawal/", "Withdrawal rules"),
    ("/cherry-policy/", "Policy summary"),
]
FOOTER_SITE = [("/", "Home"), ("/about/", "About this website"), ("/contact/", "Contact")]

MONTHS = ["January", "February", "March", "April", "May", "June", "July",
          "August", "September", "October", "November", "December"]

WA_ICON = ('<svg class="icon" viewBox="0 0 24 24" width="24" height="24" aria-hidden="true" focusable="false">'
           '<path fill="currentColor" d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2c-1.5 0-3-.4-4.3-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2zm4.6-6.1c-.3-.1-1.5-.7-1.7-.8-.2-.1-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.2-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5c-.2 0-.4.1-.7.3-.2.3-.9.9-.9 2.1s.9 2.4 1 2.6c.1.2 1.8 2.8 4.4 3.9 1.6.7 2.3.8 3.1.6.5-.1 1.5-.6 1.7-1.2.2-.6.2-1.1.2-1.2-.1-.2-.3-.3-.7-.4z"/></svg>')


def human_date(iso):
    y, m, d = (int(x) for x in iso.split("-"))
    return f"{d} {MONTHS[m - 1]} {y}"


def esc(text):
    return html.escape(text, quote=True)


def wa_link(context, label, cls="btn btn-primary"):
    return (f'<a class="{cls}" href="{WA[context]}" target="_blank" rel="noopener">'
            f'{WA_ICON}<span>{label}</span><span class="visually-hidden"> (opens WhatsApp)</span></a>')


def structured_data(page):
    url = DOMAIN + page["path"]
    website = {"@id": DOMAIN + "/#website"}
    graph = []
    if page["path"] == "/":
        graph.append({
            "@type": "WebSite",
            "@id": DOMAIN + "/#website",
            "url": DOMAIN + "/",
            "name": SITE_NAME,
            "description": "Independent information and registration-enquiry website about the Cherry App for prospective hosts and agencies.",
            "inLanguage": "en",
            "publisher": {"@id": DOMAIN + "/#organization"},
        })
        graph.append({
            "@type": "Organization",
            "@id": DOMAIN + "/#organization",
            "name": SITE_NAME,
            "url": DOMAIN + "/",
            "logo": {"@type": "ImageObject", "url": DOMAIN + "/assets/images/cherry-logo.png", "width": 512, "height": 512},
            "contactPoint": {
                "@type": "ContactPoint",
                "telephone": "+91-9233262700",
                "contactType": "registration enquiries",
                "availableLanguage": ["English"],
            },
        })
    webpage = {
        "@type": page["type"],
        "@id": url + "#webpage",
        "url": url,
        "name": page["title"],
        "description": page["description"],
        "isPartOf": website,
        "inLanguage": "en",
        "dateModified": page["reviewed"],
    }
    graph.append(webpage)
    if page["path"] == "/":
        webpage["about"] = {"@id": DOMAIN + "/#organization"}
    else:
        webpage["breadcrumb"] = {"@id": url + "#breadcrumb"}
        graph.append({
            "@type": "BreadcrumbList",
            "@id": url + "#breadcrumb",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": DOMAIN + "/"},
                {"@type": "ListItem", "position": 2, "name": page["crumb"], "item": url},
            ],
        })
    data = {"@context": "https://schema.org", "@graph": graph}
    return '<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False, indent=1) + "</script>"


def head(page):
    url = DOMAIN + page["path"]
    noindex = page.get("noindex")
    lines = [
        '<!doctype html>',
        '<html lang="en">',
        '<head>',
        '<meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        f'<title>{esc(page["title"])}</title>',
        f'<meta name="description" content="{esc(page["description"])}">',
    ]
    if noindex:
        lines.append('<meta name="robots" content="noindex, follow">')
    else:
        lines += [
            f'<link rel="canonical" href="{url}">',
            '<meta property="og:type" content="website">',
            f'<meta property="og:site_name" content="{SITE_NAME}">',
            f'<meta property="og:title" content="{esc(page["title"])}">',
            f'<meta property="og:description" content="{esc(page["description"])}">',
            f'<meta property="og:url" content="{url}">',
            f'<meta property="og:image" content="{DOMAIN}/assets/images/cherry-social-preview.png">',
            '<meta property="og:image:width" content="1200">',
            '<meta property="og:image:height" content="630">',
            '<meta property="og:image:alt" content="Cherry App Agency cherry logo beside an illustration of a video call, with the text Host and agency registration guide">',
            '<meta property="og:locale" content="en_IN">',
            '<meta name="twitter:card" content="summary_large_image">',
        ]
    lines += [
        '<meta name="theme-color" content="#ffffff">',
        '<link rel="icon" href="/favicon.ico" sizes="32x32">',
        '<link rel="icon" href="/assets/images/favicon.svg" type="image/svg+xml">',
        '<link rel="apple-touch-icon" href="/apple-touch-icon.png">',
        '<link rel="manifest" href="/site.webmanifest">',
        '<link rel="preload" href="/assets/fonts/barlow-condensed-700.woff2" as="font" type="font/woff2" crossorigin>',
        f'<link rel="stylesheet" href="/assets/css/styles.css?v={ASSET_VERSION}">',
        "<script>document.documentElement.className+=' js'</script>",
    ]
    if not noindex:
        lines.append(structured_data(page))
    lines.append('</head>')
    return "\n".join(lines)


def header(page):
    items = []
    for href, label in NAV:
        current = ' aria-current="page"' if href == page["path"] else ""
        items.append(f'<li><a href="{href}"{current}>{label}</a></li>')
    home_current = ' aria-current="page"' if page["path"] == "/" else ""
    return f'''<body>
<a class="skip-link" href="#main">Skip to main content</a>
<header class="site-header">
  <div class="container header-inner">
    <a class="brand" href="/"{home_current}>
      <img src="/assets/images/cherry-logo.svg" width="40" height="40" alt="">
      <span class="brand-name">Cherry App <span>Agency</span></span>
    </a>
    <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav" hidden>
      <span class="nav-toggle-bars" aria-hidden="true"></span><span class="nav-toggle-label">Menu</span>
    </button>
    <nav id="site-nav" class="site-nav" aria-label="Main">
      <ul>
        {"".join(items)}
      </ul>
    </nav>
  </div>
</header>'''


def breadcrumb(page):
    if not page["crumb"]:
        return ""
    return f'''<nav class="breadcrumb container" aria-label="Breadcrumb">
  <ol><li><a href="/">Home</a></li><li><span aria-current="page">{esc(page["crumb"])}</span></li></ol>
</nav>'''


def footer(page):
    guides = "".join(f'<li><a href="{h}">{l}</a></li>' for h, l in FOOTER_GUIDES)
    site = "".join(f'<li><a href="{h}">{l}</a></li>' for h, l in FOOTER_SITE)
    wa = page["wa"]
    float_label = {"host": "Host enquiry on WhatsApp", "agency": "Agency enquiry on WhatsApp",
                   "general": "Ask a question on WhatsApp"}[wa]
    return f'''<footer class="site-footer">
  <div class="container footer-grid">
    <div class="footer-brand">
      <a class="brand" href="/">
        <img src="/assets/images/cherry-logo.svg" width="40" height="40" alt="" loading="lazy">
        <span class="brand-name">Cherry App <span>Agency</span></span>
      </a>
      <p class="disclosure">This website provides independent Cherry App information and registration enquiries. Eligibility, earnings, commissions, and payments are subject to applicable platform terms. No income or account approval is guaranteed.</p>
    </div>
    <div>
      <h2 class="footer-heading">Guides</h2>
      <ul class="footer-links">{guides}</ul>
    </div>
    <div>
      <h2 class="footer-heading">Website</h2>
      <ul class="footer-links">{site}</ul>
    </div>
    <div>
      <h2 class="footer-heading">Enquiries</h2>
      <p class="footer-contact">WhatsApp: <a href="{WA["general"]}" target="_blank" rel="noopener">{PHONE_DISPLAY}<span class="visually-hidden"> (opens WhatsApp)</span></a></p>
      <p class="footer-small">This is the enquiry contact for this website, not Cherry&rsquo;s corporate support line. Messaging us starts an enquiry; it does not create or approve an account.</p>
    </div>
  </div>
  <div class="container footer-base">
    <p>&copy; 2026 Cherry App Agency. Content reviewed {human_date(page["reviewed"])}.</p>
  </div>
</footer>
<a class="wa-float" href="{WA[wa]}" target="_blank" rel="noopener" aria-label="{float_label} (opens WhatsApp)">
  {WA_ICON}<span class="wa-float-label" aria-hidden="true">WhatsApp</span>
</a>
<script src="/assets/js/main.js?v={ASSET_VERSION}" defer></script>
</body>
</html>
'''


def render(page):
    body = (SRC / page["src"]).read_text(encoding="utf-8")
    replacements = {
        "{{WA_HOST}}": WA["host"],
        "{{WA_AGENCY}}": WA["agency"],
        "{{WA_GENERAL}}": WA["general"],
        "{{BTN_HOST}}": wa_link("host", "Enquire About Host Registration"),
        "{{BTN_AGENCY}}": wa_link("agency", "Enquire About Agency Registration"),
        "{{BTN_GENERAL}}": wa_link("general", "Ask a Question on WhatsApp"),
        "{{BTN_GENERAL_SECONDARY}}": wa_link("general", "Ask a Question on WhatsApp", "btn btn-secondary"),
        "{{PHONE}}": f'<span class="nowrap">{PHONE_DISPLAY}</span>',
        "{{REVIEWED}}": human_date(page["reviewed"]),
        "{{REVIEWED_ISO}}": page["reviewed"],
    }
    for key, value in replacements.items():
        body = body.replace(key, value)
    if "{{" in body:
        raise SystemExit(f"Unreplaced placeholder in {page['src']}")
    return "\n".join([head(page), header(page), '<main id="main">', breadcrumb(page), body, "</main>", footer(page)])


def out_path(page):
    if page["path"].endswith(".html"):
        return OUT / page["path"].lstrip("/")
    return OUT / page["path"].lstrip("/") / "index.html"


def sitemap():
    rows = []
    for page in PAGES:
        if page.get("noindex"):
            continue
        rows.append(f"  <url>\n    <loc>{DOMAIN}{page['path']}</loc>\n    <lastmod>{page['reviewed']}</lastmod>\n  </url>")
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "\n".join(rows) + "\n</urlset>\n")


def main():
    for page in PAGES:
        target = out_path(page)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(render(page), encoding="utf-8")
        print("wrote", target.relative_to(ROOT))
    (OUT / "sitemap.xml").write_text(sitemap(), encoding="utf-8")
    print("wrote site/sitemap.xml")


if __name__ == "__main__":
    main()
