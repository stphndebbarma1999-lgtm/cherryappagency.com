# Assets

## Used on the site

| File | What it is | Origin |
|---|---|---|
| `site/assets/images/cherry-logo.svg` | Two connected cherries, green stems and leaf, transparent background | Hand-drawn SVG made for this build |
| `site/assets/images/favicon.svg` | Same mark, used as the SVG favicon | Copy of the logo |
| `site/assets/images/cherry-logo.png` | 512×512 transparent PNG (used for the Organization logo) | Rendered from the SVG |
| `site/favicon.ico` | 16/32/48 px icon | Rendered from the SVG |
| `site/apple-touch-icon.png`, `assets/images/icon-192.png`, `icon-512.png` | Touch and manifest icons on white | Rendered from the SVG |
| `site/assets/images/cherry-hero.svg` | Flat illustration: an adult woman on a smartphone video call, with cherries on soft pink. No text in the image | Hand-drawn SVG made for this build |
| `site/assets/images/cherry-social-preview.png` | 1200×630 Open Graph image: logo, wordmark, tagline and hero illustration | Rendered from the SVGs |
| `site/assets/fonts/barlow-condensed-700.woff2` | Heading font, Latin subset | Barlow Condensed (SIL Open Font License, see `OFL-barlow-condensed.txt`), self-hosted |

The wordmark "Cherry App Agency" is live text, not an image. Body text uses the
device's system font, so no extra download is needed.

## Missing standalone assets

None of the brief's supplied files were in the repository: the AI-created two-cherry
logo, the AI hero image, the design mockups, "Recruiting Policy - Cherry.pdf" and the
salary-plan image.

An AI hero image could not be generated either. The connected Higgsfield account
had 0 credits, and an image costs 0.25 credits.

The SVG logo and illustration above are honest stand-ins. They are drawn
illustrations, not photographs, and they don't depict a real host or employee.
To use the intended AI assets:

1. Save the logo as `site/assets/images/cherry-logo.svg` (best) or as a transparent PNG.
   If you use a PNG, update the `<img src>` in `tools/build.py` and the CSS background in `styles.css`.
2. Save the hero as `site/assets/images/cherry-hero.webp` at about 1280×1440 (an 8:9 ratio)
   plus a 640×720 version. In `src/pages/home.html`, replace the hero `<img>` with
   `srcset="/assets/images/cherry-hero-640.webp 640w, /assets/images/cherry-hero.webp 1280w"`,
   keep `width`/`height`, keep `fetchpriority="high"` and don't add `loading="lazy"`.
   Update the alt text to describe the new image.
3. Run `node tools/make-images.js` to refresh the PNG icons and social image, then rebuild.

The social preview is a PNG rather than WebP, because some social platforms
still don't render WebP previews reliably.
