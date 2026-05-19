# OCR 尝试日志

## Attempt 001｜环境核验：基础 OCR 工具检查

- **时间**：2026-05-19
- **目标文件**：工具环境
- **命令**：

```bash
which ocrmypdf || true
ocrmypdf --version || true
which tesseract || true
tesseract --version || true
tesseract --list-langs || true
which pdftotext || true
pdftotext -v || true
python3 --version || true
```

- **退出码**：0
- **耗时**：< 1 min
- **输出文件**：`outputs/ocr/logs/tool_check.log`
- **日志文件**：`outputs/ocr/logs/tool_check.log`
- **结果判断**：
  - 部分成功
- **失败原因或警告**：
  - 初始环境无 `ocrmypdf`、`pdftotext`、`pdfinfo`
  - `tesseract` 初始仅有 `eng/osd/snum`，缺少 `chi_sim`
  - Python 初始无 `fitz`、`pytesseract`、`pdf2image`
- **下一步处理**：
  - 建立隔离虚拟环境并补本地依赖与中文语言包

## Attempt 002｜本地依赖准备：venv + OCR 栈安装

- **时间**：2026-05-19
- **目标文件**：OCR 运行环境
- **命令**：

```bash
python3 -m venv outputs/ocr/.venv
source outputs/ocr/.venv/bin/activate
python -m pip install --upgrade pip setuptools wheel
python -m pip install pymupdf pytesseract pypdf ocrmypdf pdf2image
```

- **退出码**：0
- **耗时**：约 3 min
- **输出文件**：`outputs/ocr/.venv/`
- **日志文件**：
  - `outputs/ocr/logs/pip_upgrade.log`
  - `outputs/ocr/logs/pip_install_ocr_stack.log`
- **结果判断**：
  - 成功
- **失败原因或警告**：
  - 无
- **下一步处理**：
  - 下载本地 `chi_sim` / `chi_sim_vert` 语言包并复检环境

## Attempt 003｜语言包补强：chi_sim / chi_sim_vert

- **时间**：2026-05-19
- **目标文件**：本地 tessdata
- **命令**：

```bash
curl -L https://github.com/tesseract-ocr/tessdata_best/raw/main/chi_sim.traineddata -o outputs/ocr/tessdata/chi_sim.traineddata
curl -L https://github.com/tesseract-ocr/tessdata_best/raw/main/chi_sim_vert.traineddata -o outputs/ocr/tessdata/chi_sim_vert.traineddata
```

- **退出码**：0
- **耗时**：约 1 min
- **输出文件**：`outputs/ocr/tessdata/`
- **日志文件**：
  - `outputs/ocr/logs/download_chi_sim.log`
  - `outputs/ocr/logs/download_chi_sim_vert.log`
- **结果判断**：
  - 成功
- **失败原因或警告**：
  - 无
- **下一步处理**：
  - 试跑 `ocrmypdf + tesseract`

## Attempt 004｜ocrmypdf 样本 OCR：历年题解析（Ghostscript 缺失）

- **时间**：2026-05-19
- **目标文件**：`历年系统集成项目管理工程师试题解析及答案-171页.pdf`
- **命令**：

```bash
source outputs/ocr/.venv/bin/activate
export TESSDATA_PREFIX="/Users/wangrundong/work/软考/outputs/ocr/tessdata"
ocrmypdf -l chi_sim+eng --deskew --rotate-pages --skip-text --pages 1-3           "历年系统集成项目管理工程师试题解析及答案-171页.pdf"           "outputs/ocr/pdf/past_papers_171_sample_ocr.pdf"
```

- **退出码**：3
- **耗时**：0.20 s
- **输出文件**：未生成可用 PDF
- **日志文件**：`outputs/ocr/logs/attempt_ocrmypdf_past_papers_sample.log`
- **结果判断**：
  - 失败
- **失败原因或警告**：
  - `gs` 不存在，`ocrmypdf` 直接退出
- **下一步处理**：
  - 安装 Ghostscript 后重试

## Attempt 005｜系统依赖补充：Ghostscript

- **时间**：2026-05-19
- **目标文件**：OCR 系统依赖
- **命令**：

```bash
brew install ghostscript
```

- **退出码**：0
- **耗时**：约 4 min
- **输出文件**：系统命令 `gs`
- **日志文件**：`outputs/ocr/logs/brew_install_ghostscript.log`
- **结果判断**：
  - 成功
- **失败原因或警告**：
  - 无
- **下一步处理**：
  - 重试 `ocrmypdf` 样本

## Attempt 006｜ocrmypdf 样本 OCR：历年题解析（成功生成 PDF/A）

- **时间**：2026-05-19
- **目标文件**：`历年系统集成项目管理工程师试题解析及答案-171页.pdf`
- **命令**：

```bash
source outputs/ocr/.venv/bin/activate
export TESSDATA_PREFIX="/Users/wangrundong/work/软考/outputs/ocr/tessdata"
ocrmypdf -l chi_sim+eng --deskew --rotate-pages --skip-text --pages 1-3           "历年系统集成项目管理工程师试题解析及答案-171页.pdf"           "outputs/ocr/pdf/past_papers_171_sample_ocr.pdf"
```

- **退出码**：0
- **耗时**：18.50 s
- **输出文件**：`outputs/ocr/pdf/past_papers_171_sample_ocr.pdf`
- **日志文件**：`outputs/ocr/logs/attempt_ocrmypdf_past_papers_sample.log`
- **结果判断**：
  - 部分成功
- **失败原因或警告**：
  - PDF/A 成功生成，但随后用 `PyMuPDF` / `pypdf` 抽取文本层时得到 0 字符，无法作为稳定的后续引用基础
- **下一步处理**：
  - 继续试跑官方教程样本，并同时准备 Python 页级 OCR 备用方案

## Attempt 007｜ocrmypdf 样本 OCR：官方教程（成功生成 PDF/A）

- **时间**：2026-05-19
- **目标文件**：`《系统集成项目管理工程师教程》官方考试指定第二版.pdf`
- **命令**：

```bash
source outputs/ocr/.venv/bin/activate
export TESSDATA_PREFIX="/Users/wangrundong/work/软考/outputs/ocr/tessdata"
ocrmypdf -l chi_sim+eng --deskew --rotate-pages --skip-text --pages 1-3           "《系统集成项目管理工程师教程》官方考试指定第二版.pdf"           "outputs/ocr/pdf/official_tutorial_sample_ocr.pdf"
```

- **退出码**：0
- **耗时**：16.64 s
- **输出文件**：`outputs/ocr/pdf/official_tutorial_sample_ocr.pdf`
- **日志文件**：`outputs/ocr/logs/attempt_ocrmypdf_official_sample.log`
- **结果判断**：
  - 部分成功
- **失败原因或警告**：
  - 样本 OCR PDF 成功生成，但抽取文本层仍不稳定，无法作为正式页级索引来源
- **下一步处理**：
  - 转为 `PyMuPDF + pytesseract` 主流程

## Attempt 008｜PyMuPDF + pytesseract 样本 OCR：两份 PDF 抽样页

- **时间**：2026-05-19
- **目标文件**：
  - `《系统集成项目管理工程师教程》官方考试指定第二版.pdf`
  - `历年系统集成项目管理工程师试题解析及答案-171页.pdf`
- **命令**：

```bash
source outputs/ocr/.venv/bin/activate
python - <<'PY'
# 渲染 page 1-3 / page 34，使用 pytesseract.image_to_string(lang="chi_sim+eng")
PY
```

- **退出码**：0
- **耗时**：约 13 s
- **输出文件**：
  - `outputs/ocr/logs/sample_texts/official_sample.txt`
  - `outputs/ocr/logs/sample_texts/past_sample.txt`
- **日志文件**：上述样本文本文件
- **结果判断**：
  - 成功
- **失败原因或警告**：
  - 封面、图示与少量字符有误识别
- **下一步处理**：
  - 将该路线写成可重复运行脚本，并在页级保留质量标记

## Attempt 009｜Python OCR 流水线样本：官方教程 / 历年题解析

- **时间**：2026-05-19
- **目标文件**：两份 PDF 的前 3 页
- **命令**：

```bash
source outputs/ocr/.venv/bin/activate
python outputs/ocr/scripts/ocr_scan_pdfs.py --pdf "《系统集成项目管理工程师教程》官方考试指定第二版.pdf" --slug official_tutorial_sample_pipeline --output-pdf-name official_tutorial_sample_pipeline.pdf --start-page 1 --end-page 3
python outputs/ocr/scripts/ocr_scan_pdfs.py --pdf "历年系统集成项目管理工程师试题解析及答案-171页.pdf" --slug past_papers_171_sample_pipeline --output-pdf-name past_papers_171_sample_pipeline.pdf --start-page 1 --end-page 3
```

- **退出码**：0
- **耗时**：
  - 官方教程样本：33.00 s
  - 历年题样本：31.92 s
- **输出文件**：
  - `outputs/ocr/pages/official_tutorial_sample_pipeline/`
  - `outputs/ocr/pages/past_papers_171_sample_pipeline/`
- **日志文件**：
  - `outputs/ocr/logs/attempt_python_pipeline_official_sample.log`
  - `outputs/ocr/logs/attempt_python_pipeline_past_sample.log`
- **结果判断**：
  - 成功
- **失败原因或警告**：
  - 生成的 OCR PDF 仍不适合作为唯一文本来源，因此页级 `.txt` 保持为权威产物
- **下一步处理**：
  - 全量跑两份 PDF

## Attempt 010｜Python OCR 全量：历年题解析 171 页

- **时间**：2026-05-19
- **目标文件**：`历年系统集成项目管理工程师试题解析及答案-171页.pdf`
- **命令**：

```bash
source outputs/ocr/.venv/bin/activate
python outputs/ocr/scripts/ocr_scan_pdfs.py           --pdf "历年系统集成项目管理工程师试题解析及答案-171页.pdf"           --slug past_papers_171           --output-pdf-name 历年题解析_171页_ocr.pdf
```

- **退出码**：0
- **耗时**：727.40 s
- **输出文件**：
  - `outputs/ocr/pdf/历年题解析_171页_ocr.pdf`
  - `outputs/ocr/pages/past_papers_171/`
- **日志文件**：`outputs/ocr/logs/attempt_python_pipeline_past_full.log`
- **结果判断**：
  - 成功
- **失败原因或警告**：
  - 3 页 `review`、3 页 `empty`，已进入复核队列
- **下一步处理**：
  - 全量跑官方教程并统一做质量评估

## Attempt 011｜Python OCR 全量：官方教程 678 页

- **时间**：2026-05-19
- **目标文件**：`《系统集成项目管理工程师教程》官方考试指定第二版.pdf`
- **命令**：

```bash
source outputs/ocr/.venv/bin/activate
python outputs/ocr/scripts/ocr_scan_pdfs.py           --pdf "《系统集成项目管理工程师教程》官方考试指定第二版.pdf"           --slug official_tutorial           --output-pdf-name 官方教程_ocr.pdf
```

- **退出码**：0
- **耗时**：1939.45 s
- **输出文件**：
  - `outputs/ocr/pdf/官方教程_ocr.pdf`
  - `outputs/ocr/pages/official_tutorial/`
- **日志文件**：`outputs/ocr/logs/attempt_python_pipeline_official_full.log`
- **结果判断**：
  - 成功
- **失败原因或警告**：
  - 2 页 `review`、1 页 `empty`，已进入复核队列
- **下一步处理**：
  - 生成质量报告、补强索引与质量更新
