# Review Feedback Workflow

## Continuous Forgetting

连续遗忘的卡先改写 Front 或拆分 Back；不要只是硬背。给卡加 `ruankao::feedback::too_hard`。

## Wrong Questions

做错真题后，判断是概念不清、题干信号没识别、错项陷阱、还是计算失误；必要时新增辨析卡或关键词识别卡。

## Low Quality Cards

模糊正面加 `ruankao::feedback::ambiguous_front`；背面太长加 `ruankao::feedback::too_long_back`；答案疑似错误加 `ruankao::feedback::wrong_answer`。

## OCR Errors

发现 OCR 错题，回写到待核验列表，给卡加 `ruankao::feedback::wrong_answer` 和 `ruankao::needs_review`，下一轮增量更新时用 checksum 更新而不是重复导入。

## Weak Topic Loop

错题归因到 SourceTopicID，统计薄弱专题，再回专题学习包补理解和补卡。
