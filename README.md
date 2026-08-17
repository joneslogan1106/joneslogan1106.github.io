# The Logan Group — website

A static, no-build-tools site for The Logan Group and its divisions, made to run on GitHub Pages exactly as-is.

## Structure

```
index.html                    Home — mission, all divisions, governance
charter.html                  Founding Charter, Articles I–XI
jones-academy.html            Division page (generated)
logan-labs.html                "
logan-works.html               "
logan-press.html                "
logan-research.html             "
logan-infrastructure.html       "
logan-ventures.html             "
ministry.html                 The Upper Room Ministry (generated)
404.html                      Custom not-found page
robots.txt                    Disallows /tools/ from search crawlers
sitemap.xml
.nojekyll                     Tells GitHub Pages to serve files as-is
assets/css/style.css          All styling — one file
assets/js/main.js             Seal-logo renderer, nav, scroll reveal, resource feeds
assets/data/*.json            Published entries for Ministry / Press / Research
assets/img/favicon.svg        Placeholder brand mark — replace with your own
tools/publish.html            Internal markdown → hyperlink publishing tool (not linked, noindex)
build.py                      Regenerates the 7 division pages + ministry.html from one dataset
```

## Editing division content

Don't hand-edit `jones-academy.html`, `logan-labs.html`, etc. — they're generated. Open `build.py`,
edit the `DIVISIONS` list (or the `MINISTRY` dict) near the top, then run:

```bash
python3 build.py
```

This regenerates all eight pages consistently — same structure, same styling, new content.
`index.html` and `charter.html` are hand-written and safe to edit directly.

## The "logos"

Every division mark you see is not an image file — it's an inline SVG seal drawn by
`assets/js/main.js` from a single letter and an accent color (see `--acc-*` variables in
`assets/css/style.css`). That's why there's nothing to upload for them and why they stay crisp
at any size. If you'd rather use real artwork later, replace `<div class="seal" data-letter="…">`
with an `<img>` tag pointing at `assets/img/`.

## Favicon

You said you already have one. Drop it in as:

- `favicon.ico` at the repo root, and/or
- `assets/img/favicon.svg` (replacing the placeholder seal already there)

Both are already linked from every page's `<head>`.

## Publishing hyperlinks (Ministry, Press, Research)

Those three pages read from a JSON file in `assets/data/` and render each entry as a card —
no page edits needed to add a new link. To add one:

1. Open `tools/publish.html` locally (double-click it, or run a local server — see below).
2. Fill in title, link, date, tag, and a short markdown-lite description.
3. Copy the generated JSON entry.
4. Paste it into the matching array in `assets/data/ministry.json`, `press.json`, or `research.json`.
5. Commit and push. The card appears on the next deploy.

**`tools/publish.html` is intentionally not linked from any page**, and it's marked `noindex` and
disallowed in `robots.txt` so it won't turn up in search or navigation. That's obscurity, not real
security — anyone with the exact URL can still open it, because GitHub Pages can't password-protect
a page. If you want it genuinely private, don't push the `tools/` folder to the public repo at all;
keep it locally (or in a separate private repo) and only copy the JSON it generates into the public
site.

## Deploying to GitHub Pages

1. Create a new GitHub repository (or use an existing one).
2. Copy everything in this folder into the repo root (keep the folder structure as-is).
3. Commit and push to the `main` branch.
4. In the repo: **Settings → Pages → Build and deployment → Source → Deploy from a branch**,
   then pick `main` and `/ (root)`.
5. Wait a minute for the first deploy, then your site is live at
   `https://<your-username>.github.io/<repo-name>/`.

Every internal link in this site is **relative** (`index.html`, `assets/…`, and `../assets/…`
from `tools/`), not root-absolute. That matters on GitHub Pages: most repos are served at
`https://<username>.github.io/<repo-name>/`, a subpath, not the domain root — root-absolute
links (`/assets/…`) would 404 there. Relative links work at any subpath, and also work unchanged
if you later move to a custom domain.

## Previewing locally

Opening `index.html` directly in a browser works for most of the site, but the resource feeds
(Ministry/Press/Research) use `fetch()`, which browsers block on `file://` URLs. Run a tiny local
server instead:

```bash
python3 -m http.server 8000
# then open http://localhost:8000
```
