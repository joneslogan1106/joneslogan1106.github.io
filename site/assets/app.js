const $=s=>document.querySelector(s);
const esc=s=>String(s??"").replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
function md(src){
 let s=esc(src).replace(/\r/g,"");
 s=s.replace(/```([\s\S]*?)```/g,(_,x)=>`<pre><code>${x.trim()}</code></pre>`);
 s=s.replace(/^### (.*)$/gm,"<h3>$1</h3>").replace(/^## (.*)$/gm,"<h2>$1</h2>").replace(/^# (.*)$/gm,"<h1>$1</h1>");
 s=s.replace(/^> (.*)$/gm,"<blockquote>$1</blockquote>");
 s=s.replace(/^\- (.*)$/gm,"<li>$1</li>").replace(/(<li>.*<\/li>\n?)+/g,x=>`<ul>${x}</ul>`);
 s=s.replace(/\[([^\]]+)\]\(([^)]+)\)/g,(m,t,u)=>`<a href="${u}" ${u.startsWith("http")?'target="_blank" rel="noopener"':''}>${t}</a>`);
 s=s.replace(/\*\*(.*?)\*\*/g,"<strong>$1</strong>").replace(/\*(.*?)\*/g,"<em>$1</em>").replace(/`([^`]+)`/g,"<code>$1</code>");
 return s.split(/\n{2,}/).map(x=>/^<(h|ul|pre|blockquote)/.test(x.trim())?x:`<p>${x.replace(/\n/g,"<br>")}</p>`).join("");
}
function header(){
return `<header class="topbar"><div class="shell nav"><a class="brand" href="#/">THE <span>LOGAN</span> GROUP</a><nav class="navlinks"><a href="#/">Home</a><a href="#/about">About</a><a href="#/divisions">Divisions</a><a href="#/library">Library</a></nav><button class="menu" onclick="this.previousElementSibling.style.display='flex'">☰</button></div></header>`;
}
function footer(){return `<footer class="footer"><div class="shell">© ${new Date().getFullYear()} The Logan Group · Learning · Depth · Integrity · Long-term thinking</div></footer>`}
function card(d){return `<a class="card reveal" href="#/${d.id}"><img class="card-image" src="${esc(d.image)}" alt="${esc(d.name)}"><div class="card-body"><span class="pill">${esc(d.type)} · ${esc(d.status)}</span><h3>${esc(d.name)}</h3><div class="muted">${esc(d.tagline)}</div></div></a>`}
function home(){
return `${header()}<main class="page-transition"><section class="hero shell"><div class="eyebrow">An integrated institution</div><h1>Build deeply.<br>Document everything.</h1><p>${esc(TLG.mission)}</p><div class="actions"><a class="btn primary" href="#/divisions">Explore the Group</a><a class="btn" href="#/library">Open Library</a></div></section><section class="section shell"><div class="eyebrow">The architecture</div><h2>One institution. Many disciplines.</h2><p class="section-lead">Education, research, engineering, publishing, ministry, infrastructure, and future ventures operate as complementary parts of one system.</p><div class="grid">${TLG.divisions.map(card).join("")}</div></section><section class="section shell"><div class="quote">“Research → Education → Product → Feedback.”</div><p class="section-lead">The divisions are designed to reinforce one another rather than exist as isolated projects.</p></section><section class="section shell"><div class="eyebrow">Operating principles</div><h2>How TLG works.</h2><div class="principles">${TLG.principles.map(p=>`<div class="principle reveal"><b>${esc(p[0])}</b><span class="muted">${esc(p[1])}</span></div>`).join("")}</div></section></main>${footer()}`;
}
function divisions(){return `${header()}<main class="section shell page-transition"><div class="eyebrow">The organization</div><h1 style="font:700 58px 'Space Grotesk';letter-spacing:-.06em">Divisions</h1><p class="section-lead">Distinct missions. Shared standards. One institution.</p><div class="grid">${TLG.divisions.map(card).join("")}</div></main>${footer()}`}
function about(){return `${header()}<main class="section shell page-transition"><div class="eyebrow">The Logan Group</div><h1 style="font:700 58px 'Space Grotesk';letter-spacing:-.06em">A long-term institution in progress.</h1><div class="markdown"><p>${esc(TLG.mission)}</p><h2>Purpose</h2><p>TLG is structured to design and operate educational platforms, conduct technical and interdisciplinary research, build software and systems, document knowledge for long-term use, and prepare for future academic, institutional, and societal impact.</p><h2>Principles</h2><ul>${TLG.principles.map(p=>`<li><strong>${esc(p[0])}</strong> — ${esc(p[1])}</li>`).join("")}</ul><h2>Organizational model</h2><p>The Logan Group functions as an umbrella structure with defined divisions. Each division has its own role while operating under shared governance, standards, and long-term direction.</p></div></main>${footer()}`}
function division(id){
 const d=TLG.divisions.find(x=>x.id===id); if(!d)return notfound();
 const extra=(window.TLG_CONTENT||[]).filter(x=>x.division===id);
 return `${header()}<main class="page-transition"><section class="division-hero shell"><img src="${esc(d.image)}" alt="${esc(d.name)}"><div class="eyebrow">${esc(d.type)} · ${esc(d.status)}</div><h1>${esc(d.name)}</h1><p class="section-lead">${esc(d.tagline)}</p></section><section class="section shell" style="padding-top:20px"><div class="division-layout"><div class="markdown"><p>${esc(d.description)}</p><h2>Areas of work</h2><ul class="area-list">${d.areas.map(x=>`<li>${esc(x)}</li>`).join("")}</ul>${extra.map(x=>`<article><h2>${esc(x.title)}</h2>${md(x.markdown)}</article>`).join("")}</div><aside class="side"><h3>Division profile</h3><p class="muted">Type</p><strong>${esc(d.type)}</strong><p class="muted">Status</p><strong>${esc(d.status)}</strong><p class="muted">Quick links</p><a class="btn" style="width:100%" href="#/divisions">All divisions</a></aside></div></section></main>${footer()}`;
}
function library(){
 const items=window.TLG_CONTENT||[];
 return `${header()}<main class="section shell page-transition"><div class="eyebrow">Knowledge center</div><h1 style="font:700 58px 'Space Grotesk';letter-spacing:-.06em">Library</h1><p class="section-lead">Published documents, devotionals, research notes, announcements, and other TLG material.</p>${items.length?`<div class="grid">${items.map(x=>`<a class="card reveal" href="#/document/${esc(x.slug)}"><div class="card-body"><span class="pill">${esc(x.category||"Document")}</span><h3>${esc(x.title)}</h3><div class="muted">${esc(x.description||"")}</div></div></a>`).join("")}</div>`:`<p class="muted" style="margin-top:35px">The library is ready for its first publication.</p>`}</main>${footer()}`;
}
function documentPage(slug){
 const x=(window.TLG_CONTENT||[]).find(x=>x.slug===slug); if(!x)return notfound();
 return `${header()}<main class="section shell page-transition"><div class="eyebrow">${esc(x.category||"Document")}</div><h1 style="font:700 clamp(42px,6vw,72px)/1 'Space Grotesk';letter-spacing:-.06em">${esc(x.title)}</h1><p class="muted">${esc(x.description||"")}</p><div class="markdown" style="margin-top:40px">${md(x.markdown)}</div></main>${footer()}`;
}
function notfound(){return `${header()}<main class="section shell page-transition"><h1>404</h1><p class="muted">That page does not exist.</p><a class="btn" href="#/">Return home</a></main>${footer()}`}
function reveal(){requestAnimationFrame(()=>document.querySelectorAll(".reveal").forEach((e,i)=>setTimeout(()=>e.classList.add("visible"),i*45)))}
function render(){
 const p=location.hash.slice(1)||"/"; let h;
 if(p==="/")h=home(); else if(p==="/about")h=about(); else if(p==="/divisions")h=divisions(); else if(p==="/library")h=library(); else if(p.startsWith("/document/"))h=documentPage(p.slice(10)); else h=division(p.slice(1));
 $("#app").innerHTML=h; reveal(); window.scrollTo({top:0,behavior:"smooth"});
}
window.addEventListener("hashchange",render); render();