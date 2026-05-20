# 专题学习包 PDF 导出目录

- PDF 生成数量：38/38
- `topics/`：正式专题 PDF，目录结构镜像 `topic_learning_packages/topics/`。
- `index/`：导航、manifest、覆盖矩阵等 PDF。
- `reports/`：环境探测与导出报告。

如需重新导出：

```bash
python scripts/export_topic_packages_to_pdf.py --source topic_learning_packages --output topic_learning_packages_pdf --include-topics --include-index
```
