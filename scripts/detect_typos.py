#!/usr/bin/env python3
"""
Layer 3: 互動式審閱疑似辨識錯誤
掃描所有集數摘要中的「# 疑似辨識錯誤」區塊，逐條讓你確認，
確認後自動寫入 dictionary.json。

用法：
  python scripts/detect_typos.py           # 審閱所有未處理的建議
  python scripts/detect_typos.py --all     # 包含已在字典中的詞（重新審閱）
"""
import json
import re
import argparse
from pathlib import Path

ROOT = Path(__file__).parent.parent
DICTIONARY_FILE = ROOT / "dictionary.json"
PODCASTS_DIR = ROOT / "data" / "podcasts"

# 解析「# 疑似辨識錯誤」區塊
SECTION_RE = re.compile(
    r"#\s*疑似辨識錯誤\s*\n(.*?)(?=\n#\s|\Z)",
    re.DOTALL,
)
# 解析每一條建議：「原文」→ 建議：「修正」（說明）
ENTRY_RE = re.compile(
    r"[-•]\s*「(.+?)」\s*[→->]+\s*建議[：:]\s*「(.+?)」(?:[（(](.+?)[)）])?"
)


def load_dictionary() -> dict:
    if DICTIONARY_FILE.exists():
        return json.loads(DICTIONARY_FILE.read_text(encoding="utf-8"))
    return {}


def save_dictionary(d: dict) -> None:
    DICTIONARY_FILE.write_text(
        json.dumps(d, ensure_ascii=False, indent=4), encoding="utf-8"
    )


def extract_candidates(summary: str) -> list[tuple[str, str, str]]:
    """從摘要 markdown 提取疑似錯誤，回傳 [(原文, 建議, 說明), ...]"""
    match = SECTION_RE.search(summary)
    if not match:
        return []
    section = match.group(1).strip()
    if section in ("無", "none", ""):
        return []
    results = []
    for m in ENTRY_RE.finditer(section):
        wrong = m.group(1).strip()
        correct = m.group(2).strip()
        note = m.group(3).strip() if m.group(3) else ""
        results.append((wrong, correct, note))
    return results


def collect_all_candidates(include_known: bool = False) -> list[dict]:
    """掃描所有 JSON 檔，彙整候選詞。"""
    dictionary = load_dictionary()
    seen_keys: set[str] = set()
    candidates = []

    for json_path in sorted(PODCASTS_DIR.glob("**/*.json")):
        try:
            data = json.loads(json_path.read_text(encoding="utf-8"))
        except Exception:
            continue

        summary = data.get("summary") or ""
        if not summary:
            continue

        for wrong, correct, note in extract_candidates(summary):
            if wrong in seen_keys:
                continue
            seen_keys.add(wrong)

            already_in_dict = wrong in dictionary
            if already_in_dict and not include_known:
                continue

            candidates.append({
                "wrong": wrong,
                "correct": correct,
                "note": note,
                "source": data.get("title", json_path.name),
                "already_in_dict": already_in_dict,
                "current_correction": dictionary.get(wrong),
            })

    return candidates


def interactive_review(candidates: list[dict]) -> int:
    """互動式審閱，回傳新增筆數。"""
    dictionary = load_dictionary()
    added = 0

    print(f"\n找到 {len(candidates)} 筆待審閱的疑似辨識錯誤\n")
    print("操作說明：y = 確認加入，n = 跳過，直接輸入文字 = 自訂修正詞\n")
    print("=" * 60)

    for i, c in enumerate(candidates, 1):
        wrong = c["wrong"]
        correct = c["correct"]
        note = c["note"]
        source = c["source"]

        note_str = f"（{note}）" if note else ""
        existing_str = ""
        if c["already_in_dict"]:
            existing_str = f"  ⚠️  字典中已有：「{wrong}」→「{c['current_correction']}」"

        print(f"[{i}/{len(candidates)}] 來源：{source}")
        if existing_str:
            print(existing_str)
        print(f"  「{wrong}」→「{correct}」{note_str}")

        try:
            ans = input("  加入 dictionary？(y/n/自訂修正詞) ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n\n中止審閱。")
            break

        if ans.lower() == "y":
            dictionary[wrong] = correct
            added += 1
            print(f"  ✅ 已加入\n")
        elif ans.lower() == "n" or ans == "":
            print(f"  ⏭️  跳過\n")
        else:
            # 使用者輸入自訂修正詞
            dictionary[wrong] = ans
            added += 1
            print(f"  ✅ 已加入（自訂：「{ans}」）\n")

    return added, dictionary


def main():
    parser = argparse.ArgumentParser(
        description="審閱 Claude 偵測到的疑似 Whisper 辨識錯誤，確認後寫入 dictionary.json"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="包含已在字典中的詞（用於重新審閱或修改現有修正）",
    )
    args = parser.parse_args()

    candidates = collect_all_candidates(include_known=args.all)

    if not candidates:
        print("✅ 沒有新的疑似辨識錯誤需要審閱。")
        print("   （若要重新審閱已在字典中的詞，加上 --all 參數）")
        return

    added, updated_dict = interactive_review(candidates)

    if added > 0:
        save_dictionary(updated_dict)
        print(f"✅ 已將 {added} 筆修正寫入 dictionary.json")
        print(f"   目前字典共 {len(updated_dict)} 條規則")
    else:
        print("未新增任何項目，dictionary.json 未變動。")


if __name__ == "__main__":
    import sys
    sys.path.insert(0, str(ROOT))
    main()
