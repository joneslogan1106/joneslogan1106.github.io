# The Logan Group — GitHub Pages Website

This version is designed specifically for GitHub Pages.

## Important architecture

Only the `site/` folder is deployed publicly.

The Markdown source lives in `content/`, and the local build script converts it into `site/assets/content-manifest.js`.

The `tools/` folder is NOT deployed. There is no public Admin page.

## Publishing a new Markdown document

1. Create a `.md` file in `content/`.
2. Add front matter:

---
title: "Your Title"
slug: "your-title"
category: "Ministry"
division: "upper-room"
description: "Short description."
---

# Your Title

Your content.

[Read something](https://example.com)

3. Commit and push to GitHub.
4. GitHub Actions automatically builds the Markdown and deploys the site.

The `division` field is optional. Supported division IDs:
- upper-room
- jones-academy
- logan-labs
- logan-works
- logan-press
- logan-research
- logan-infrastructure
- logan-ventures

If `division` is supplied, the document is also shown on that division's page.

## GitHub Pages setup

Push this repository to GitHub with `main` as the branch.

Then go to:
Settings → Pages → Source → GitHub Actions

The included workflow handles the deployment.

## Images

Division hero artwork is stored in `site/assets/divisions/`.

Replace those SVG files with your actual company/ministry logos or branded artwork whenever you have them. SVG is ideal for logos because it stays sharp at every size.

## Favicon

Replace `site/assets/logo.svg` or update the favicon link in `site/index.html` with your existing favicon.

## Why there is no public admin page

A static GitHub Pages site cannot securely provide a publishing dashboard. Anything shipped to `site/` is public.

Instead, TLG uses a GitHub-native content workflow:
Markdown → Git commit → GitHub Action → published page.

That is safer, version-controlled, and fits the institutional/documentation philosophy of TLG.
