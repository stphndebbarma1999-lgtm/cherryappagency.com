# Deployment and redirects

Nothing in this file has been carried out yet. No DNS changes, hosting uploads,
redirects or Search Console setup have been made. These are the steps to follow.

## 1. What to upload

Upload the **contents** of the `site/` folder into the web root of the hosting account
for `cherryappagency.com` (usually `public_html/`). Include the hidden `.htaccess` file.
Do not upload `src/`, `tools/` or `docs/`.

```
public_html/
  .htaccess  404.html  index.html  robots.txt  sitemap.xml  site.webmanifest
  favicon.ico  apple-touch-icon.png
  about/  contact/  cherry-agency/  cherry-app/  cherry-earnings/
  cherry-host/  cherry-policy/  cherry-withdrawal/  assets/
```

The site is plain static HTML, CSS and a small JavaScript file. It needs no PHP,
database or Node.js on the server. The `.htaccess` file assumes Apache or LiteSpeed,
which most cPanel and hPanel shared hosts use.

## 2. HTTPS first

Install a TLS certificate for `cherryappagency.com` (and `www.cherryappagency.com`)
before you rely on the redirects. On cPanel this is usually **SSL/TLS Status → Run AutoSSL**.
On hPanel it is **Security → SSL**. Then open `https://cherryappagency.com/` and check
that the browser shows a valid certificate.

## 3. Canonical-domain redirect (already in `.htaccess`)

`site/.htaccess` sends every request that is not `https://cherryappagency.com`
to the same path on `https://cherryappagency.com` with a **301** redirect, in a single hop:

| Request | Redirects to |
|---|---|
| `http://cherryappagency.com/cherry-host/` | `https://cherryappagency.com/cherry-host/` |
| `https://www.cherryappagency.com/about/` | `https://cherryappagency.com/about/` |
| `https://cherryapp.agency/cherry-agency/` | `https://cherryappagency.com/cherry-agency/` |
| `https://cherryappagency.in/` | `https://cherryappagency.com/` |
| `/cherry-host` (no slash) | `/cherry-host/` |
| `/index.html`, `/about/index.html` | `/`, `/about/` |

Paths are preserved, so an old link to a page that exists on the main site
lands on the same page. A path that doesn't exist redirects and then shows the
real 404 page with a 404 status. It is not sent to the homepage.

If your host or CDN terminates HTTPS before Apache (some Cloudflare setups do this),
`%{HTTPS}` can always read "off" and the site will loop. If that happens, follow the
comment in `.htaccess` and use the `X-Forwarded-Proto` condition instead.

## 4. Redirecting `cherryapp.agency` and `cherryappagency.in`

Use **one** of these options for each extra domain. Do not upload a second copy
of the site to them.

### Option A: add them as alias/parked domains (simplest on shared hosting)
1. In the hosting panel, add `cherryapp.agency` and `cherryappagency.in` as
   **Aliases** (cPanel → Domains → Create a New Domain, with "Share document root"
   ticked) or **Parked domains** (hPanel), pointing at the same `public_html`.
2. At each domain's registrar, point DNS at the host: either use the host's nameservers,
   or set an `A` record for `@` and `www` to the hosting server's IP address.
3. Issue TLS certificates for both domains (AutoSSL normally covers aliases), so that
   `https://cherryapp.agency/...` doesn't show a certificate warning before redirecting.
4. The existing `.htaccess` rule then 301-redirects them, path for path.

### Option B: registrar or DNS-level forwarding
If the registrar offers URL forwarding, set **permanent (301) forwarding** to
`https://cherryappagency.com` with **"forward path" / "path forwarding" enabled**.
Turn off "masking" or "frame forwarding". It hides the real URL and is bad for search engines.

### Option C: Cloudflare (if the domains use Cloudflare DNS)
Create a **Redirect Rule** (Rules → Redirect Rules) for each zone:
- When: hostname equals `cherryapp.agency` or `www.cherryapp.agency`
- Then: dynamic redirect to `concat("https://cherryappagency.com", http.request.uri.path)`,
  status **301**, preserve query string.
Each hostname needs a proxied (orange-cloud) DNS record, for example `A @ 192.0.2.1`,
so that Cloudflare receives the request.

### Nginx equivalent (if you ever move off Apache)
```nginx
server {
  listen 80; listen 443 ssl;
  server_name www.cherryappagency.com cherryapp.agency www.cherryapp.agency
              cherryappagency.in www.cherryappagency.in;
  # ssl_certificate ... (a certificate covering these names)
  return 301 https://cherryappagency.com$request_uri;
}
server {
  listen 443 ssl; server_name cherryappagency.com;
  root /var/www/cherryappagency.com/site;
  error_page 404 /404.html;
  location / { try_files $uri $uri/ =404; }
}
```

### Check the redirects after setup
```bash
for u in http://cherryappagency.com/ https://www.cherryappagency.com/cherry-host/ \
         https://cherryapp.agency/cherry-agency/ https://cherryappagency.in/about/ \
         https://cherryappagency.com/cherry-host https://cherryappagency.com/nope/; do
  echo "$u -> $(curl -s -o /dev/null -w '%{http_code} %{redirect_url}' "$u")"
done
```
Expected: one `301` per redirect to the matching `https://cherryappagency.com/...`
path, `200` for real pages, and `404` for `/nope/`.

## 5. Staging

If you put a copy online for review before launch, keep it out of search results
**and** private:
- Protect the staging folder with a password (cPanel → Directory Privacy). `robots.txt`
  is not access control.
- Add `Header set X-Robots-Tag "noindex, nofollow"` to the staging `.htaccess`.
- Remove or edit the host-name redirect rule in the staging `.htaccess`. Otherwise it
  will redirect the staging site to production.

## 6. After launch: search engines

These steps need your own Google and Bing accounts:
1. Google Search Console → add a **Domain property** for `cherryappagency.com`
   (verified with a DNS TXT record at the registrar).
2. Submit `https://cherryappagency.com/sitemap.xml`.
3. Optionally add `cherryapp.agency` and `cherryappagency.in` as properties too, to
   watch for crawl errors on the redirects.
4. Bing Webmaster Tools can import the Search Console property.

Submitting a sitemap helps discovery but does not guarantee indexing or rankings.

## 7. Updating content later

1. Edit the page body in `src/pages/*.html` (or titles and descriptions in `tools/build.py`).
2. When the content of a page has genuinely been reviewed or changed, update that
   page's `"reviewed"` date in `tools/build.py`. It drives the visible review date,
   `dateModified` and the sitemap `lastmod`.
3. If you changed `styles.css` or `main.js`, increase `ASSET_VERSION` in `tools/build.py`.
4. Run `python3 tools/build.py` and upload the changed files from `site/`.
5. Optional checks: `python3 tools/serve.py 8765` in one terminal, then
   `node tools/check-site.js http://127.0.0.1:8765` (requires Playwright).

To regenerate the PNG icons and social image after changing the SVG logo or hero:
`node tools/make-images.js`, then move `site/assets/images/apple-touch-icon.png` into `site/`
and build the favicon with
`convert site/assets/images/favicon-64.png -background none -define icon:auto-resize=48,32,16 site/favicon.ico && rm site/assets/images/favicon-64.png`.

## 8. Optional hardening once HTTPS is stable

Uncomment the `Strict-Transport-Security` line in `.htaccess` only after you are sure
every hostname that reaches the site has a working certificate.
