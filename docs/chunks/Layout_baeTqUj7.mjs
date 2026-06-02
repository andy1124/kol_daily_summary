import { c as createAstro, a as createComponent, e as addAttribute, f as renderHead, b as renderTemplate, g as renderSlot } from './astro/server_DoyQVsRw.mjs';
import 'kleur/colors';
import 'clsx';
import { c as getPodcastList } from './data_BM1uCfFy.mjs';
/* empty css                        */

const $$Astro = createAstro("https://andy1124.github.io");
const $$Layout = createComponent(($$result, $$props, $$slots) => {
  const Astro2 = $$result.createAstro($$Astro, $$props, $$slots);
  Astro2.self = $$Layout;
  const { title, description = "每日財經 Podcast & KOL 重點彙整" } = Astro2.props;
  const base = "/kol_daily_summary".replace(/\/$/, "");
  const podcasts = getPodcastList();
  const pathname = Astro2.url.pathname;
  const isHome = pathname === base + "/" || pathname === base || pathname === "/";
  function isPodcastActive(slug) {
    return pathname.includes(`/podcasts/${slug}`);
  }
  return renderTemplate`<html lang="zh-TW" data-astro-cid-sckkx6r4> <head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><meta name="description"${addAttribute(description, "content")}><title>${title} · KOL Daily</title>${renderHead()}</head> <body data-astro-cid-sckkx6r4> <div class="app" data-astro-cid-sckkx6r4> <aside class="sidebar" id="sidebar" data-astro-cid-sckkx6r4> <div class="sidebar-logo" data-astro-cid-sckkx6r4> <a${addAttribute(`${base}/`, "href")} data-astro-cid-sckkx6r4> <div class="logo-main" data-astro-cid-sckkx6r4>KOL <span data-astro-cid-sckkx6r4>Daily</span></div> <div class="logo-sub" data-astro-cid-sckkx6r4>財經 Podcast 自動摘要</div> </a> </div> <nav class="sidebar-nav" data-astro-cid-sckkx6r4> <span class="nav-label" data-astro-cid-sckkx6r4>導航</span> <a${addAttribute(`${base}/`, "href")}${addAttribute(isHome ? "nav-item active" : "nav-item", "class")} data-astro-cid-sckkx6r4> <span class="nav-icon" data-astro-cid-sckkx6r4>⌂</span><span class="nav-name" data-astro-cid-sckkx6r4>首頁</span> </a> <span class="nav-label" style="margin-top:0.5rem" data-astro-cid-sckkx6r4>KOL 頻道</span> ${podcasts.map((p) => renderTemplate`<a${addAttribute(`${base}/podcasts/${p.slug}/`, "href")}${addAttribute(isPodcastActive(p.slug) ? "nav-item active" : "nav-item", "class")} data-astro-cid-sckkx6r4> <span class="nav-icon" data-astro-cid-sckkx6r4>▶</span> <span class="nav-name" data-astro-cid-sckkx6r4>${p.name}</span> <span class="ep-count" data-astro-cid-sckkx6r4>${p.episodeCount}</span> </a>`)} </nav> <div class="sidebar-footer" data-astro-cid-sckkx6r4>每日自動更新<br data-astro-cid-sckkx6r4>Whisper 轉錄 · Claude AI 摘要</div> </aside> <div class="overlay" id="overlay" data-astro-cid-sckkx6r4></div> <div class="mobile-header" data-astro-cid-sckkx6r4> <button class="hamburger" id="hamburger" aria-label="開啟選單" data-astro-cid-sckkx6r4> <span data-astro-cid-sckkx6r4></span><span data-astro-cid-sckkx6r4></span><span data-astro-cid-sckkx6r4></span> </button> <span class="mobile-logo" data-astro-cid-sckkx6r4>KOL <span data-astro-cid-sckkx6r4>Daily</span></span> </div> <div class="main-wrap" data-astro-cid-sckkx6r4> <main data-astro-cid-sckkx6r4>${renderSlot($$result, $$slots["default"])}</main> <footer data-astro-cid-sckkx6r4>每日自動更新 &nbsp;·&nbsp; 資料來源：各 Podcast RSS Feed &nbsp;·&nbsp; 轉錄：Whisper &nbsp;·&nbsp; 摘要：Claude AI</footer> </div> </div>  </body> </html>`;
}, "/sessions/vibrant-zealous-heisenberg/mnt/kol_daily_summary/site/src/layouts/Layout.astro", void 0);

export { $$Layout as $ };
