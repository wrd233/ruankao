# PDF 导出环境探测

> 生成脚本：`scripts/export_topic_packages_to_pdf.py`

## 工具探测

| 工具 | 路径/状态 |
|---|---|
| `pandoc` | `not found` |
| `xelatex` | `not found` |
| `wkhtmltopdf` | `not found` |
| `weasyprint` | `not found` |
| `node` | `/opt/homebrew/bin/node` |
| `npx` | `/opt/homebrew/bin/npx` |
| `mmdc` | `not found` |
| `chrome_headless` | `/Applications/Google Chrome.app/Contents/MacOS/Google Chrome` |
| `python` | `3.9.6` |

## 中文字体候选

- `/System/Library/Fonts/NotoSerifMyanmar.ttc: Noto Serif Myanmar,Noto Serif Myanmar SemBd:style=SemiBold,Regular`
- `/System/Library/Fonts/Supplemental/NotoSansKaithi-Regular.ttf: Noto Sans Kaithi:style=Regular`
- `/System/Library/Fonts/Supplemental/NotoSansYi-Regular.ttf: Noto Sans Yi:style=Regular`
- `/System/Library/Fonts/Supplemental/NotoSansMendeKikakui-Regular.ttf: Noto Sans Mende Kikakui:style=Regular`
- `/System/Library/Fonts/NotoSansMyanmar.ttc: Noto Sans Zawgyi,Noto Sans Zawgyi Blk:style=Black,Regular`
- `/System/Library/Fonts/Supplemental/NotoSansLydian-Regular.ttf: Noto Sans Lydian:style=Regular`
- `/System/Library/Fonts/Supplemental/NotoSansHanifiRohingya-Regular.ttf: Noto Sans Hanifi Rohingya,Noto Sans HanifiRohg:style=Regular`
- `/System/Library/Fonts/Supplemental/NotoSansSyriac-Regular.ttf: Noto Sans Syriac:style=ExtraBold`
- `/System/Library/Fonts/Supplemental/NotoSansOldPersian-Regular.ttf: Noto Sans Old Persian:style=Regular`
- `/System/Library/Fonts/Supplemental/NotoSerifBalinese-Regular.ttf: Noto Serif Balinese:style=Regular`
- `/System/Library/Fonts/Supplemental/NotoSansMeeteiMayek-Regular.ttf: Noto Sans Meetei Mayek:style=Regular`
- `/System/Library/Fonts/NotoSansArmenian.ttc: Noto Sans Armenian,Noto Sans Armenian ExtBd:style=ExtraBold,Regular`
- `/System/Library/Fonts/Supplemental/NotoSansTakri-Regular.ttf: Noto Sans Takri:style=Regular`
- `/System/Library/Fonts/Supplemental/NotoSansSiddham-Regular.otf: Noto Sans Siddham:style=Regular`
- `/System/Library/Fonts/Supplemental/NotoSansMultani-Regular.ttf: Noto Sans Multani:style=Regular`
- `/System/Library/Fonts/STHeiti Medium.ttc: Heiti SC,黑體\-簡,黒体\-簡,Heiti\-간체,黑体\-简:style=Medium,中黑,Halbfett,Normaali,Moyen,Medio,ミディアム,중간체,Médio,Средний,Normal,中等,Media`
- `/System/Library/Fonts/NotoSansMyanmar.ttc: Noto Sans Zawgyi,Noto Sans Zawgyi Thin:style=Thin,Regular`
- `/System/Library/Fonts/Supplemental/NotoSansLimbu-Regular.ttf: Noto Sans Limbu:style=Regular`
- `/System/Library/Fonts/Supplemental/NotoSansLinearA-Regular.ttf: Noto Sans Linear A:style=Regular`
- `/System/Library/Fonts/Supplemental/NotoSansMongolian-Regular.ttf: Noto Sans Mongolian:style=Regular`

## 采用路线

- 当前环境未发现 Pandoc/XeLaTeX、wkhtmltopdf、weasyprint 或 mmdc。
- 实际采用：Markdown → HTML → Chrome headless print-to-pdf。
- 中文字体处理：脚本通过 `@font-face` 强制加载 `/System/Library/Fonts/STHeiti Light.ttc`、`/System/Library/Fonts/STHeiti Medium.ttc` 和 `/System/Library/Fonts/Supplemental/Songti.ttc`，已修复 Chrome headless 默认字体导致的中文正文缺失问题。
- Mermaid 处理：浏览器端加载 `https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js` 渲染，Chrome 使用 `--virtual-time-budget` 等待渲染。
