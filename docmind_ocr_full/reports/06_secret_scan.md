# Security Scan Report

Generated: 2026-05-19 12:34:41

## Scan Summary

| Category | Count |
|----------|-------|
| Real leaks | 0 |
| False positives | 25 |
| Uncertain | 2 |

## False Positives (Documented)

- `docmind_ocr_trial/reports/preflight_report.md:17:- ALIBABA_CLOUD_ACCESS_KEY_ID: PRESENT`
- `docmind_ocr_trial/reports/preflight_report.md:18:- ALIBABA_CLOUD_ACCESS_KEY_SECRET: PRESENT`
- `docmind_ocr_trial/scripts/00_preflight.py:84:    ak = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID")`
- `docmind_ocr_trial/scripts/00_preflight.py:85:    sk = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET")`
- `docmind_ocr_trial/scripts/00_preflight.py:126:        verdicts.append("AK not set, run: export ALIBABA_CLOUD_ACCESS_KEY_`
- `docmind_ocr_trial/scripts/00_preflight.py:148:- ALIBABA_CLOUD_ACCESS_KEY_ID: {ak_status}`
- `docmind_ocr_trial/scripts/00_preflight.py:149:- ALIBABA_CLOUD_ACCESS_KEY_SECRET: {sk_status}`
- `docmind_ocr_trial/scripts/02_mcp_convert_to_markdown.py:46:    ak = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID")`
- `docmind_ocr_trial/scripts/02_mcp_convert_to_markdown.py:47:    sk = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET")`
- `docmind_ocr_trial/scripts/02_mcp_convert_to_markdown.py:49:        log("✗ 未检测到 ALIBABA_CLOUD_ACCESS_KEY_ID 环境变量")`
- ... and 15 more

## Uncertain — Review Manually

- `docmind_ocr_trial/scripts/00_preflight.py:89:    log(f"AK_SECRET: {sk_status}")`
- `docmind_ocr_trial/scripts/02_mcp_convert_to_markdown.py:57:    log("AK_SECRET: PRESENT ✓")`

## Verdict: PASS
