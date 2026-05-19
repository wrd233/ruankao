# GPT-4 在指导下，通常能够从解释性文本中为陈述性知识生成可用的间隔重复卡片

> [原文链接](https://zhuanlan.zhihu.com/p/656760808)

通过结合以下的洞见，我在[使用机器学习从解释性文本中生成优质的间隔重复卡片](https://link.zhihu.com/?target=https%3A//notes.andymatuschak.org/z2DY7qsP5iHsiA5hxUHheV8hu7Xe96vdGyYX)[1]中用 [GPT-4](https://link.zhihu.com/?target=https%3A//notes.andymatuschak.org/z3Bab7JXEhospmJZJQnduTFFjrZHaHKMCJBQE) 取得了成功，通常都能一次搞定：

[对于卡片生成任务，选择要强化的目标概念，和为这些目标概念编写卡片，是两个独立的问题](https://link.zhihu.com/?target=https%3A//notes.andymatuschak.org/z62s1nNLEfhGbDmpb8Z7dZiYyi3kaSziuLVXd)[2]。在这些例子里，我负责选择制卡对象（例如，通过指向更大篇幅中的短语），模型的任务是根据这些给定的目标，生成有用的卡片。
 

[对于卡片生成任务，如果提供了编写卡片的原则，大型语言模型（LLM）的表现可能会有所提升](https://link.zhihu.com/?target=https%3A//notes.andymatuschak.org/zrqgkr9n3eCMNsAPDsRozt3HLd8nRT5nVASc)[3]；我提供了这些原则。
 

[对于卡片生成任务，大型语言模型（LLM）经常需要额外的提示，来确定从何种角度制卡](https://link.zhihu.com/?target=https%3A//notes.andymatuschak.org/zomoPzCNzSi5GqtfTeVWgm7RjmiArjS8vvM5)[4]；我提供了这些提示。
 

[对于卡片生成任务，如果提供了充足的上下文，大型语言模型（LLM）可能会表现得更好](https://link.zhihu.com/?target=https%3A//notes.andymatuschak.org/z5LQFLXHFLrb4nYAtLrB3JBzNyJng8fYHVJYN)[5]；我提供了上下文。
 

这对于简单的描写来说，效果相当好，但对于更概念化的材料来说就不行了：[对于卡片生成任务，大型语言模型（LLM）缺乏为复杂概念材料编写卡片的模式](https://link.zhihu.com/?target=https%3A//notes.andymatuschak.org/zmrbnm683nVZi9ut63vsr8BwYKEtATA6e4B3)[6]

一个提示词示例：[20230614123022](https://link.zhihu.com/?target=https%3A//notes.andymatuschak.org/z4jtgUPVP5pABoDEjvz22hzYzAuRELqGg4BR6)

## 链接至本文（已汉化）

[对于卡片生成任务，大型语言模型（LLM）缺乏为复杂概念材料编写卡片的模式](https://zhuanlan.zhihu.com/p/656355546)
[使用机器学习从解释性文本中生成优质的间隔重复卡片](https://zhuanlan.zhihu.com/p/716570823)

## 声明

此内容发布由 Andy Matuschak 许可。未经允许，不得转载或修改。保留所有权利。

> [Thoughts Memo](https://link.zhihu.com/?target=http%3A//paratranz.cn/projects/3131) 汉化组译制
> 感谢主要译者 Jarrett Ye，校对偶然奇怪~ ☆
> 原文：[GPT-4 can often generate usable spaced repetition prompts for declarative knowledge from explanatory text with guidance (andymatuschak.org)](https://link.zhihu.com/?target=https%3A//notes.andymatuschak.org/z2VVmj24FLixtrijdAbkKty91JQruAaZGbHE6)
