"""Check RSS feeds for new podcast episodes."""
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

import feedparser
import yaml

ROOT = Path(__file__).parent.parent
DATA_DIR = ROOT / "data"
CONFIG_FILE = ROOT / "config" / "sources.yaml"
PROCESSED_FILE = DATA_DIR / "processed.json"


def load_processed() -> set[str]:
    if PROCESSED_FILE.exists():
        return set(json.loads(PROCESSED_FILE.read_text(encoding="utf-8"))["episodes"])
    return set()


def save_processed(processed: set[str]) -> None:
    PROCESSED_FILE.write_text(
        json.dumps({"episodes": sorted(processed)}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def parse_episode(entry, podcast: dict) -> dict:
    published = entry.get("published_parsed")
    if published:
        published_at = datetime(*published[:6], tzinfo=timezone.utc).isoformat()
    else:
        published_at = datetime.now(timezone.utc).isoformat()

    audio_url = ""
    for link in entry.get("links", []):
        if link.get("type", "").startswith("audio"):
            audio_url = link.get("href", "")
            break
    if not audio_url:
        for enc in entry.get("enclosures", []):
            if enc.get("type", "").startswith("audio"):
                audio_url = enc.get("href", enc.get("url", ""))
                break

    cover = ""
    if "image" in entry:
        cover = entry["image"].get("href", "")
    if not cover:
        cover = podcast.get("cover_image", "")

    duration_seconds = 0
    itunes = entry.get("itunes_duration", "")
    if itunes:
        parts = str(itunes).split(":")
        try:
            if len(parts) == 3:
                duration_seconds = int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
            elif len(parts) == 2:
                duration_seconds = int(parts[0]) * 60 + int(parts[1])
            else:
                duration_seconds = int(parts[0])
        except ValueError:
            pass

    slug = podcast["slug"]
    episode_id = f"{slug}-{entry.get('id', entry.get('link', ''))}"
    episode_id = "".join(c if c.isalnum() or c in "-_" else "-" for c in episode_id)
    episode_id = episode_id[:80].strip("-")

    return {
        "id": episode_id,
        "podcast_slug": slug,
        "podcast_name": podcast["name"],
        "title": entry.get("title", "無標題"),
        "published_at": published_at,
        "duration_seconds": duration_seconds,
        "audio_url": audio_url,
        "cover_image": cover,
        "show_notes": entry.get("summary", ""),
        "transcript": "",
        "summary": None,
    }


def check_all(dry_run: bool = False, max_episodes: int = 0) -> list[dict]:
    sources = yaml.safe_load(CONFIG_FILE.read_text(encoding="utf-8"))
    processed = load_processed()
    new_episodes = []

    for podcast in sources.get("podcasts", []):
        rss_url = podcast.get("rss_url", "")
        if not rss_url:
            print(f"[skip] {podcast['name']}: rss_url 未設定", file=sys.stderr)
            continue

        print(f"[rss] 檢查 {podcast['name']} ...")
        try:
            feed = feedparser.parse(rss_url)
        except Exception as exc:
            print(f"[error] {podcast['name']}: {exc}", file=sys.stderr)
            continue

        for entry in feed.entries:
            ep = parse_episode(entry, podcast)
            if ep["id"] in processed:
                continue
            if not ep["audio_url"]:
                print(f"  [skip] {ep['title']}: 無音訊連結")
                continue
            print(f"  [new] {ep['title']} ({ep['published_at'][:10]})")
            new_episodes.append(ep)
            if max_episodes and len(new_episodes) >= max_episodes:
                break

        if max_episodes and len(new_episodes) >= max_episodes:
            break

    if not dry_run:
        for ep in new_episodes:
            pod_dir = DATA_DIR / "podcasts" / ep["podcast_slug"]
            pod_dir.mkdir(parents=True, exist_ok=True)
            out_file = pod_dir / f"{ep['id']}.json"
            out_file.write_text(json.dumps(ep, ensure_ascii=False, indent=2), encoding="utf-8")

    return new_episodes


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--max-episodes", type=int, default=0)
    args = parser.parse_args()
    episodes = check_all(dry_run=args.dry_run, max_episodes=args.max_episodes)
    print(f"\n找到 {len(episodes)} 個新集數")
