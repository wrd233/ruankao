# OCR Skill 对比实验建议

## 1. 安装情况

- 安装成功：
  - `aidenwu0209/paddleocr-skills@paddleocr-text-recognition`
  - `dkyazzentwatwa/chatgpt-skills@ocr-document-processor`
  - `claude-office-skills/skills@"PDF OCR Extraction"`（兼容命名补试）
- 安装失败：
  - `claude-office-skills/skills@pdf-ocr-extraction` 这个精确字符串在当前 Skills CLI 下未命中
- 环境风险：
  - `paddleocr-text-recognition` 依赖外部 API 和令牌，不是本地可复现实验
  - `ocr-document-processor` 需额外依赖，已通过 `outputs/ocr_skill_trials/.venv` 局部隔离解决，没有修改主 OCR 环境

## 2. 运行情况

- 能实际运行：
  - `ocr-document-processor`
- 已安装但当前会话无法运行：
  - `pdf-ocr-extraction`
    - 原因：依赖当前会话不存在的 `office-mcp.extract_text_from_pdf`
  - `paddleocr-text-recognition`
    - 原因：缺少 `PADDLEOCR_OCR_API_URL` / `PADDLEOCR_ACCESS_TOKEN`

## 3. 质量对比

### 普通正文页

- `ocr-document-processor` 对中文正文页没有提升，反而普遍更差。
- 代表页：
  - `official_tutorial/page_002`
  - `official_tutorial/page_006`
  - `official_tutorial/page_675`
- 当前基线能保持较多中文字符和段落顺序；skill 输出出现大量英文字母化乱码。

### 低质量页

- 真正的空白/尾页：
  - `official_tutorial/page_022`
  - `official_tutorial/page_678`
- 通过视觉抽检可确认这两页基本就是空白/噪声页，当前基线“空文本”并不是实质性缺陷。
- 对真正有内容但基线失败的页：
  - `past_papers_171/page_084`
  - `past_papers_171/page_086`
  - `past_papers_171/page_093`
  - `past_papers_171/page_171`
- `ocr-document-processor` 没有补救成功，仍为空或严重乱码。

### 题目页

- 英文题页：
  - `past_papers_171/page_014`
- `ocr-document-processor` 与当前基线大体相近，但没有明显更好；“解析”标签反而退化成 `fF AT`、`fe AT` 一类噪声。
- 中文题页：
  - `past_papers_171/page_001`
  - `past_papers_171/page_003`
  - `past_papers_171/page_034`
  - `past_papers_171/page_167`
- `ocr-document-processor` 普遍不如基线，题号、选项和解析结构更容易粘连或变形。

### 表格 / 图示 / 公式页

- `official_tutorial/page_339`、`page_340` 的图示结构没有因为 skill 而改善。
- `past_papers_171/page_171` 的表格/题目内容在当前基线和 skill 下都没有稳定抽出。
- 当前没有证据表明这些 skill 对图表、表格、黄色高亮答案页有结构性提升。

## 4. 总体建议

- 是否建议全量重跑：否
- 是否建议仅用于低质量页补强：否
- 是否建议保留当前 PyMuPDF + pytesseract 作为主流水线：是
- 是否建议把某些页面的 skill 输出并入正式索引：否

## 5. 建议用 skill 结果补强的页面

当前没有页面达到“skill 结果明显优于现有基线，可直接作为替换候选”的标准。

| 文件 | 页码 | 当前 OCR 问题 | 更好的结果来源 | 建议动作 |
|---|---:|---|---|---|
| 暂无 | - | - | - | 保留当前主结果 |

## 6. 仍需人工或多模态复核

- `past_papers_171/page_084`：视觉上有真实内容，但当前基线与 `ocr-document-processor` 都为空。
- `past_papers_171/page_086`：视觉上是高亮答案页，当前基线和 skill 都不可可靠引用。
- `past_papers_171/page_093`：视觉上是高亮长段解析页，两个方案都未成功抽出。
- `past_papers_171/page_171`：视觉上存在高亮文字与表格，两个方案都失败，优先级最高。
- `official_tutorial/page_339`：若后续需要重绘图 8-10，仍建议人工看图，不要直接依赖 OCR 文本。
- `official_tutorial/page_340`：若后续需要重绘跟踪横道图，仍建议人工看图。

## 7. 对原 review queue 的修正建议

- `official_tutorial/page_022`：
  - 建议从“需 OCR 复核”降级为“确认空白/分隔页”
- `official_tutorial/page_678`：
  - 建议从“需 OCR 复核”降级为“确认尾页/噪声页”
- `official_tutorial/page_423`：
  - 视觉抽检表明当前基线实际上已经足够可用，不建议用 skill 替换
- `past_papers_171/page_171`：
  - 应从“疑似封底或扫描结束页”更正为“实际有内容但 OCR 失败”

## 8. 下一步建议

- 如果要继续探索更强 OCR，不建议再围绕当前这几个 skill 做全量工作。
- 更值得尝试的是：
  - 直接对 `past_papers_171/page_084`、`086`、`093`、`171` 试本地 `PaddleOCR Python 包`，而不是 API skill 包装器
  - 对高亮答案页采用多模态看图复核
  - 对图表示例页单独做“看图转结构化摘要”，而不是只追求逐字 OCR
