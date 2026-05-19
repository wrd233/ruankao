#!/usr/bin/env python3
"""02_mcp_convert_to_markdown.py — 通过 MCP 调用 docmind-parser-mcp 转 Markdown

使用 subprocess + JSON-RPC 2.0 与 uvx docmind-parser-mcp 通信，
调用 convert_to_markdown 工具，保存原始返回和 Markdown 正文。

所有 AK/SK 凭据仅通过环境变量传递，绝不打印。
"""

from __future__ import annotations

import json
import os
import signal
import subprocess
import sys
import time
import urllib.parse
from pathlib import Path
from datetime import datetime, timezone, timedelta

tz = timezone(timedelta(hours=8))
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
TRIAL_DIR = PROJECT_ROOT / "docmind_ocr_trial"
INPUT_DIR = TRIAL_DIR / "input_samples"
RAW_DIR = TRIAL_DIR / "raw_outputs"
MD_DIR = TRIAL_DIR / "markdown_outputs"
LOGS_DIR = TRIAL_DIR / "logs"

TIMEOUT_SECONDS = 180  # 每个文档最多等待 3 分钟

SAMPLES = [
    {"slug": "tutorial", "label": "教程样本"},
    {"slug": "questions", "label": "题库样本"},
]


def log(msg: str) -> None:
    timestamp = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {msg}"
    print(line)


def check_env() -> dict[str, str]:
    """检查并返回环境变量，绝不打印具体值。"""
    ak = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID")
    sk = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET")
    if not ak:
        log("✗ 未检测到 ALIBABA_CLOUD_ACCESS_KEY_ID 环境变量")
        log("  请先: source .env 或 export ALIBABA_CLOUD_ACCESS_KEY_ID=...")
        sys.exit(1)
    if not sk:
        log("✗ 未检测到 ALIBABA_CLOUD_ACCESS_KEY_SECRET 环境变量")
        log("  请先: source .env 或 export ALIBABA_CLOUD_ACCESS_KEY_SECRET=...")
        sys.exit(1)
    log("AK_ID: PRESENT ✓")
    log("AK_SECRET: PRESENT ✓")
    return {"ALIBABA_CLOUD_ACCESS_KEY_ID": ak, "ALIBABA_CLOUD_ACCESS_KEY_SECRET": sk}


def build_file_uri(path: Path) -> str:
    """构建 file:// URI。"""
    abs_path = str(path.resolve())
    return "file://" + urllib.parse.quote(abs_path, safe="/")


def read_line_with_timeout(proc, timeout: float = 5.0) -> str | None:
    """从子进程 stdout 读取一行，带超时。"""
    import select
    ready, _, _ = select.select([proc.stdout], [], [], timeout)
    if ready:
        line = proc.stdout.readline()
        if line:
            return line.rstrip("\n")
    return None


def send_jsonrpc(proc, payload: dict) -> None:
    """发送 JSON-RPC 请求到子进程 stdin。"""
    line = json.dumps(payload, ensure_ascii=False)
    proc.stdin.write(line + "\n")
    proc.stdin.flush()


def read_jsonrpc_response(proc, timeout: float = 60.0) -> dict | None:
    """从子进程 stdout 读取 JSON-RPC 响应行。"""
    line = read_line_with_timeout(proc, timeout)
    if line is None:
        return None
    try:
        return json.loads(line)
    except json.JSONDecodeError:
        log(f"  跳过非 JSON 行（前 100 字符）: {line[:100]}")
        return None


def handshake(proc) -> bool:
    """MCP 初始化握手: initialize → response, 然后 notifications/initialized。"""
    init_req = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "docmind-trial", "version": "1.0"},
        },
    }
    send_jsonrpc(proc, init_req)
    log("  已发送 initialize 请求")

    resp = read_jsonrpc_response(proc, timeout=30.0)
    if resp is None:
        log("✗ initialize 响应超时")
        return False
    if "error" in resp:
        log(f"✗ initialize 返回错误: {json.dumps(resp['error'], ensure_ascii=False)}")
        return False
    log("  initialize 握手成功 ✓")

    # 发送 initialized 通知
    initialized = {
        "jsonrpc": "2.0",
        "method": "notifications/initialized",
        "params": None,
    }
    send_jsonrpc(proc, initialized)
    time.sleep(0.3)
    return True


def call_convert_to_markdown(proc, uri: str, timeout: float = 120.0) -> dict | None:
    """调用 convert_to_markdown 工具。"""
    request = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/call",
        "params": {
            "name": "convert_to_markdown",
            "arguments": {"uri": uri},
        },
    }
    send_jsonrpc(proc, request)
    log(f"  已发送 tools/call，uri: {uri[:80]}...")

    start = time.time()
    last_response = None
    while time.time() - start < timeout:
        resp = read_jsonrpc_response(proc, timeout=10.0)
        if resp is None:
            continue
        last_response = resp
        if "id" in resp:
            # 这是对我们的 tools/call 的响应
            if "error" in resp:
                log(f"✗ tools/call 返回错误: {json.dumps(resp['error'], ensure_ascii=False)}")
                return resp
            log("  convert_to_markdown 调用成功 ✓")
            return resp
        else:
            # 可能是服务器通知或中间消息
            log(f"  收到非响应消息: {json.dumps(resp, ensure_ascii=False)[:200]}")
    log("✗ tools/call 超时")
    return last_response


def extract_markdown_text(response: dict) -> str | None:
    """从 MCP 响应中提取 Markdown 文本。"""
    try:
        result = response.get("result", {})
        content = result.get("content", [])
        if not content:
            log(f"  响应 result 中没有 content 字段，result keys: {list(result.keys())}")
            return None
        texts = []
        for item in content:
            if isinstance(item, dict) and item.get("type") == "text":
                texts.append(item.get("text", ""))
            elif isinstance(item, str):
                texts.append(item)
        combined = "\n".join(texts)
        if combined.strip():
            return combined
        log(f"  content 存在但未提取到文本，content 结构摘要: {json.dumps(content, ensure_ascii=False)[:300]}")
    except Exception as e:
        log(f"  Markdown 提取异常: {e}")
    return None


def drain_stderr(proc) -> list[str]:
    """排干 stderr 缓冲区，返回所有错误行。"""
    lines = []
    import select
    while True:
        ready, _, _ = select.select([proc.stderr], [], [], 0.1)
        if not ready:
            break
        line = proc.stderr.readline()
        if not line:
            break
        lines.append(line.rstrip("\n"))
    return lines


def shutdown_server(proc) -> None:
    """优雅关闭 MCP 服务器。"""
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


def process_sample(slug: str, label: str, env: dict, force: bool = False) -> bool:
    """处理单个样本 PDF。"""
    pdf_path = INPUT_DIR / f"{slug}_pages_001_010.pdf"
    raw_path = RAW_DIR / f"{slug}_pages_001_010.raw.json"
    md_path = MD_DIR / f"{slug}_pages_001_010.md"

    if not pdf_path.is_file():
        log(f"✗ {label} 样本 PDF 不存在: {pdf_path}")
        return False

    if md_path.is_file() and not force:
        log(f"⊙ {label} Markdown 已存在，跳过（用 --force 强制重新生成）")
        return True

    uri = build_file_uri(pdf_path)
    log(f"  文件 URI: {uri}")

    # 启动 MCP 服务器
    env_full = os.environ.copy()
    env_full.update(env)

    log(f"  启动 uvx docmind-parser-mcp ...")
    try:
        proc = subprocess.Popen(
            ["uvx", "docmind-parser-mcp"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            env=env_full,
        )
    except FileNotFoundError:
        log("✗ uvx 命令不可用")
        return False
    except Exception as e:
        log(f"✗ 启动子进程失败: {e}")
        return False

    try:
        # 握手
        if not handshake(proc):
            stderr_lines = drain_stderr(proc)
            for l in stderr_lines:
                log(f"  [stderr] {l}")
            return False

        # 调用 convert_to_markdown
        resp = call_convert_to_markdown(proc, uri)
        if resp is None:
            return False

        # 保存原始响应
        raw_path.parent.mkdir(parents=True, exist_ok=True)
        raw_path.write_text(json.dumps(resp, ensure_ascii=False, indent=2), encoding="utf-8")
        log(f"  原始响应已保存: {raw_path.name}")

        # 检查错误
        if "error" in resp:
            err = resp["error"]
            log(f"✗ MCP 返回错误: {json.dumps(err, ensure_ascii=False)[:500]}")
            err_msg = str(err).lower()
            if "file" in err_msg and ("not supported" in err_msg or "invalid" in err_msg or "unsupported" in err_msg):
                log("")
                log("=" * 60)
                log("该 docmind-parser-mcp 版本可能不支持本地 file:// URI。")
                log("请将样本 PDF 上传到阿里云 OSS，然后设置环境变量：")
                log("  export DOCMIND_TUTORIAL_SAMPLE_URI='https://...'")
                log("  export DOCMIND_QUESTIONS_SAMPLE_URI='https://...'")
                log("之后重新运行本脚本。")
                log("=" * 60)
            return False

        # 提取 Markdown
        md_text = extract_markdown_text(resp)
        if md_text is None:
            log(f"✗ 无法从响应中提取 Markdown 文本")
            return False

        md_path.parent.mkdir(parents=True, exist_ok=True)
        md_path.write_text(md_text, encoding="utf-8")
        log(f"  Markdown 已保存: {md_path.name} ({len(md_text)} 字符)")

        return True

    finally:
        shutdown_server(proc)


def main():
    force = "--force" in sys.argv

    os.makedirs(RAW_DIR, exist_ok=True)
    os.makedirs(MD_DIR, exist_ok=True)
    os.makedirs(LOGS_DIR, exist_ok=True)

    log("===== MCP 转换开始 =====")

    # 加载 .env 文件（如果存在）
    env_path = PROJECT_ROOT / ".env"
    if env_path.is_file():
        log("检测到 .env 文件，加载环境变量...")
        for line in env_path.read_text().split("\n"):
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, _, val = line.partition("=")
                if key and val and key not in os.environ:
                    os.environ[key] = val

    env = check_env()

    # 检查是否设置了 OSS URL 环境变量
    tutorial_uri_env = os.getenv("DOCMIND_TUTORIAL_SAMPLE_URI")
    questions_uri_env = os.getenv("DOCMIND_QUESTIONS_SAMPLE_URI")

    results = {}
    for sample in SAMPLES:
        log(f"\n--- 处理 {sample['label']} ---")
        ok = process_sample(sample["slug"], sample["label"], env, force=force)
        results[sample["slug"]] = ok

    log("\n===== MCP 转换完成 =====")
    for slug, ok in results.items():
        status = "✓ 成功" if ok else "✗ 失败"
        log(f"  {slug}: {status}")

    if not all(results.values()):
        log("\n部分/全部转换失败，请检查上述错误信息。")
        sys.exit(1)


if __name__ == "__main__":
    main()
