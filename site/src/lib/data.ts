import { readFileSync, readdirSync, existsSync } from "node:fs";
import { join, resolve } from "node:path";

export interface EpisodeSummary {
  key_points: string[];
  stocks_mentioned: string[];
  market_sentiment: string;
  one_line_summary: string;
  generated_at: string;
}

export interface Episode {
  id: string;
  podcast_slug: string;
  podcast_name: string;
  title: string;
  published_at: string;
  duration_seconds: number;
  audio_url: string;
  cover_image: string;
  show_notes: string;
  transcript: string;
  summary: EpisodeSummary | null;
  markdownContent?: string;
  hasMarkdown?: boolean;
}

export interface PodcastMeta {
  slug: string;
  name: string;
  episodeCount: number;
  latestEpisode?: Episode;
  coverImage?: string;
}

const DATA_DIR = resolve(join(import.meta.dirname ?? "", "../../../data"));

function readJson<T>(path: string): T | null {
  try {
    return JSON.parse(readFileSync(path, "utf-8")) as T;
  } catch {
    return null;
  }
}

function readMarkdown(path: string): string | null {
  try {
    return readFileSync(path, "utf-8");
  } catch {
    return null;
  }
}

export function getAllEpisodes(): Episode[] {
  const podcastsDir = join(DATA_DIR, "podcasts");
  if (!existsSync(podcastsDir)) return [];

  const episodes: Episode[] = [];
  for (const slug of readdirSync(podcastsDir)) {
    const slugDir = join(podcastsDir, slug);
    for (const file of readdirSync(slugDir)) {
      if (!file.endsWith(".json")) continue;
      const ep = readJson<Episode>(join(slugDir, file));
      if (!ep) continue;
      // Check for companion markdown file
      const mdPath = join(slugDir, file.replace(/\.json$/, ".md"));
      const md = readMarkdown(mdPath);
      ep.markdownContent = md ?? undefined;
      ep.hasMarkdown = md !== null;
      episodes.push(ep);
    }
  }
  return episodes.sort(
    (a, b) => new Date(b.published_at).getTime() - new Date(a.published_at).getTime()
  );
}

export function getEpisodeById(id: string): Episode | null {
  const all = getAllEpisodes();
  return all.find((e) => e.id === id) ?? null;
}

export function getPodcastList(): PodcastMeta[] {
  const episodes = getAllEpisodes();
  const map = new Map<string, PodcastMeta>();

  for (const ep of episodes) {
    if (!map.has(ep.podcast_slug)) {
      map.set(ep.podcast_slug, {
        slug: ep.podcast_slug,
        name: ep.podcast_name,
        episodeCount: 0,
        coverImage: ep.cover_image || undefined,
      });
    }
    const meta = map.get(ep.podcast_slug)!;
    meta.episodeCount += 1;
    if (!meta.latestEpisode) meta.latestEpisode = ep;
    if (ep.cover_image && !meta.coverImage) meta.coverImage = ep.cover_image;
  }

  return Array.from(map.values());
}

export function getEpisodesByPodcast(slug: string): Episode[] {
  return getAllEpisodes().filter((e) => e.podcast_slug === slug);
}

export function getRecentEpisodes(withinHours = 48): Episode[] {
  const cutoff = Date.now() - withinHours * 60 * 60 * 1000;
  return getAllEpisodes().filter(
    (e) => new Date(e.published_at).getTime() > cutoff
  );
}

export function getLatestPerPodcast(): Episode[] {
  const seen = new Set<string>();
  return getAllEpisodes().filter((ep) => {
    if (seen.has(ep.podcast_slug)) return false;
    seen.add(ep.podcast_slug);
    return true;
  });
}

export interface DateGroup {
  date: string;
  label: string;
  episodes: Episode[];
}

export function getEpisodesGroupedByDate(): DateGroup[] {
  const episodes = getAllEpisodes();
  const groups = new Map<string, Episode[]>();
  for (const ep of episodes) {
    const date = ep.published_at.slice(0, 10);
    if (!groups.has(date)) groups.set(date, []);
    groups.get(date)!.push(ep);
  }
  return Array.from(groups.entries())
    .sort(([a], [b]) => b.localeCompare(a))
    .map(([date, eps]) => {
      const d = new Date(date + "T12:00:00Z");
      const label = `${d.getUTCMonth() + 1}/${d.getUTCDate()}`;
      return { date, label, episodes: eps };
    });
}

  for (const ep of episodes) {
    const dateKey = ep.published_at.slice(0, 10);
    if (!groups.has(dateKey)) groups.set(dateKey, []);
    groups.get(dateKey)!.push(ep);
  }

  return Array.from(groups.entries())
    .sort(([a], [b]) => b.localeCompare(a))
    .map(([date, eps]) => ({
      date,
      label: new Date(date).toLocaleDateString("zh-TW", { year: "numeric", month: "long", day: "numeric" }),
      episodes: eps,
    }));
}
    });
}
