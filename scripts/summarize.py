"""Summarize podcast transcripts using Claude API with prompt caching."""
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

import anthropic
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent / ".env")

ROOT = Path(__file__).parent.parent
DATA_DIR = ROOT / "data"

SYSTEM_PROMPT = """你是一位專業的財經分析助理，專門整理台灣財經 Podcast 的重點內容。
請根據提供的 Podcast 逐字稿，萃取以下資訊，並以繁體中文回覆：
1. 核心觀點（3-7 個重點，每點一句話）
2. 提及的股票或市場（台股代號 + 名稱，或國際市場名稱）
3. 整體市場情緒（看多 / 看空 / 中性 / 混合）
4. 一句話重點摘要（30 字以內）

請以 JSON 格式回覆，格式如下：
{
  "key_points": ["重點1", "重點2", ...],
  "stocks_mentioned": ["台積電 (2330)", "NVDA", ...],
  "market_sentiment": "看多",
  "one_line_summary": "..."
}

只回覆 JSON，不要有其他說明文字。"""


def summarize_episode(episode_file: Path, client: anthropic.Anthropic) -> bool:
    ep = json.loads(episode_file.read_text(encoding="utf-8"))

    if ep.get("summary"):
        print(f"  [skip] 已有摘要: {ep['title']}")
        return False

    if not ep.get("transcript"):
        print(f"  [skip] 無逐字稿: {ep['title']}")
        return False

    print(f"[summarize] {ep['title']}")

    transcript = ep["transcript"]
    # Truncate very long transcripts to avoid token limits
    if len(transcript) > 80000:
        transcript = transcript[:80000] + "\n...(逐字稿已截斷)"

    try:
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=1024,
            system=[
                {
                    "type": "text",
                    "text": SYSTEM_PROMPT,
                    "cache_control": {"type": "ephemeral"},
                }
            ],
            messages=[
                {
                    "role": "user",
                    "content": f"以下是 Podcast「{ep['podcast_name']}」集數「{ep['title']}」的逐字稿：\n\n{transcript}",
                }
            ],
        )
        raw = response.content[0].text.strip()
        # Strip markdown code fences if present
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        summary_data = json.loads(raw)
    except json.JSONDecodeError as exc:
        print(f"  [error] JSON 解析失敗: {exc}", file=sys.stderr)
        return False
    except Exception as exc:
        print(f"  [error] Claude API 呼叫失敗: {exc}", file=sys.stderr)
        return False

    ep["summary"] = {
        **summary_data,
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }
    episode_file.write_text(json.dumps(ep, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  [done] 情緒: {summary_data.get('market_sentiment', '?')} | {summary_data.get('one_line_summary', '')}")
    return True


def summarize_all(dry_run: bool = False) -> int:
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("[error] 未設定 ANTHROPIC_API_KEY", file=sys.stderr)
        sys.exit(1)

    client = anthropic.Anthropic(api_key=api_key)
    count = 0

    for ep_file in sorted(DATA_DIR.rglob("*.json")):
        if ep_file.name == "processed.json":
            continue
        ep = json.loads(ep_file.read_text(encoding="utf-8"))
        if ep.get("summary"):
            continue
        if not ep.get("transcript"):
            continue
        if dry_run:
            print(f"  [pending] {ep.get('title', ep_file.name)}")
            count += 1
        else:
            if summarize_episode(ep_file, client):
                count += 1

    return count


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    n = summarize_all(dry_run=args.dry_run)
    print(f"\n摘要了 {n} 個集數")
