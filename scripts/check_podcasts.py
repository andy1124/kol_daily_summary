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


def check_all(
    dry_run: bool = False,
    max_episodes: int = 0,
    since_date: str = "",
) -> list[dict]:
    """
    收集各 Podcast 的新集數（未處理過的）。

    模式一（since_date）：每個 Podcast 取 since_date 當天（含）到現在的所有集數。
    模式二（max_episodes）：每個 Podcast 各自取最新的 max_episodes 集。
    兩種模式皆跳過已在 processed.json 中的集數。
    """
    sources = yaml.safe_load(CONFIG_FILE.read_text(encoding="utf-8"))
    processed = load_processed()
    new_episodes = []

    # 解析起始日期（UTC 00:00:00）
    since_dt = None
    if since_date:
        since_dt = datetime.fromisoformat(since_date).replace(
            hour=0, minute=0, second=0, microsecond=0, tzinfo=timezone.utc
        )
        print(f"[模式] 日期區間：{since_date} 至今")
    elif max_episodes:
        print(f"[模式] 每個 Podcast 最新 {max_episodes} 集")

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

        podcast_new = []
        for entry in feed.entries:
            ep = parse_episode(entry, podcast)

            # 跳過已處理過的集數
            if ep["id"] in processed:
                continue

            # 跳過沒有音訊連結的集數
            if not ep["audio_url"]:
                print(f"  [skip] {ep['title']}: 無音訊連結")
                continue

            # 日期模式：過濾發布時間早於 since_dt 的集數
            if since_dt:
                ep_dt = datetime.fromisoformat(ep["published_at"])
                if ep_dt < since_dt:
                    continue

            print(f"  [new] {ep['title']} ({ep['published_at'][:10]})")
            podcast_new.append(ep)

        # 每個 Podcast 內部依發布時間排序（新到舊）
        podcast_new.sort(key=lambda e: e["published_at"], reverse=True)

        # max_episodes 模式：每個 Podcast 各自截取最新 N 集
        if max_episodes and not since_dt:
            podcast_new = podcast_new[:max_episodes]

        new_episodes.extend(podcast_new)

    # 全部結果再依時間排序（新到舊）
    new_episodes.sort(key=lambda e: e["published_at"], reverse=True)

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
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--max-episodes", type=int, default=0, help="每個 Podcast 最新 N 集")
    group.add_argument("--since", dest="since_date", default="", metavar="YYYY-MM-DD", help="下載該日期至今的所有集數")
    args = parser.parse_args()
    episodes = check_all(dry_run=args.dry_run, max_episodes=args.max_episodes, since_date=args.since_date)
    print(f"\n找到 {len(episodes)} 個新集數")
