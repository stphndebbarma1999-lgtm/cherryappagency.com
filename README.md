# cherryappagency.com

Static, mobile-first website for **Cherry App Agency**: an independent Cherry App
information and registration-enquiry site for prospective hosts and agencies.

- `site/`: the finished website. Upload its contents to the web root.
- `src/pages/`: page body content (edit these).
- `tools/build.py`: wraps the page bodies in the shared layout and writes `site/`. Uses only Python 3.
- `tools/serve.py`: local preview server with real 404s.
- `tools/check-site.js`: automated link, layout, WhatsApp, SEO and keyboard checks (needs Playwright).
- `tools/make-images.js`: renders PNG icons and the social preview from the SVGs.
- `docs/DEPLOYMENT.md`: hosting, HTTPS, domain redirects, staging and Search Console steps.
- `docs/SEO-MAP.md`: page / keyword / title / H1 map.
- `docs/CONTENT-VERIFICATION.md`: sources, open factual questions and what was deliberately left out.
- `docs/ASSETS.md`: images, fonts and missing assets.

```bash
python3 tools/build.py          # rebuild site/ after editing src/pages or tools/build.py
python3 tools/serve.py 8765     # preview at http://127.0.0.1:8765/
node tools/check-site.js http://127.0.0.1:8765
```
