#!/usr/bin/env python3
"""Generates the static HTML pages for The Logan Group site.
Run with: python3 build.py
Edit the DIVISIONS data below (or the hero copy) and re-run to regenerate.
"""
import os, re

ROOT = os.path.dirname(os.path.abspath(__file__))

NAV_LINKS = [
    ("index.html", "Home"),
    ("charter.html", "Charter"),
    ("index.html#divisions", "Divisions"),
    ("ministry.html", "Ministry"),
]

CONTACT_FOOTER_COLUMN = """<div>
          <h4>Contact</h4>
          <ul>
            <li><a href="https://github.com/joneslogan1106" target="_blank" rel="noopener">GitHub</a></li>
            <li><a href="mailto:loganjones110613@gmail.com">Email</a></li>
            <li><a href="https://www.instagram.com/loeasy68" target="_blank" rel="noopener">Instagram</a></li>
            <li><a href="https://wa.me/12404995414" target="_blank" rel="noopener">WhatsApp</a></li>
          </ul>
        </div>"""

DIVISIONS = [
    {
        "slug": "jones-academy",
        "article": "Article XII",
        "name": "Jones Academy",
        "role": "Flagship Educational Institution",
        "accent": "var(--acc-academy)",
        "letter": "J",
        "tagline": "Free education is a right. Advanced mastery is a premium.",
        "mission": "Jones Academy provides universal, high-quality education at no cost, organized into four schools modeled on a modern research university. Long-term operation is sustained only through optional, advanced tools that enhance — but never gate — access to knowledge.",
        "purpose": [
            "Design curriculum with the rigor of a research university, not a course platform",
            "Keep every core subject free and permanently accessible",
            "Fund continued operation through optional Mastery Tools, never through paywalls on fundamentals",
        ],
        "scope_title": "Four Schools",
        "scope": [
            ("School of Mathematics & Logic", "Algebra through analysis, discrete mathematics, statistics, logic, and mathematical physics."),
            ("School of Applied Science & Engineering", "Physics, chemistry, biology, and computer science taught through computational, systems-based methods."),
            ("School of Humanities & Social Sciences", "History, philosophy, psychology, economics, political science, and religious & ethical studies."),
            ("School of Languages, Arts & Skillcraft", "World languages, fine arts, and practical, technical craft."),
        ],
        "relationships": [
            ("Logan Labs", "logan-labs.html", "Supplies real engineering artifacts as teaching material for applied courses."),
            ("Logan Press", "logan-press.html", "Formally publishes Academy-authored papers, textbooks, and course notes."),
            ("The Upper Room Ministry", "ministry.html", "Handles academic religious studies; the Academy studies faith as a discipline, the Ministry practices it."),
        ],
        "vision": [
            ("Now", "Private, self-directed institute — depth and documentation over scale."),
            ("Near-term", "A public library of free coursework across all four schools."),
            ("Long-term", "A globally accessible digital university and permanent knowledge institution."),
        ],
        "resources": None,
        "active": True,
    },
    {
        "slug": "logan-labs",
        "article": "Article XIII",
        "name": "Logan Labs",
        "role": "Engineering & Systems Research Platform",
        "accent": "var(--acc-labs)",
        "letter": "L",
        "tagline": "Durable engineering artifacts, not tutorials.",
        "mission": "Logan Labs designs, implements, and documents software systems, programming languages, tools, and research artifacts that demonstrate real technical depth. Where the Academy teaches theory, Labs builds the systems that prove it out.",
        "purpose": [
            "Turn language and systems study into working, documented software",
            "Operate as a technical research laboratory, not a portfolio of demos",
            "Study computing from a systems-first philosophy — compilers, operating systems, tooling",
        ],
        "scope_title": "Active Research Lines",
        "scope": [
            ("Systems Engineering & Infrastructure", "Build-Your-Own-X projects: interpreters, databases, schedulers, and internal tooling."),
            ("Aeronautics & Aerospace Systems", "A dedicated division studying flight dynamics, propulsion, and aerospace computing alongside the core lab."),
            ("Languages & Paradigms", "Comparative study of programming languages and computational paradigms."),
            ("Infrastructure Research", "Tooling and internal platforms later handed to Logan Infrastructure to operate."),
        ],
        "relationships": [
            ("Jones Academy", "jones-academy.html", "Labs projects become case studies and teaching material for applied courses."),
            ("Logan Works", "logan-works.html", "Labs supplies engines, tools, and frameworks that Works ships as real products."),
            ("Logan Infrastructure", "logan-infrastructure.html", "Infrastructure operates and hardens what Labs prototypes."),
        ],
        "vision": [
            ("Now", "Systems programming and aerospace research, documented as formal artifacts."),
            ("Near-term", "A public technical repository demonstrating engineering depth."),
            ("Long-term", "A research laboratory bridging computer science and aerospace systems."),
        ],
        "resources": None,
        "active": True,
    },
    {
        "slug": "logan-works",
        "article": "Article XIV",
        "name": "Logan Works",
        "role": "Application & Game Studio",
        "accent": "var(--acc-works)",
        "letter": "W",
        "tagline": "Research → Education → Product → Feedback.",
        "mission": "Logan Works builds and ships applications and games that put technical knowledge and systems thinking in front of real users. Nothing ships without documentation, testing, and reflection.",
        "purpose": [
            "Turn research and learning into software people actually use",
            "Treat user experience as a design constraint, not an afterthought",
            "Feed real-world usage data back into research and education",
        ],
        "scope_title": "Product Lines",
        "scope": [
            ("Applications", "Educational apps, productivity tools, data-visualization tools, and utilities."),
            ("Games", "Educational, simulation-based, and systems-driven games and experimental interactive media."),
            ("Platforms", "Web, desktop, mobile, and cross-platform builds — the stack follows the product, not the trend."),
        ],
        "relationships": [
            ("Logan Labs", "logan-labs.html", "Supplies engines, frameworks, and low-level tooling."),
            ("Jones Academy", "jones-academy.html", "Uses Works' shipped products directly as learning material."),
            ("Logan Press", "logan-press.html", "Receives product documentation and post-mortems for formal archive."),
        ],
        "vision": [
            ("Now", "Private or educational builds — no aggressive marketing."),
            ("Near-term", "A small catalog of tested, documented applications and games."),
            ("Long-term", "A professional studio bridging research and real-world impact."),
        ],
        "resources": None,
        "active": True,
    },
    {
        "slug": "logan-press",
        "article": "Article XV",
        "name": "Logan Press",
        "role": "Publishing & Documentation Arm",
        "accent": "var(--acc-press)",
        "letter": "P",
        "tagline": "The permanent, citable record of everything The Logan Group produces.",
        "mission": "Logan Press formally publishes, preserves, and distributes the intellectual work produced across every division — white papers, research notes, textbooks, and engineering post-mortems — to a standard of long-term archival quality.",
        "purpose": [
            "Hold every division to the same standard of sourcing and structure",
            "Preserve work against loss, in formats built to outlast their format (LaTeX, plain text, open archives)",
            "Give the whole organization one publishing arm, not seven inconsistent ones",
        ],
        "scope_title": "What Logan Press Publishes",
        "scope": [
            ("Academic White Papers", "History, science, geography, and economics papers built on the standard LaTeX templates."),
            ("Research Notes & Technical Reports", "Findings from Logan Research fellowships and Logan Labs projects."),
            ("Textbooks & Learning Materials", "Longer-form instructional works originating in Jones Academy."),
            ("Engineering Documentation", "Post-mortems and technical write-ups from Logan Works and Logan Labs."),
        ],
        "relationships": [
            ("Logan Research", "logan-research.html", "Fellows are expected to publish findings through Press."),
            ("Jones Academy", "jones-academy.html", "Supplies instructional content for formal publication."),
            ("Logan Labs", "logan-labs.html", "Supplies research and technical work for the archive."),
        ],
        "vision": [
            ("Now", "Internal archive of white papers and technical reports."),
            ("Near-term", "A public-facing, citable repository."),
            ("Long-term", "A formal academic press recognized by educational institutions."),
        ],
        "resources": "assets/data/press.json",
        "active": True,
    },
    {
        "slug": "logan-research",
        "article": "Article XVI",
        "name": "Logan Research",
        "role": "Research Programs & Fellowships",
        "accent": "var(--acc-research)",
        "letter": "R",
        "tagline": "Structured inquiry, not scattered curiosity.",
        "mission": "Logan Research cultivates deep, structured inquiry across mathematics, science, engineering, and history. Every project runs as a formal proposal with milestones, a conclusion, and an honest account of its limitations.",
        "purpose": [
            "Prepare participants for university-level and doctoral research",
            "Require reflection and stated limitations as a mandatory part of every project — not just results",
            "Route every finished finding through Logan Press for formal publication",
        ],
        "scope_title": "How Research Runs",
        "scope": [
            ("Tracks by Discipline", "Independent research tracks opened per subject area as questions warrant."),
            ("The Fellowship Model", "Participants operate as Research Fellows, with the same expectations as any working researcher."),
            ("Formal Proposals", "Every project states its question, method, and milestones before work begins."),
            ("Peer Review", "Internal review always; external review where feasible."),
        ],
        "relationships": [
            ("Logan Press", "logan-press.html", "The required publication venue for finished findings."),
            ("Jones Academy", "jones-academy.html", "Research questions often originate from Academy coursework."),
        ],
        "vision": [
            ("Now", "Fellowship-model research tracks documented internally."),
            ("Near-term", "A small, citable body of finished, peer-reviewed findings."),
            ("Long-term", "A track record built for doctoral-level admission and scholarly contribution."),
        ],
        "resources": "assets/data/research.json",
        "active": True,
    },
    {
        "slug": "logan-infrastructure",
        "article": "Article XVII",
        "name": "Logan Infrastructure",
        "role": "Internal Systems & Operations",
        "accent": "var(--acc-infra)",
        "letter": "I",
        "tagline": "The backbone. Reliability over novelty.",
        "mission": "Logan Infrastructure designs, maintains, and documents the technical and organizational systems that keep every other division running — from version control to build pipelines to knowledge management.",
        "purpose": [
            "Keep documentation ahead of convenience, always",
            "Choose scalable systems over short-term optimizations",
            "Prevent institutional fragility as the organization grows",
        ],
        "scope_title": "What It Maintains",
        "scope": [
            ("Internal Tooling", "Automation pipelines, internal software, and developer tooling shared across divisions."),
            ("Data & File Systems", "Organization standards for files, data, and version control."),
            ("Build & Deployment", "Testing and deployment workflows for anything the other divisions ship."),
            ("Knowledge Management", "The systems that keep documentation findable and durable."),
        ],
        "relationships": [
            ("Logan Labs", "logan-labs.html", "Provides and hardens development environments."),
            ("Logan Press", "logan-press.html", "Maintains the archival systems Press depends on."),
        ],
        "vision": [
            ("Now", "Documentation standards and internal tooling."),
            ("Near-term", "Automated pipelines shared across every division."),
            ("Long-term", "A backbone durable enough to outlast any single project on top of it."),
        ],
        "resources": None,
        "active": True,
    },
    {
        "slug": "logan-ventures",
        "article": "Article XIX",
        "name": "Logan Ventures",
        "role": "Future Commercialization & Partnerships",
        "accent": "var(--acc-ventures)",
        "letter": "V",
        "tagline": "Dormant by design, not by neglect.",
        "mission": "Logan Ventures is the future-facing division responsible for commercial expansion, spin-offs, and external partnerships. It remains deliberately inactive while the Founder is a minor, and will only activate on legal eligibility, institutional maturity, and formal Charter review.",
        "purpose": [
            "Hold space for future licensing, partnerships, and spin-off entities",
            "Guarantee commercial activity never compromises educational access or research integrity",
            "Activate only through a deliberate, reviewed decision — never by default",
        ],
        "scope_title": "Future Scope (Inactive)",
        "scope": [
            ("Spin-Off Companies", "Formal entities that may emerge from mature divisions."),
            ("Licensing Agreements", "Licensing of tools, research, or educational material."),
            ("Strategic Partnerships", "External collaborations aligned with the Charter's mission."),
            ("Mission-Aligned Investment", "Capital directed only toward efforts consistent with Article II."),
        ],
        "relationships": [
            ("The Logan Group (Parent)", "charter.html", "Ventures may only activate under direct Charter review and guardian consent."),
        ],
        "vision": [
            ("Now", "Fully dormant. No commercial activity of any kind."),
            ("Trigger", "Activates upon legal eligibility and Charter review."),
            ("Long-term", "Commercial arm that funds the mission without ever governing it."),
        ],
        "resources": None,
        "active": False,
    },
]

MINISTRY = {
    "slug": "ministry",
    "article": "Addendum · Article XXI",
    "name": "The Upper Room Ministry",
    "role": "Spiritual & Devotional Arm",
    "accent": "var(--acc-ministry)",
    "letter": "U",
    "tagline": "The engine that gives the whole system its \u201cwhy.\u201d",
    "mission": "The Upper Room Ministry provides daily scriptural teaching, theological reflection, and spiritual discipline grounded in a non-denominational Christian tradition — serving as both personal practice and public ministry. It is the ethical foundation the rest of The Logan Group is built on, kept clearly separate from academic study of religion.",
    "purpose": [
        "Maintain a non-negotiable daily devotional practice",
        "Publish sermons, reflections, and theological writing to a public audience",
        "Provide the moral and ethical framework the other divisions operate within",
        "Build community, starting from a local network and growing deliberately",
    ],
    "scope_title": "Daily Rhythm",
    "scope": [
        ("Morning Study", "Scripture and commentary — roughly twenty minutes, before academic or work sessions begin."),
        ("Reflection", "Personal application of that morning's study."),
        ("Recording / Writing", "The sermon or devotional itself is produced."),
        ("Publishing", "Shared to the ministry platform and, where relevant, social media."),
    ],
    "relationships": [
        ("Jones Academy", "jones-academy.html", "Handles academic religious studies — comparative religion and theology as a discipline — kept distinct from devotional practice here."),
        ("Logan Press", "logan-press.html", "Publishes formal theological papers and research that grow out of this ministry."),
    ],
    "vision": [
        ("Phase 1 — Now", "Personal practice and a simple digital presence, integrated into the daily system."),
        ("Phase 2 — College Years", "Leading a small group, formal teaching curriculum, higher-production content."),
        ("Phase 3 — Post-College", "Possible 501(c)(3) incorporation, publishing partnerships, and speaking."),
        ("Phase 4 — Long-Term", "A recognized spiritual pillar of The Logan Group, cross-pollinating with Academy religious studies and Press theological research."),
    ],
    "resources": "assets/data/ministry.json",
    "active": True,
    "guardrails": [
        "Stay grounded in core, historic Christian conviction without tying it to any single denomination",
        "Keep devotional application distinct from academic study",
        "Avoid sectarian polemics that would narrow the ministry's reach",
        "Lead with humility — \u201chere's what I'm learning,\u201d not \u201chere's absolute truth\u201d",
        "Ministry funds are never drawn from investment layers, and never the reverse",
    ],
}

ALL_PAGES_FOR_NAV = DIVISIONS + [MINISTRY]


def seal(letter, color="var(--brass)", size=40, ring="true"):
    return f'<div class="seal" data-letter="{letter}" data-color="{color}" data-ring="{ring}" style="width:{size}px;height:{size}px"></div>'


def nav_html(active_href):
    items = []
    for href, label in NAV_LINKS:
        current = ' aria-current="page"' if href == active_href else ""
        items.append(f'<li><a href="{href}"{current}>{label}</a></li>')
    return "\n          ".join(items)


def mobile_nav_html(active_href):
    items = []
    for href, label in NAV_LINKS:
        items.append(f'<li><a href="{href}">{label}</a></li>')
    return "\n          ".join(items)


def header_html(active_href, root="."):
    return f"""  <header class="site-header">
    <div class="wrap">
      <a class="brand" href="{root}/index.html">
        {seal("L", "var(--brass)", 34)}
        <span class="brand-name">The Logan Group<small>Est. Charter v1.0</small></span>
      </a>
      <nav class="main-nav" aria-label="Primary">
        <ul>
          {nav_html(active_href)}
        </ul>
      </nav>
      <button class="nav-toggle" aria-label="Toggle menu" aria-expanded="false">
        <span></span><span></span><span></span>
      </button>
    </div>
  </header>
  <div class="mobile-nav" aria-label="Mobile">
    <ul>
      {mobile_nav_html(active_href)}
    </ul>
  </div>"""


def footer_html(root="."):
    div_links = "\n          ".join(
        f'<li><a href="{d["slug"]}.html">{d["name"]}</a></li>' for d in DIVISIONS
    )
    return f"""  <footer class="site-footer">
    <div class="wrap">
      <div class="footer-grid footer-grid-5">
        <div>
          {seal("L", "var(--brass)", 36)}
          <p style="margin-top:14px;max-width:34ch;">The Logan Group unifies education, research, and engineering into one disciplined, long-term system. Charter v1.0 &mdash; pre-incorporation, guardian-overseen.</p>
        </div>
        <div>
          <h4>Divisions</h4>
          <ul>
            {div_links}
          </ul>
        </div>
        <div>
          <h4>Organization</h4>
          <ul>
            <li><a href="{root}/index.html">Home</a></li>
            <li><a href="{root}/charter.html">Founding Charter</a></li>
            <li><a href="{root}/ministry.html">The Upper Room Ministry</a></li>
          </ul>
        </div>
        <div>
          <h4>Principles</h4>
          <ul>
            <li>Learning first</li>
            <li>Depth over breadth</li>
            <li>Documentation as proof</li>
            <li>No burnout, no leverage</li>
          </ul>
        </div>
        {CONTACT_FOOTER_COLUMN}
      </div>
      <hr class="rule" />
      <div class="footer-bottom" style="margin-top:22px;">
        <span>&copy; <span id="year"></span> The Logan Group &mdash; private academic organization</span>
        <span>Charter v1.0</span>
      </div>
    </div>
  </footer>"""


def page_shell(title, description, active_href, accent, body, extra_head=""):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{title} — The Logan Group</title>
<meta name="description" content="{description}" />
<link rel="icon" href="favicon.ico" sizes="any" />
<link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml" />
<link rel="apple-touch-icon" href="assets/img/apple-touch-icon.png" />
<link rel="stylesheet" href="assets/css/style.css" />
<meta property="og:title" content="{title} — The Logan Group" />
<meta property="og:description" content="{description}" />
<meta property="og:type" content="website" />
{extra_head}
</head>
<body style="--accent:{accent}">
{header_html(active_href)}
{body}
{footer_html()}
<script>document.getElementById('year').textContent = new Date().getFullYear();</script>
<script src="assets/js/main.js"></script>
</body>
</html>
"""


def division_body(d):
    purpose_items = "\n            ".join(f"<li>{p}</li>" for p in d["purpose"])
    scope_cards = "\n        ".join(
        f"""<div class="card reveal" style="--i:{i}">
          <div class="num">{str(i+1).zfill(2)}</div>
          <h3>{name}</h3>
          <p>{desc}</p>
        </div>"""
        for i, (name, desc) in enumerate(d["scope"])
    )
    rel_items = "\n          ".join(
        f"""<li><span class="k">{name}</span><span class="v">{desc} <a href="{href}" style="color:var(--accent);text-decoration:none;border-bottom:1px solid currentColor;">Visit &rarr;</a></span></li>"""
        for name, href, desc in d["relationships"]
    )
    vision_items = "\n        ".join(
        f"""<li><div class="phase">{phase}</div><p style="margin:0;">{desc}</p></li>"""
        for phase, desc in d["vision"]
    )

    resources_block = ""
    if d["resources"]:
        resources_block = f"""
  <section>
    <div class="wrap">
      <div class="section-head reveal">
        <div class="eyebrow">Published</div>
        <h2>Latest from {d['name']}</h2>
        <p>Entries added through the internal publishing tool appear here automatically.</p>
      </div>
      <div data-resource-feed="{d['resources']}"></div>
    </div>
  </section>"""

    other_divisions = [x for x in DIVISIONS if x["slug"] != d["slug"]]
    chips = "\n        ".join(
        f'<a class="tag" href="{o["slug"]}.html" style="color:{o["accent"]};text-decoration:none;margin:0 8px 8px 0;">{o["name"]}</a>'
        for o in other_divisions
    )

    inactive_note = ""
    if not d["active"]:
        inactive_note = f"""<div class="tag" style="margin-bottom:18px;">Currently dormant</div>"""

    return f"""
  <section class="hero">
    <div class="wrap grid cols-2" style="align-items:center;">
      <div class="reveal">
        <div class="article-no">{d['article']} &mdash; The Logan Group Founding Charter</div>
        <div class="eyebrow">{d['role']}</div>
        {inactive_note}
        <h1>{d['name']}</h1>
        <p class="lede">{d['tagline']}</p>
        <p>{d['mission']}</p>
        <a class="btn primary" href="charter.html">Read the full Charter</a>
      </div>
      <div class="hero-seal-wrap reveal" style="--i:1">
        {seal(d['letter'], d['accent'], 220)}
      </div>
    </div>
  </section>

  <hr class="rule" />

  <section>
    <div class="wrap">
      <div class="section-head reveal">
        <div class="eyebrow">Purpose</div>
        <h2>Why {d['name']} exists</h2>
      </div>
      <ul class="kv-list reveal">
        {"".join(f'<li><span class="k">{"0"+str(i+1)}</span><span class="v">{p}</span></li>' for i, p in enumerate(d["purpose"]))}
      </ul>
    </div>
  </section>

  <section style="background:var(--cream-ink);border-top:1px solid var(--paper-line);border-bottom:1px solid var(--paper-line);">
    <div class="wrap">
      <div class="section-head reveal">
        <div class="eyebrow">Scope</div>
        <h2>{d['scope_title']}</h2>
      </div>
      <div class="grid cols-2 reveal-stagger">
        {scope_cards}
      </div>
    </div>
  </section>

  <section>
    <div class="wrap">
      <div class="section-head reveal">
        <div class="eyebrow">Relationships</div>
        <h2>How {d['name']} connects to the rest of the Group</h2>
      </div>
      <ul class="kv-list reveal">
        {rel_items}
      </ul>
    </div>
  </section>

  <section class="dark">
    <div class="wrap">
      <div class="section-head reveal">
        <div class="eyebrow" style="--accent:{d['accent']}">Long-Term Vision</div>
        <h2>Where {d['name']} is going</h2>
      </div>
      <ul class="timeline reveal" style="--accent:{d['accent']}">
        {vision_items}
      </ul>
    </div>
  </section>
{resources_block}
  <section>
    <div class="wrap reveal">
      <div class="eyebrow">Other Divisions</div>
      <div>{chips}</div>
    </div>
  </section>
"""


def build_division_page(d):
    body = division_body(d)
    html = page_shell(
        title=d["name"],
        description=d["mission"][:155],
        active_href="index.html#divisions",
        accent=d["accent"],
        body=body,
    )
    with open(os.path.join(ROOT, f"{d['slug']}.html"), "w") as f:
        f.write(html)


def build_ministry_page():
    d = MINISTRY
    body = division_body(d)
    guard_items = "\n        ".join(f"<li>{g}</li>" for g in d["guardrails"])
    guard_section = f"""
  <section style="background:var(--cream-ink);border-top:1px solid var(--paper-line);">
    <div class="wrap">
      <div class="section-head reveal">
        <div class="eyebrow" style="--accent:{d['accent']}">Guardrails</div>
        <h2>Boundaries this ministry keeps</h2>
      </div>
      <ul class="kv-list reveal">
        {"".join(f'<li><span class="k">Rule {str(i+1).zfill(2)}</span><span class="v">{g}</span></li>' for i, g in enumerate(d["guardrails"]))}
      </ul>
    </div>
  </section>"""
    body = body.replace("<section>\n    <div class=\"wrap reveal\">\n      <div class=\"eyebrow\">Other Divisions</div>", guard_section + "\n\n  <section>\n    <div class=\"wrap reveal\">\n      <div class=\"eyebrow\">Other Divisions</div>")
    html = page_shell(
        title=d["name"],
        description=d["mission"][:155],
        active_href="ministry.html",
        accent=d["accent"],
        body=body,
    )
    with open(os.path.join(ROOT, "ministry.html"), "w") as f:
        f.write(html)


if __name__ == "__main__":
    for d in DIVISIONS:
        build_division_page(d)
    build_ministry_page()
    print("Built:", ", ".join(d["slug"] + ".html" for d in DIVISIONS), "ministry.html")