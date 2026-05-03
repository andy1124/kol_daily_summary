"""Orchestrator: RSS check → Whisper transcribe → mark processed."""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
PROCESSED_FILE = ROOT / "data" / "processed.json"


def load_processed() -> set[str]:
    if PROCESSED_FILE.exists():
        return set(json.loads(PROCESSED_FILE.read_text(encoding="utf-8"))["episodes"])
    return set()


def save_processed(processed: set[str]) -> None:
    PROCESSED_FILE.write_text(
        json.dumps({"episodes": sorted(processed)}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def main():
    parser = argparse.ArgumentParser(description="每日 Podcast 更新流程")
    parser.add_argument("--dry-run", action="store_true", help="只顯示待處理項目，不實際執行")
    parser.add_argument("--max-episodes", type=int, default=5, help="每次最多處理集數（0=不限）")
    parser.add_argument("--skip-transcribe", action="store_true", help="跳過 Whisper 轉錄")
    args = parser.parse_args()

    print("=" * 50)
    print("Step 1: 檢查 RSS 新集數")
    print("=" * 50)
    from scripts.check_podcasts import check_all
    new_episodes = check_all(dry_run=args.dry_run, max_episodes=args.max_episodes)
    print(f"找到 {len(new_episodes)} 個新集數\n")

    if not new_episodes:
        print("沒有新集數，結束。")
        return

    if not args.skip_transcribe:
        print("=" * 50)
        print("Step 2: Whisper 音訊轉錄")
        print("=" * 50)
        from scripts.transcribe import transcribe_all
        n = transcribe_all(dry_run=args.dry_run)
        print(f"轉錄 {n} 個集數\n")

    if not args.dry_run:
        print("=" * 50)
        print("Step 3: 更新已處理記錄")
        print("=" * 50)
        processed = load_processed()
        for ep in new_episodes:
            processed.add(ep["id"])
        save_processed(processed)
        print(f"已記錄 {len(new_episodes)} 個新集數\n")

    print("完成！")


if __name__ == "__main__":
    sys.path.insert(0, str(ROOT))
    main()
