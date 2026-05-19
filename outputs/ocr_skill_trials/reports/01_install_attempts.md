# OCR Skill 安装与运行尝试记录

## 环境前提

- 当前仓库根目录：`/Users/wangrundong/work/软考`
- `npx`：可用
- `uv`：可用，版本 `0.9.7`
- `tesseract`：可用，版本 `5.5.2`
- PaddleOCR API 环境变量：
  - `PADDLEOCR_OCR_API_URL`：未配置
  - `PADDLEOCR_ACCESS_TOKEN`：未配置

## Skill: claude-office-skills/skills@pdf-ocr-extraction

- **安装命令**：
  `npx skills add claude-office-skills/skills@pdf-ocr-extraction -g -y`
- **是否成功**：否（精确 skill id 未匹配）
- **安装日志**：
  `outputs/ocr_skill_trials/logs/install_pdf_ocr_extraction.log`
- **失败/警告**：
  - Skills CLI 能拉取仓库并列出 skill，但提示 `No matching skills found for: pdf-ocr-extraction`
  - 说明该 repo 内实际可安装名与用户给定字符串不完全一致
- **可用命令或入口**：无
- **依赖情况**：未进入运行阶段
- **实测页面**：无
- **输出目录**：无
- **初步判断**：用户给定安装串在当前 Skills CLI 下不能直接命中

### 兼容命名补试

- **安装命令**：
  `npx skills add "claude-office-skills/skills@PDF OCR Extraction" -g -y`
- **是否成功**：是
- **安装日志**：
  `outputs/ocr_skill_trials/logs/install_pdf_ocr_extraction_named.log`
- **安装位置**：
  `~/.agents/skills/pdf-ocr-extraction`
- **可用命令或入口**：
  - 仅发现 `SKILL.md`
  - 未发现本地 `scripts/`、CLI、可直接调用的 Python 入口
- **依赖情况**：
  - `SKILL.md` 声明依赖 `office-mcp` 的 `extract_text_from_pdf`
  - 当前会话工具集中没有该 MCP 工具
- **实测页面**：无
- **输出目录**：无
- **初步判断**：
  - 可安装，但在当前会话里不可实际运行
  - 问题不在 OCR 算法，而在 skill 运行入口依赖当前不存在的 MCP 能力

## Skill: aidenwu0209/paddleocr-skills@paddleocr-text-recognition

- **安装命令**：
  `npx skills add aidenwu0209/paddleocr-skills@paddleocr-text-recognition -g -y`
- **是否成功**：是
- **安装日志**：
  `outputs/ocr_skill_trials/logs/install_paddleocr_skill.log`
- **安装位置**：
  `~/.agents/skills/paddleocr-text-recognition`
- **可用命令或入口**：
  - `scripts/ocr_caller.py`
  - `scripts/lib.py`
- **依赖情况**：
  - Skill 不是本地 PaddleOCR 包封装，而是外部 PaddleOCR API 包装器
  - 强依赖环境变量：
    - `PADDLEOCR_OCR_API_URL`
    - `PADDLEOCR_ACCESS_TOKEN`
  - 当前环境未配置这两个值
- **实测页面**：
  - `official_tutorial/page_423`
  - `past_papers_171/page_014`
- **运行日志**：
  - `outputs/ocr_skill_trials/logs/run_paddle_page_423.log`
  - `outputs/ocr_skill_trials/logs/run_paddle_page_014.log`
- **输出目录**：无成功输出
- **实际运行结果**：
  - 两次都返回：
    - `CONFIG_ERROR`
    - `PADDLEOCR_OCR_API_URL not configured`
- **初步判断**：
  - 可安装，但当前仓库环境中不可直接运行
  - 若要继续评估，必须补充外部 API 服务与访问令牌
  - 这不适合当作当前仓库的可复现实验主方案

## Skill: dkyazzentwatwa/chatgpt-skills@ocr-document-processor

- **安装命令**：
  `npx skills add dkyazzentwatwa/chatgpt-skills@ocr-document-processor -g -y`
- **是否成功**：是
- **安装日志**：
  `outputs/ocr_skill_trials/logs/install_ocr_document_processor.log`
- **安装位置**：
  `~/.agents/skills/ocr-document-processor`
- **可用命令或入口**：
  - `scripts/ocr_processor.py`
  - `scripts/business_card_scanner.py`
  - `scripts/receipt_scanner.py`
- **依赖情况**：
  - 脚本本身依赖：
    - `numpy`
    - `Pillow`
    - `pytesseract`
    - `PyMuPDF`
  - 直接用现有环境首跑失败：
    - `ModuleNotFoundError: No module named 'numpy'`
  - 为避免污染主环境，单独创建实验虚拟环境：
    - `outputs/ocr_skill_trials/.venv`
  - 局部安装日志：
    - `outputs/ocr_skill_trials/logs/install_ocr_document_processor_deps.log`
- **实测页面**：
  - 全部样本页，共 20 页
- **运行日志**：
  - 首次失败：
    - `outputs/ocr_skill_trials/logs/run_ocr_document_processor_page_423.log`
    - `outputs/ocr_skill_trials/logs/run_ocr_document_processor_page_025.log`
  - 隔离环境补依赖后全量样本运行：
    - `outputs/ocr_skill_trials/logs/run_ocr_document_processor_samples.log`
- **输出目录**：
  - `outputs/ocr_skill_trials/pages/ocr_document_processor/`
- **初步判断**：
  - 这是本轮唯一“安装成功且能在当前仓库里实跑”的 OCR skill
  - 但它本质仍是 `pytesseract` 封装，和现有主流水线同源
  - 对中文扫描页、图示页、题目高亮页没有表现出明显优势

## 补充说明：smart-ocr

- 在排查 `claude-office-skills` repo 时补装过 `smart-ocr`
- 安装日志：
  `outputs/ocr_skill_trials/logs/install_smart_ocr.log`
- 该 skill 也主要依赖 `office-mcp` 工具，而非本地脚本
- 不属于用户要求的正式对比对象，因此未纳入后续页级比较
