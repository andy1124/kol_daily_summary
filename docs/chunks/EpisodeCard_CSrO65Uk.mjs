import { c as createAstro, a as createComponent, m as maybeRenderHead, e as addAttribute, b as renderTemplate } from './astro/server_DoyQVsRw.mjs';
import 'kleur/colors';
import 'clsx';
/* empty css                         */

const $$Astro = createAstro("https://andy1124.github.io");
const $$EpisodeCard = createComponent(($$result, $$props, $$slots) => {
  const Astro2 = $$result.createAstro($$Astro, $$props, $$slots);
  Astro2.self = $$EpisodeCard;
  const {
    id,
    podcastName,
    podcastSlug,
    title,
    publishedAt,
    durationSeconds,
    coverImage,
    hasMarkdown,
    hidePodcast = false
  } = Astro2.props;
  const base = "/kol_daily_summary".replace(/\/$/, "");
  const date = new Date(publishedAt).toLocaleDateString("zh-TW", {
    year: "numeric",
    month: "2-digit",
    day: "2-digit"
  });
  const mins = Math.round(durationSeconds / 60);
  return renderTemplate`${maybeRenderHead()}<a${addAttribute(`${base}/episodes/${id}/`, "href")} class="episode-card" data-astro-cid-7apkpmh7> ${!hidePodcast && coverImage && renderTemplate`<img class="thumb"${addAttribute(coverImage, "src")}${addAttribute(title, "alt")} loading="lazy" data-astro-cid-7apkpmh7>`} <div class="body" data-astro-cid-7apkpmh7> <div class="meta" data-astro-cid-7apkpmh7> ${!hidePodcast && renderTemplate`<span class="podcast" data-astro-cid-7apkpmh7>${podcastName}</span>`} <span class="date" data-astro-cid-7apkpmh7>${date}</span> ${mins > 0 && renderTemplate`<span class="dur" data-astro-cid-7apkpmh7>${mins} 分</span>`} ${hasMarkdown ? renderTemplate`<span class="badge badge--has" data-astro-cid-7apkpmh7>✦ 已摘要</span>` : renderTemplate`<span class="badge badge--none" data-astro-cid-7apkpmh7>待摘要</span>`} </div> <div class="title" data-astro-cid-7apkpmh7>${title}</div> </div> </a> `;
}, "/sessions/youthful-intelligent-ramanujan/mnt/kol_daily_summary/site/src/components/EpisodeCard.astro", void 0);

export { $$EpisodeCard as $ };
