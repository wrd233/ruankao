# OCR Skill 对比实验工作清单

## 实验目标

- 验证指定 OCR skill 是否能在当前仓库环境中安装并实际运行。
- 对低质量页、图表页、表格页、公式/题目结构页做小范围对比。
- 不覆盖当前 `outputs/ocr/` 主结果，只在 `outputs/ocr_skill_trials/` 下独立保存实验产物。

## 当前基线

- 主 OCR 流水线：`PyMuPDF + pytesseract (chi_sim+eng)`
- 基线文本来源：`outputs/ocr/pages/`
- 基线质量参考：
  - `outputs/ocr/reports/02_ocr_quality_report.md`
  - `outputs/ocr/review_queue/low_quality_pages.md`

## 本轮实验目录

- `outputs/ocr_skill_trials/logs/`
- `outputs/ocr_skill_trials/pages/current_baseline/`
- `outputs/ocr_skill_trials/pages/source_images/`
- `outputs/ocr_skill_trials/pages/pdf_ocr_extraction/`
- `outputs/ocr_skill_trials/pages/paddleocr_text_recognition/`
- `outputs/ocr_skill_trials/pages/ocr_document_processor/`
- `outputs/ocr_skill_trials/reports/`
- `outputs/ocr_skill_trials/scripts/`

## 对比 skill

| 优先级 | Skill | 目标状态 |
|---|---|---|
| 1 | `claude-office-skills/skills@pdf-ocr-extraction` | 安装并实跑 |
| 2 | `aidenwu0209/paddleocr-skills@paddleocr-text-recognition` | 安装并实跑 |
| 3 | `dkyazzentwatwa/chatgpt-skills@ocr-document-processor` | 前两者不可用时补试 |

## 样本页

### 官方教程

- 必选低质量页：`page_022`、`page_423`、`page_678`
- 图表/结构页：`page_338`、`page_339`、`page_340`
- 正文对照页：`page_002`、`page_006`、`page_675`

### 历年题解析

- 必选低质量页：`page_014`、`page_025`、`page_084`、`page_086`、`page_093`、`page_171`
- 普通题目页：`page_001`、`page_003`、`page_167`
- 题目密集或混合结构页：`page_034`、`page_085`

## 样本准备方式

- 用 `outputs/ocr_skill_trials/scripts/run_skill_trials.py` 从基线 OCR 复制样本页文本到 `pages/current_baseline/`。
- 同一脚本从原始 PDF 渲染样本页 PNG 到 `pages/source_images/`，用于视觉抽检和 skill 输入。
- 用 `outputs/ocr_skill_trials/scripts/compare_ocr_outputs.py` 汇总页级统计到：
  - `outputs/ocr_skill_trials/reports/sample_pages_manifest.json`
  - `outputs/ocr_skill_trials/reports/sample_pages_comparison.json`

## 本轮实际采用的方法

### 方案 A｜skill 安装验证

- 使用 `npx skills add ... -g -y`
- 完整安装输出保存到 `outputs/ocr_skill_trials/logs/`

### 方案 B｜skill 运行验证

- `pdf-ocr-extraction`：检查是否生成可执行入口或当前会话可用工具
- `paddleocr-text-recognition`：直接调用 skill 自带 `scripts/ocr_caller.py`
- `ocr-document-processor`：直接调用 skill 自带 `scripts/ocr_processor.py`

### 方案 C｜视觉抽检

- 对强制低质量页和若干代表页渲染原图并做人工视觉核对
- 本轮已做视觉核对的重点页包括：
  - 官方教程：`022`、`423`、`678`
  - 历年题解析：`014`、`025`、`084`、`086`、`093`、`171`

## 注意事项

- 本轮没有覆盖 `outputs/ocr/pages/` 任何文件。
- 未全量重跑 PDF；仅处理抽样页。
- 若 skill 仅“安装成功”但“当前会话不可运行”，单独记为“已安装、未实跑”。
