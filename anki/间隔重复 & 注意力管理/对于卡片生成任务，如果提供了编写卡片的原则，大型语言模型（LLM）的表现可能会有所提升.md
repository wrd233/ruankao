# 对于卡片生成任务，如果提供了编写卡片的原则，大型语言模型（LLM）的表现可能会有所提升

> [原文链接](https://zhuanlan.zhihu.com/p/644435843)

[间隔重复记忆系统](https://link.zhihu.com/?target=https%3A//notes.andymatuschak.org/z4eXdSMJFv2qVGXSUEKH4vdcHBrLHcFY1ZGfC)[1]社区已经发现了许多[高质量间隔重复记忆卡片的重要属性](https://link.zhihu.com/?target=https%3A//notes.andymatuschak.org/z42J1vxsMjhkdbrqVfoqjiEesSzfaEqurBtoJ)[2]。当我将这些属性提供给 GPT-4 时，它似乎在生成间隔重复卡片方面做得更好。与这些提示相关的思维链式提示词也可能有所帮助（例如「解释这些卡片是如何满足每个原则的......」）。

目前还不清楚这些效果的强度或可靠性如何。在我的非正式实验中，有时这些因素似乎很重要，有时则没什么影响。如果有[一份由专家编写的卡片的数据集](https://link.zhihu.com/?target=https%3A//notes.andymatuschak.org/z6ZUDZaQrh43M64sHsZL48QZVKcFKQsTi4kTY)进行评估，那将对卡片生成系统的发展大有裨益。

参见示例 [20230614114329](https://link.zhihu.com/?target=https%3A//notes.andymatuschak.org/z5yuB8kkYToFBYYpoYQkehPEKWKb66JWw4X1d)。

### 参考文献

最初是在 Twitter 上有人向我提出这个建议（抱歉，我找不到那条信息了！），然后在 2023 年 5 月，[Yuval Milo](https://link.zhihu.com/?target=https%3A//notes.andymatuschak.org/zJ55L18u5sagXqnMWh5szwfZ388oGQbyfW3) 通过一个具体的提示词再次提醒了我。

## 链接至本文（已汉化）

[对于卡片生成任务，大型语言模型（LLM）缺乏为复杂概念材料编写卡片的模式](https://zhuanlan.zhihu.com/p/656355546)
[GPT-4 在指导下，通常能够从解释性文本中为陈述性知识生成可用的间隔重复卡片](https://zhuanlan.zhihu.com/p/656760808)
[叶峻峣：使用机器学习从解释性文本中生成优质的间隔重复卡片](https://zhuanlan.zhihu.com/p/716570823)

## 声明

此内容发布由 Andy Matuschak 许可。未经允许，不得转载或修改。保留所有权利。

> [Thoughts Memo](https://link.zhihu.com/?target=http%3A//paratranz.cn/projects/3131) 汉化组译制
> 感谢主要译者 GPT-4、校对 JarrettYe
> 原文：[In prompt generation, LLMs may perform better when given prompt-writing principles (andymatuschak.org)](https://link.zhihu.com/?target=https%3A//notes.andymatuschak.org/zrqgkr9n3eCMNsAPDsRozt3HLd8nRT5nVASc)
