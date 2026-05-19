# 次世代间隔重复算法 FSRS4Anki v3.7.0-v3.23.0 主要更新记录

> [原文链接](https://zhuanlan.zhihu.com/p/636114722)

好久不见，伙计们。我已经半年没有分享我在 FSRS4Anki 上的进展了。最近 FSRS4Anki 经历了重大更新，借此机会我也想宣传一下 FSRS4Anki 这半年来的主要更新。感谢开源社区中所有无私的贡献者，从 v3.7.0 到 v3.23.0，我们一共发布了 17 个 feature，以及几打的修复补丁，在本文中我只介绍最重要的更新。

PS: 不了解 FSRS4Anki 的朋友，可以看这篇教程：

[叶峻峣：如何在 Anki 上使用次世代间隔重复算法 FSRS？](https://zhuanlan.zhihu.com/p/591833332)## Optimizer

优化了数据预处理和训练过程的代码，性能提高了 10 倍。在我自己的 22 万条复习记录的数据集上，使用免费版 Google Colab 的 CPU 机器，只需要 5 分钟就能完成全部优化。
增加了更多的评估模块，可以更方便地检测 FSRS 的潜在缺陷。
增加了和 SM-2 算法的对比模块，在我自己的数据集上，FSRS 的误差只有 SM-2 的 20%。
更严格的参数范围约束，减轻 ease hell 和长期间隔过长的问题。
在寻找最佳保留率算法中，考虑了实际的复习时间，使结果更符合实际。
## Scheduler

解耦了牌组参数和调度算法，现在为每个牌组设置独立的参数更方便了。
允许用户在特定牌组中关闭 FSRS，使用默认算法
允许用户开启 DSR 记忆状态日志，可以在复习时查看当前卡片的记忆状态。
## Helper

重构了 Postpone 和 Advance 功能，现在用户可以输入想要推迟或提前的卡片数量，Helper 将自动计算每张卡片的相对推迟/提前程度，优先推迟或提前偏离最佳保留率最小的卡片。
增加了分散兄弟姐妹功能，可以让关联卡片的复习日期尽可能错开，避免相互干扰或提醒。
增加了卡片浏览器支持，现在可以在卡片浏览器中查看每张卡片的记忆状态，也可以通过特定语法搜索这些卡片 （但由于Anki框架原因，无法在筛选牌组搜索中使用）
增加了自动重新规划功能，可以在同步后自动重新规划那些在其他设备复习的卡片。这对 AnkiDroid 用户很重要。
优化了性能，重新规划功能速度快了 7 倍。
增加了 FSRS 统计面板，可以查看自己的 retention、stability 的统计信息。
增加了 Free days 功能，可以显著减少在特定日期的复习数量
增加了 Load Balance 功能，可以让每日复习量更加一致。
## 下一步的工作

最近我和社区的贡献者正在改进 FSRS 的记忆模型，让 FSRS 更具通用性。如果记忆模型更新，我们将发布 v4.0.0 版本（顺带一提，FSRS4Anki 中的 4 不是版本，而是 for 的谐音。我同时也在开发 fsrs4remnote，以及帮助维护 FSRS 各编程语言实现的算法库）。

重写教程/帮助文档，让用户更轻松上手 FSRS。

牌组/卡片优先级等概念正在起草中。这将帮助我们更高效地安排复习。

敬请期待。

## 支持我的工作

如果我的工作帮助到了你的学习，希望可以给我的开源项目 star，以及给我的 add-on 点赞。

[open-spaced-repetition/fsrs4anki: A modern Anki custom scheduling based on free spaced repetition scheduler algorithm (github.com)](https://link.zhihu.com/?target=https%3A//github.com/open-spaced-repetition/fsrs4anki)[FSRS4Anki Helper - AnkiWeb](https://link.zhihu.com/?target=https%3A//ankiweb.net/shared/info/759844606)## 一些预览图

![](https://pic3.zhimg.com/v2-70f4331c6ca66132e4c2890168608b76_1440w.jpg)

![](https://picx.zhimg.com/v2-6550549da7fc9187dbff664988322d39_1440w.jpg)

![](https://pica.zhimg.com/v2-f00a0cfffd8c8adcf0e2f7f5e755f8a2_1440w.jpg)

![](https://pic3.zhimg.com/v2-9de039ce05c7d572581548d2afba9d84_1440w.jpg)

![](https://pica.zhimg.com/v2-5165f1badbd62ea28e6be6aa39bef464_1440w.jpg)
