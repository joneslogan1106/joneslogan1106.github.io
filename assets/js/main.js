/* THE LOGAN GROUP — shared front-end behavior
   - draws the brass "seal" mark used as each division's logo (no image files needed)
   - mobile nav
   - scroll-reveal
   - resource/publication list loader (reads /assets/data/*.json)
*/

(function () {
  "use strict";

  /* ---------------------------------------------------------------------
     Seal renderer. Any element like:
       <div class="seal" data-letter="J" data-color="var(--acc-academy)"></div>
     becomes an inline SVG wax-seal / schematic monogram mark.
  --------------------------------------------------------------------- */
  function buildSeal(letter, color, ring) {
    const c = color || "currentColor";
    const showRing = ring !== "false";
    const ticks = [];
    for (let i = 0; i < 24; i++) {
      const a = (i / 24) * Math.PI * 2;
      const x1 = 50 + Math.cos(a) * 46;
      const y1 = 50 + Math.sin(a) * 46;
      const x2 = 50 + Math.cos(a) * (i % 2 === 0 ? 41 : 43.5);
      const y2 = 50 + Math.sin(a) * (i % 2 === 0 ? 41 : 43.5);
      ticks.push(`<line x1="${x1.toFixed(2)}" y1="${y1.toFixed(2)}" x2="${x2.toFixed(2)}" y2="${y2.toFixed(2)}" />`);
    }
    return `
      <svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" style="color:${c}">
        <g fill="none" stroke="currentColor" stroke-width="1">
          ${showRing ? `<circle cx="50" cy="50" r="48" stroke-width="1.1" />` : ""}
          ${showRing ? `<circle cx="50" cy="50" r="36" stroke-width="0.6" opacity="0.55" />` : ""}
          ${showRing ? ticks.join("") : ""}
        </g>
        <text x="50" y="59" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-size="34" font-weight="600" fill="currentColor">${letter}</text>
      </svg>`;
  }

  function paintSeals() {
    document.querySelectorAll(".seal[data-letter]").forEach((el) => {
      const letter = el.getAttribute("data-letter") || "L";
      const color = el.getAttribute("data-color");
      const ring = el.getAttribute("data-ring");
      el.innerHTML = buildSeal(letter, color, ring);
    });
  }

  /* ---------------------------------------------------------------------
     Mobile nav
  --------------------------------------------------------------------- */
  function initNav() {
    const toggle = document.querySelector(".nav-toggle");
    const panel = document.querySelector(".mobile-nav");
    if (!toggle || !panel) return;
    toggle.addEventListener("click", () => {
      const open = panel.classList.toggle("open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
      document.body.style.overflow = open ? "hidden" : "";
    });
    panel.querySelectorAll("a").forEach((a) =>
      a.addEventListener("click", () => {
        panel.classList.remove("open");
        document.body.style.overflow = "";
      })
    );
  }

  /* ---------------------------------------------------------------------
     Scroll reveal
  --------------------------------------------------------------------- */
  function initReveal() {
    const items = document.querySelectorAll(".reveal");
    if (!("IntersectionObserver" in window) || items.length === 0) {
      items.forEach((el) => el.classList.add("in-view"));
      return;
    }
    const io = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("in-view");
            io.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.12, rootMargin: "0px 0px -40px 0px" }
    );
    items.forEach((el, i) => {
      el.style.setProperty("--i", i % 8);
      io.observe(el);
    });
  }

  /* ---------------------------------------------------------------------
     Resource / publication loader
     Renders JSON entries into any [data-resource-feed="path.json"] target.
     JSON shape: [{ "title": "", "url": "", "date": "YYYY-MM-DD", "description": "" }]
     description supports a tiny markdown subset: **bold**, *italic*, [text](url)
  --------------------------------------------------------------------- */
  function mdLite(str) {
    if (!str) return "";
    let s = str
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;");
    s = s.replace(/\[([^\]]+)\]\((https?:\/\/[^\s)]+)\)/g, '<a href="$2" target="_blank" rel="noopener">$1</a>');
    s = s.replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>");
    s = s.replace(/\*([^*]+)\*/g, "<em>$1</em>");
    return s;
  }

  function formatDate(d) {
    if (!d) return "";
    const dt = new Date(d + "T00:00:00");
    if (isNaN(dt.getTime())) return d;
    return dt.toLocaleDateString(undefined, { year: "numeric", month: "long", day: "numeric" });
  }

  async function loadResourceFeeds() {
    const targets = document.querySelectorAll("[data-resource-feed]");
    for (const target of targets) {
      const src = target.getAttribute("data-resource-feed");
      try {
        const res = await fetch(src, { cache: "no-store" });
        if (!res.ok) throw new Error("feed unavailable");
        const entries = await res.json();
        if (!Array.isArray(entries) || entries.length === 0) {
          target.innerHTML = `<p class="res-empty">Nothing published here yet.</p>`;
          continue;
        }
        entries
          .slice()
          .sort((a, b) => (a.date < b.date ? 1 : -1))
          .forEach((entry) => {
            const card = document.createElement("article");
            card.className = "res-card reveal";
            const titleHtml = entry.url
              ? `<a href="${entry.url}" target="_blank" rel="noopener">${(entry.title || "Untitled").replace(/</g, "&lt;")}</a>`
              : (entry.title || "Untitled").replace(/</g, "&lt;");
            card.innerHTML = `
              <div class="meta">${formatDate(entry.date)}${entry.tag ? " · " + entry.tag : ""}</div>
              <h3>${titleHtml}</h3>
              <p>${mdLite(entry.description || "")}</p>
            `;
            target.appendChild(card);
          });
        initReveal();
      } catch (err) {
        target.innerHTML = `<p class="res-empty">Could not load this feed (${src}). If you're browsing this site locally via file://, run it through a local server — fetch() needs http(s).</p>`;
      }
    }
  }

  document.addEventListener("DOMContentLoaded", () => {
    paintSeals();
    initNav();
    initReveal();
    loadResourceFeeds();
  });

  window.TLG = { buildSeal, mdLite };
})();
