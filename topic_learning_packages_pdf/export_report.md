# 本轮交付总结

## 1. PDF 导出结果

- 扫描 Markdown 数量：38
- 成功生成 PDF 数量：38
- 失败数量：0
- 使用的导出工具：Chrome headless (`/Applications/Google Chrome.app/Contents/MacOS/Google Chrome`)
- 中文字体：强制加载 macOS `STHeiti` 与 `Songti.ttc`，避免 Chrome headless 中文正文缺字
- Mermaid 处理方式：浏览器端 Mermaid CDN 渲染，累计 Mermaid 代码块 83 个

### 失败文件列表

- 无

## 2. 学习路线

- 输出文件：`topic_learning_packages/study_plan/学习路线与打卡TODO.md`
- 覆盖阶段：准备与总览、项目管理主线、计算题专项、下午案例专项、上午零散考点补漏、真题回流与复盘
- TODO 数量：79 个复选框
- 建议使用方式：按阶段打卡，错题回流到专题和零散题库，待核验点不直接制成稳定记忆卡

## 3. Anki 试制

- 选择专题：`T-COST-002｜挣值管理与成本绩效分析`
- 卡片总数：56
- 卡片类型分布：概念 12、公式 11、计算 10、辨析 10、案例 6、陷阱 7
- 是否生成 `deck.apkg`：是
- 导入 Anki 的方法：优先直接导入 `anki_pilot/T-COST-002/deck.apkg`；也可用 `cards.tsv` 按表头字段导入
- 需要人工检查的卡片：`CPI × SPI` 的 EAC 扩展公式卡、案例模板措辞、计算题四舍五入口径
- 详见：`anki_pilot/T-COST-002/generation_report.md`

## 4. 后续建议

- PDF 导出流程在当前环境下可复用；若后续需要离线 Mermaid，可安装 `mmdc` 并扩展脚本。
- 建议人工抽查表格较宽、公式较多、Mermaid 图较多的 PDF。
- Anki 试制通过后，再扩展到全量专题；扩展前先处理高优先级 `[待核验]`。
