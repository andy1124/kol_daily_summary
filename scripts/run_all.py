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
    parser = argparse.ArgumentParser(
        description="每日 Podcast 更新流程",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用方式（兩種模式二擇一）：
  --since YYYY-MM-DD   下載每個 Podcast 從該日期到今天的所有新集數
  --max-episodes N     下載每個 Podcast 最新的 N 集（預設 5）

範例：
  python run_all.py --since 2026-05-01
  python run_all.py --max-episodes 3
  python run_all.py --since 2026-05-01 --dry-run
        """,
    )
    parser.add_argument("--dry-run", action="store_true", help="只顯示待處理項目，不實際執行")
    parser.add_argument("--skip-transcribe", action="store_true", help="跳過 Whisper 轉錄")

    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--since",
        dest="since_date",
        default="",
        metavar="YYYY-MM-DD",
        help="下載每個 Podcast 從指定日期（含）至今的所有未處理集數",
    )
    mode.add_argument(
        "--max-episodes",
        type=int,
        default=5,
        metavar="N",
        help="每個 Podcast 各自取最新 N 集（預設 5，0=不限）",
    )
    args = parser.parse_args()

    print("=" * 50)
    print("Step 1: 檢查 RSS 新集數")
    print("=" * 50)
    from scripts.check_podcasts import check_all
    new_episodes = check_all(
        dry_run=args.dry_run,
        max_episodes=args.max_episodes,
        since_date=args.since_date,
    )
    print(f"找到 {len(new_episodes)} 個新集數\n")

    if not new_episodes:
        print("沒有新集數，結束。")
        return

    if not args.skip_transcribe:
        print("=" * 50)
        print("Step 2: Whisper 音訊轉錄")
        print("=" * 50)
        if args.dry_run:
            print("  [dry-run] 跳過 Whisper 載入")
        else:
            from scripts.transcribe import transcribe_all
            n = transcribe_all()
            print(f"轉錄 {n} 個集數\n")

    if not args.dry_run:
        print("=" * 50)
        print("Step 3: 更新已處理記錄")
        print("=" * 50)
        processed = load_processed()
        recorded = 0
        skipped = 0
        for ep in new_episodes:
            # 只記錄已成功取得逐字稿的集數，避免轉錄失敗的集數被永久跳過
            ep_file = ROOT / "data" / "podcasts" / ep["podcast_slug"] / f"{ep['id']}.json"
            if ep_file.exists():
                ep_data = json.loads(ep_file.read_text(encoding="utf-8"))
                if ep_data.get("transcript"):
                    processed.add(ep["id"])
                    recorded += 1
                else:
                    print(f"  [skip] 無逐字稿，不記錄為已處理: {ep['title']}")
                    skipped += 1
            else:
                # 若 JSON 檔不存在（dry-run 等情況），仍照舊記錄
                processed.add(ep["id"])
                recorded += 1
        save_processed(processed)
        print(f"已記錄 {recorded} 個集數（{skipped} 個因無逐字稿暫不記錄）\n")

    print("完成！")


if __name__ == "__main__":
    sys.path.insert(0, str(ROOT))
    main()
