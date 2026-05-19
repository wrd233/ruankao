#!/usr/bin/env python3
"""02_docmind_mcp_full_run.py — Batch MCP convert_to_markdown with resume/retry.

Usage:
  python3 02_docmind_mcp_full_run.py --doc all
  python3 02_docmind_mcp_full_run.py --doc tutorial
  python3 02_docmind_mcp_full_run.py --doc questions
  python3 02_docmind_mcp_full_run.py --doc all --resume
  python3 02_docmind_mcp_full_run.py --doc all --retry-failed
"""

from __future__ import annotations

import argparse
import json
import os
import select
import subprocess
import sys
import time
import urllib.parse
from datetime import datetime, timezone, timedelta
from pathlib import Path

tz = timezone(timedelta(hours=8))
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
FULL_DIR = PROJECT_ROOT / "docmind_ocr_full"
MANIFEST_PATH = FULL_DIR / "input_manifest.json"
CHUNKS_DIR = FULL_DIR / "chunks"
RAW_DIR = FULL_DIR / "raw_outputs"
MD_DIR = FULL_DIR / "markdown_chunks"
REPORTS_DIR = FULL_DIR / "reports"

TIMEOUT_SECONDS = 1800   # 30 minutes per chunk
MAX_RETRIES = 3
INIT_TIMEOUT = 60


def log(msg: str) -> None:
    print(f"[{datetime.now(tz).strftime('%H:%M:%S')}] {msg}")


def load_env():
    env_path = PROJECT_ROOT / ".env"
    if env_path.is_file():
        for line in env_path.read_text().split("\n"):
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, _, val = line.partition("=")
                if key and val and key not in os.environ:
                    os.environ[key] = val
    ak = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID")
    sk = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET")
    if not ak or not sk:
        log("FATAL: AK/SK not set. Run: source .env")
        sys.exit(1)
    log("AK_ID: PRESENT | AK_SECRET: PRESENT")
    return {"ALIBABA_CLOUD_ACCESS_KEY_ID": ak, "ALIBABA_CLOUD_ACCESS_KEY_SECRET": sk}


def build_file_uri(path: Path) -> str:
    abs_path = str(path.resolve())
    return "file://" + urllib.parse.quote(abs_path, safe="/")


def send_jsonrpc(proc, payload: dict) -> None:
    line = json.dumps(payload, ensure_ascii=False)
    proc.stdin.write(line + "\n")
    proc.stdin.flush()


def read_line_timeout(proc, timeout: float = 5.0) -> str | None:
    ready, _, _ = select.select([proc.stdout], [], [], timeout)
    if ready:
        line = proc.stdout.readline()
        return line.rstrip("\n") if line else None
    return None


def read_json_response(proc, timeout: float = 60.0) -> dict | None:
    line = read_line_timeout(proc, timeout)
    if line is None:
        return None
    try:
        return json.loads(line)
    except json.JSONDecodeError:
        return None


def mcp_handshake(proc) -> bool:
    init_req = {
        "jsonrpc": "2.0", "id": 1, "method": "initialize",
        "params": {"protocolVersion": "2024-11-05", "capabilities": {},
                    "clientInfo": {"name": "docmind-full", "version": "2.0"}},
    }
    send_jsonrpc(proc, init_req)
    resp = read_json_response(proc, timeout=INIT_TIMEOUT)
    if resp is None or "error" in resp:
        log(f"  Handshake failed: {resp}")
        return False
    send_jsonrpc(proc, {"jsonrpc": "2.0", "method": "notifications/initialized", "params": None})
    time.sleep(0.3)
    return True


def call_convert(proc, uri: str) -> dict | None:
    req = {"jsonrpc": "2.0", "id": 2, "method": "tools/call",
           "params": {"name": "convert_to_markdown", "arguments": {"uri": uri}}}
    send_jsonrpc(proc, req)
    start = time.time()
    last = None
    while time.time() - start < TIMEOUT_SECONDS:
        resp = read_json_response(proc, timeout=15.0)
        if resp is None:
            continue
        last = resp
        if "id" in resp:
            return resp
    return last


def extract_md_text(response: dict) -> str | None:
    try:
        content = response.get("result", {}).get("content", [])
        texts = []
        for item in content:
            if isinstance(item, dict) and item.get("type") == "text":
                texts.append(item.get("text", ""))
            elif isinstance(item, str):
                texts.append(item)
        return "\n".join(texts).strip()
    except Exception:
        return None


def is_error_response(text: str) -> bool:
    """Check if the markdown text is actually an error message."""
    return text.startswith("Error executing tool") or "DocMind" in text[:200]


def shutdown(proc) -> None:
    try:
        send_jsonrpc(proc, {"jsonrpc": "2.0", "id": 99, "method": "shutdown", "params": None})
        time.sleep(0.2)
        proc.terminate()
        proc.wait(timeout=5)
    except Exception:
        try:
            proc.kill()
        except Exception:
            pass


def process_chunk(chunk: dict, slug: str, env: dict, force: bool = False, retry_failed: bool = False) -> bool:
    chunk_id = chunk["chunk_id"]
    pdf_path = CHUNKS_DIR / slug / f"{chunk_id}.pdf"
    raw_path = RAW_DIR / slug / f"{chunk_id}.raw.json"
    md_path = MD_DIR / slug / f"{chunk_id}.md"

    if not force and md_path.exists():
        text = md_path.read_text(encoding="utf-8")
        if text.strip() and not is_error_response(text[:300]):
            log(f"  {chunk_id}: already done, skipping")
            chunk["status"] = "success"
            return True

    if retry_failed:
        log(f"  {chunk_id}: retrying after failure...")
    else:
        log(f"  {chunk_id}: pages {chunk['start_page']}-{chunk['end_page']}...")

    uri = build_file_uri(pdf_path)
    env_full = os.environ.copy()
    env_full.update(env)

    for attempt in range(MAX_RETRIES):
        if attempt > 0:
            log(f"  {chunk_id}: retry {attempt + 1}/{MAX_RETRIES}...")
            time.sleep(3)

        try:
            proc = subprocess.Popen(
                ["uvx", "docmind-parser-mcp"],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                text=True, bufsize=1, env=env_full,
            )
        except Exception as e:
            log(f"  {chunk_id}: spawn failed: {e}")
            chunk["status"] = "failed"
            chunk["error"] = str(e)[:300]
            return False

        ok = False
        try:
            if not mcp_handshake(proc):
                log(f"  {chunk_id}: handshake failed")
                continue

            start_t = time.time()
            resp = call_convert(proc, uri)
            elapsed = time.time() - start_t
            log(f"  {chunk_id}: API call took {elapsed:.0f}s")

            if resp is None:
                log(f"  {chunk_id}: timeout after {TIMEOUT_SECONDS}s")
                chunk["error"] = "timeout"
                continue

            # Save raw
            raw_path.parent.mkdir(parents=True, exist_ok=True)
            raw_path.write_text(json.dumps(resp, ensure_ascii=False, indent=2), encoding="utf-8")

            if "error" in resp:
                err_str = json.dumps(resp["error"], ensure_ascii=False)[:500]
                log(f"  {chunk_id}: API error: {err_str}")
                chunk["error"] = err_str
                continue

            md_text = extract_md_text(resp)
            if md_text is None:
                log(f"  {chunk_id}: no markdown text in response")
                chunk["error"] = "no_markdown_text"
                continue

            if is_error_response(md_text[:300]):
                log(f"  {chunk_id}: response is error message: {md_text[:200]}")
                chunk["error"] = md_text[:300]
                md_path.parent.mkdir(parents=True, exist_ok=True)
                md_path.write_text(md_text, encoding="utf-8")
                continue

            md_path.parent.mkdir(parents=True, exist_ok=True)
            md_path.write_text(md_text, encoding="utf-8")
            log(f"  {chunk_id}: OK — {len(md_text):,} chars saved")
            chunk["status"] = "success"
            chunk["retries"] = attempt
            ok = True
            break

        finally:
            shutdown(proc)

    if not ok:
        chunk["status"] = "failed"
        chunk["retries"] = attempt + 1
        return False
    return True


def save_manifest(manifest: dict):
    MANIFEST_PATH.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")


def generate_run_log(manifest: dict):
    lines = [
        "# Full-Run Log",
        f"\nGenerated: {datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S')}\n",
    ]
    for doc in manifest["documents"]:
        slug = doc["slug"]
        lines.append(f"## {doc['title']}")
        lines.append(f"\n| Chunk | Pages | Status | Retries | Chars | Error |")
        lines.append("|-------|-------|--------|---------|-------|-------|")
        success_n = 0
        fail_n = 0
        for chunk in doc["chunks"]:
            md_path = MD_DIR / slug / f"{chunk['chunk_id']}.md"
            chars = len(md_path.read_text(encoding="utf-8")) if md_path.exists() else 0
            err = chunk.get("error", "")[:80] if chunk.get("status") == "failed" else ""
            lines.append(f"| {chunk['chunk_id']} | {chunk['start_page']}-{chunk['end_page']} | {chunk['status']} | {chunk.get('retries', 0)} | {chars:,} | {err} |")
            if chunk["status"] == "success":
                success_n += 1
            else:
                fail_n += 1
        total = success_n + fail_n
        lines.append(f"\n- **{success_n}/{total} chunks successful**, {fail_n} failed")
    (REPORTS_DIR / "02_run_log.md").write_text("\n".join(lines), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--doc", default="all", choices=["tutorial", "questions", "all"])
    parser.add_argument("--resume", action="store_true", help="Skip already-successful chunks")
    parser.add_argument("--retry-failed", action="store_true", help="Re-process failed chunks")
    parser.add_argument("--force", action="store_true", help="Force re-process all chunks")
    args = parser.parse_args()

    log("===== Full MCP Run Start =====")

    env = load_env()
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))

    targets = manifest["documents"]
    if args.doc != "all":
        targets = [d for d in targets if d["slug"] == args.doc]

    for doc in targets:
        slug = doc["slug"]
        log(f"\n=== Processing: {slug} ({doc['pages']} pages, {len(doc['chunks'])} chunks) ===")
        for chunk in doc["chunks"]:
            if args.resume and chunk.get("status") == "success":
                log(f"  {chunk['chunk_id']}: resume skip (already success)")
                continue
            if args.retry_failed and chunk.get("status") != "failed":
                continue
            if not args.retry_failed and not args.resume and not args.force:
                # Default: skip already-successful
                md_path = MD_DIR / slug / f"{chunk['chunk_id']}.md"
                if md_path.exists():
                    text = md_path.read_text(encoding="utf-8")
                    if text.strip() and not is_error_response(text[:300]):
                        chunk["status"] = "success"
                        log(f"  {chunk['chunk_id']}: already done")
                        continue

            process_chunk(chunk, slug, env, force=args.force, retry_failed=args.retry_failed)
            save_manifest(manifest)

    generate_run_log(manifest)
    log("\n===== Full MCP Run Done =====")


if __name__ == "__main__":
    main()
