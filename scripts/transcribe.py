"""Download podcast audio and transcribe with local Whisper (medium model)."""
import json
import os
import sys
import tempfile
from pathlib import Path

import torch
import requests
import whisper

ROOT = Path(__file__).parent.parent
DATA_DIR = ROOT / "data"
TMP_DIR = ROOT / "tmp" / "audio"
TMP_DIR.mkdir(parents=True, exist_ok=True)

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
_model = None
MODEL_SIZE = "small"  # medium、small

def get_model():
    global _model
    if _model is None:
        print(f"[whisper] 載入 {MODEL_SIZE} 模型（device: {DEVICE}）...")
        _model = whisper.load_model(MODEL_SIZE, device=DEVICE)
        print("[whisper] 模型已載入")
    return _model


def download_audio(url: str, dest: Path) -> bool:
    try:
        print(f"  [download] {url[:80]}...")
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        with requests.get(url, stream=True, timeout=60, headers=headers, allow_redirects=True) as r:
            r.raise_for_status()
            content_type = r.headers.get("Content-Type", "")
            print(f"  [download] Content-Type: {content_type}")
            with open(dest, "wb") as f:
                for chunk in r.iter_content(chunk_size=1024 * 1024):
                    f.write(chunk)
        file_size = dest.stat().st_size
        print(f"  [download] 檔案大小: {file_size / 1024:.1f} KB")
        if file_size < 10 * 1024:  # 小於 10KB 幾乎不可能是有效音訊
            print(f"  [error] 檔案過小，可能不是有效音訊（{file_size} bytes）", file=sys.stderr)
            dest.unlink(missing_ok=True)
            return False
        if "text/html" in content_type:
            print(f"  [error] 伺服器回傳 HTML 而非音訊，可能需要驗證或 URL 已失效", file=sys.stderr)
            dest.unlink(missing_ok=True)
            return False
        return True
    except Exception as exc:
        print(f"  [error] 下載失敗: {exc}", file=sys.stderr)
        return False


def transcribe_episode(episode_file: Path) -> bool:
    ep = json.loads(episode_file.read_text(encoding="utf-8"))

    if ep.get("transcript"):
        print(f"  [skip] 已有逐字稿: {ep['title']}")
        return False

    if not ep.get("audio_url"):
        print(f"  [skip] 無音訊連結: {ep['title']}", file=sys.stderr)
        return False

    print(f"[transcribe] {ep['title']}")

    audio_path = TMP_DIR / f"{ep['id']}.mp3"
    if not download_audio(ep["audio_url"], audio_path):
        return False

    try:
        model = get_model()
        print("  [whisper] 開始轉錄...")
        result = model.transcribe(str(audio_path), language="zh", verbose=False)
        transcript = result["text"].strip()
        print(f"  [whisper] 完成，字數: {len(transcript)}")
    except Exception as exc:
        print(f"  [error] 轉錄失敗: {exc}", file=sys.stderr)
        return False
    finally:
        if audio_path.exists():
            audio_path.unlink()

    ep["transcript"] = transcript
    episode_file.write_text(json.dumps(ep, ensure_ascii=False, indent=2), encoding="utf-8")
    return True


def transcribe_all(dry_run: bool = False) -> int:
    count = 0
    for ep_file in sorted(DATA_DIR.rglob("*.json")):
        if ep_file.name == "processed.json":
            continue
        if dry_run:
            ep = json.loads(ep_file.read_text(encoding="utf-8"))
            if not ep.get("transcript") and ep.get("audio_url"):
                print(f"  [pending] {ep.get('title', ep_file.name)}")
                count += 1
        else:
            if transcribe_episode(ep_file):
                count += 1
    return count


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    n = transcribe_all(dry_run=args.dry_run)
    print(f"\n轉錄了 {n} 個集數")
