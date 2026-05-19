# OCR 专项工作清单

## 目标 PDF
| 编号 | 文件名 | 路径 | 页数 | 当前文本层情况 | 上轮缺口说明 |
|---|---|---|---:|---|---|
| PDF-01 | 《系统集成项目管理工程师教程》官方考试指定第二版.pdf | `./《系统集成项目管理工程师教程》官方考试指定第二版.pdf` | 678 | 原始 PDF 抽样页 `get_text()` 全为 0；已补生成 `outputs/ocr/pdf/官方教程_ocr.pdf` 与页级文本 | 上轮未能提取正文，缺少官方教材页级索引与权威引用锚点 |
| PDF-02 | 历年系统集成项目管理工程师试题解析及答案-171页.pdf | `./历年系统集成项目管理工程师试题解析及答案-171页.pdf` | 171 | 原始 PDF 抽样页 `get_text()` 全为 0；已补生成 `outputs/ocr/pdf/历年题解析_171页_ocr.pdf` 与页级文本 | 上轮未能稳定 OCR，缺少更大覆盖面的真题题号、选项、解析映射 |

## OCR 工具环境
| 工具 | 是否可用 | 版本 | 备注 |
|---|---|---|---|
| ocrmypdf | 是 | 15.4.4 | 运行于 `outputs/ocr/.venv`；样本可生成 PDF/A，但文本抽取稳定性不足 |
| tesseract | 是 | 5.5.2 | Homebrew 安装 |
| tesseract chi_sim | 是 | `chi_sim.traineddata` | 下载到 `outputs/ocr/tessdata/` |
| pdftotext | 否 | - | 本机无该命令 |
| python | 是 | 3.9.6 | OCR 脚本运行环境 |
| pymupdf/fitz | 是 | 1.26.5 | 用于渲染页面与文本抽样 |
| pdf2image | 是 | 1.17.0 | 已装，最终主流程未采用 |
| pytesseract | 是 | 0.3.13 | 当前主 OCR 方案 |
| paddleocr | 否 | - | 当前环境未安装，未强行改动系统 |

## 本轮计划
- 第一阶段：核验目标 PDF、工具环境、文本层现状，并将命令输出落盘到 `outputs/ocr/logs/tool_check.log`。
- 第二阶段：先试 `ocrmypdf + tesseract` 样本，再试 `PyMuPDF + pytesseract` 样本，比较是否能稳定得到可用文本与 OCR PDF。
- 第三阶段：采用可重复的 Python 页级 OCR 流水线全量处理两份 PDF，输出 OCR PDF、页级文本、质量评估、复核页清单与索引补强报告。
