# Deployment

The site is hosted on **Vercel**, and the domain **cherryappagency.com** is registered at **Hostinger**.
Only `cherryappagency.com` (and `www.cherryappagency.com`) point at this site.
`cherryapp.agency` and `cherryappagency.in` are reserved for separate websites and are not
connected or redirected here.

Nothing below has been done for you yet. No Vercel project exists and no DNS changes
have been made. These are the steps.

## 1. Create the Vercel project

1. Go to <https://vercel.com/new> and import `stphndebbarma1999-lgtm/cherryappagency.com`.
2. Leave the framework as **Other** and don't set a build command. `vercel.json` in the repository
   already tells Vercel to serve the `site/` folder as-is, with trailing-slash URLs, a
   `/index.html` → `/` redirect, and security and caching headers.
3. Deploy. The finished site currently lives on the `claude/cherry-app-agency-website` branch, and
   `main` only has the README. Either merge that branch into `main` (recommended, so pushes to
   `main` go live) or set **Settings → Git → Production Branch** to that branch.
4. Open the `*.vercel.app` URL and check the pages. `/does-not-exist/` should show the 404 page.

Vercel serves `site/404.html` automatically for missing pages, with a real 404 status.
`site/.htaccess` is not used on Vercel. It is kept only in case you ever move to Apache hosting.

## 2. Add the domain in Vercel

In the project, open **Settings → Domains**:
1. Add `cherryappagency.com` as the **production** domain.
2. Add `www.cherryappagency.com` and set it to **Redirect to** `cherryappagency.com` (308, permanent).

Vercel then shows the DNS records it expects. Use the values Vercel shows if they differ from the ones below.

## 3. Point the domain at Vercel from Hostinger

1. Log in at **hpanel.hostinger.com** → **Domains → Domain portfolio** → **Manage** next to
   `cherryappagency.com` → **DNS / Nameservers** → **DNS records**.
   (The domain must be using Hostinger nameservers, `ns1/ns2.dns-parking.com`, for these records to apply.)
2. Delete the existing **A**, **AAAA** and **ALIAS** records for `@` and the **CNAME** record for `www`.
   Leave **MX** and **TXT** records, which handle email and verification.
3. Add:

| Type | Name | Points to | TTL |
|---|---|---|---|
| A | `@` | `76.76.21.21` | 3600 |
| CNAME | `www` | `cname.vercel-dns.com` | 3600 |

DNS usually updates within an hour, but it can take up to 48 hours. When Vercel shows
"Valid configuration", it issues the HTTPS certificate automatically.

## 4. Check it

```bash
for u in https://cherryappagency.com/ https://www.cherryappagency.com/cherry-host/ \
         https://cherryappagency.com/cherry-host https://cherryappagency.com/index.html \
         https://cherryappagency.com/nope/; do
  echo "$u -> $(curl -s -o /dev/null -w '%{http_code} %{redirect_url}' "$u")"
done
```
Expected: `200` for the homepage, `308` redirects to the matching `https://cherryappagency.com/.../`
URL for `www`, a missing slash and `/index.html`, and `404` for `/nope/`.

## 5. Staging and previews

Vercel preview deployments (`*.vercel.app` URLs for branches) are not the canonical site.
Every page's canonical tag points to `https://cherryappagency.com/...`. To keep previews private,
leave Vercel's **Deployment Protection** (Vercel Authentication) switched on for previews.

## 6. After launch: search engines

These steps need your own Google and Bing accounts:
1. In Google Search Console, add a **Domain property** for `cherryappagency.com`. Verify it with the
   DNS TXT record Google gives you, added in Hostinger's DNS editor.
2. Submit `https://cherryappagency.com/sitemap.xml`.
3. Bing Webmaster Tools can import the Search Console property.

Submitting a sitemap helps discovery but does not guarantee indexing or rankings.

## A note on the other two domains

If `cherryapp.agency` and `cherryappagency.in` become separate websites, give each one its own
content and purpose. Copying the pages from this site onto them would create duplicate content
competing with `cherryappagency.com`. Linking between the sites is fine.

## 7. Updating content later

1. Edit the page body in `src/pages/*.html` (or titles and descriptions in `tools/build.py`).
2. When the content of a page has genuinely been reviewed or changed, update that
   page's `"reviewed"` date in `tools/build.py`. It drives the visible review date,
   `dateModified` and the sitemap `lastmod`.
3. If you changed `styles.css` or `main.js`, increase `ASSET_VERSION` in `tools/build.py`.
4. Run `python3 tools/build.py`, commit and push. Vercel redeploys automatically from the production branch.
5. Optional checks: `python3 tools/serve.py 8765` in one terminal, then
   `node tools/check-site.js http://127.0.0.1:8765` (requires Playwright).

To regenerate the PNG icons and social image after changing the SVG logo or hero:
`node tools/make-images.js`, then move `site/assets/images/apple-touch-icon.png` into `site/`
and build the favicon with
`convert site/assets/images/favicon-64.png -background none -define icon:auto-resize=48,32,16 site/favicon.ico && rm site/assets/images/favicon-64.png`.

## Alternative: Apache / shared hosting

If you ever host on Apache instead (for example Hostinger web hosting), upload the **contents** of
`site/` into `public_html/`, including `.htaccess`. It sends any other host name and plain HTTP to
`https://cherryappagency.com` on the same path, adds trailing slashes, serves the 404 page and
sets caching headers. Because that rule redirects every host except `cherryappagency.com`, don't
share that `public_html` folder with the other two domains' websites.
