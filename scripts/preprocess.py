#!/usr/bin/env python3
"""
Layer 1: 確定性替換
在逐字稿送入 Claude 之前，套用 dictionary.json 的已知修正。

用法：
  python scripts/preprocess.py              # 處理所有有逐字稿的集數
  python scripts/preprocess.py --file PATH  # 處理特定 JSON 檔案
  python scripts/preprocess.py --dry-run    # 預覽修正，不實際寫入
"""
import json
import argparse
from pathlib import Path

ROOT = Path(__file__).parent.parent
DICTIONARY_FILE = ROOT / "dictionary.json"
PODCASTS_DIR = ROOT / "data" / "podcasts"


def load_dictionary() -> dict:
    if not DICTIONARY_FILE.exists():
        print(f"⚠️  找不到 {DICTIONARY_FILE}，請先建立 dictionary.json")
        return {}
    d = json.loads(DICTIONARY_FILE.read_text(encoding="utf-8"))
    # 過濾掉 key == value 的無效規則
    return {k: v for k, v in d.items() if k != v}


def apply_corrections(text: str, dictionary: dict) -> tuple[str, list[str]]:
    """套用字典替換，回傳 (修正後文字, 修正說明清單)"""
    corrections = []
    for wrong, correct in dictionary.items():
        if wrong in text:
            count = text.count(wrong)
            text = text.replace(wrong, correct)
            corrections.append(f"    「{wrong}」→「{correct}」（{count} 處）")
    return text, corrections


def process_file(json_path: Path, dictionary: dict, dry_run: bool = False) -> bool:
    try:
        data = json.loads(json_path.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"⚠️  讀取失敗 {json_path.name}：{e}")
        return False

    transcript = data.get("transcript", "")
    if not transcript:
        return False

    corrected, corrections = apply_corrections(transcript, dictionary)
    if not corrections:
        return False

    title = data.get("title", json_path.name)
    print(f"{'[dry-run] ' if dry_run else ''}✅ {title}")
    for c in corrections:
        print(c)

    if not dry_run:
        data["transcript"] = corrected
        json_path.write_text(
            json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
        )
    return True


def main():
    parser = argparse.ArgumentParser(description="套用 dictionary.json 修正逐字稿中的已知錯誤")
    parser.add_argument("--file", help="指定要處理的 JSON 檔案路徑")
    parser.add_argument("--dry-run", action="store_true", help="預覽修正，不實際寫入檔案")
    args = parser.parse_args()

    dictionary = load_dictionary()
    if not dictionary:
        return

    print(f"📖 載入 {len(dictionary)} 條替換規則\n")

    if args.file:
        files = [Path(args.file)]
    else:
        files = sorted(PODCASTS_DIR.glob("**/*.json"))

    modified = 0
    for f in files:
        if process_file(f, dictionary, dry_run=args.dry_run):
            modified += 1

    action = "（dry-run，未寫入）" if args.dry_run else ""
    print(f"\n完成：修正了 {modified} 個檔案{action}")


if __name__ == "__main__":
    import sys
    sys.path.insert(0, str(ROOT))
    main()
