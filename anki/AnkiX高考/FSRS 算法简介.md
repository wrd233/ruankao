# FSRS 算法简介

> [原文链接](https://zhuanlan.zhihu.com/p/672908338)

FSRS 是由 Jarrett Ye 开发的一种现代[间隔重复](https://link.zhihu.com/?target=https%3A//en.wikipedia.org/wiki/Spaced_repetition)算法。它旨在学习用户的记忆习惯。相比 Anki 原有的 SM2 算法，FSRS 能更高效地安排复习计划。

间隔重复算法的核心目标，是计算出复习间隔的最佳时长。但究竟什么样的间隔才算「最佳」？在 FSRS 中，如果某个间隔能实现成功回忆一张卡片的特定概率，那么这个间隔就是最佳的。比如说，如果你想在下次看到某张卡片时，有 90% 的把握能成功回忆，那么最佳间隔就是回忆成功的概率为 90% 所需的时间。

FSRS 基于「记忆的三变量模型」。这个模型认为，只需三个变量就足以描述人脑中单一记忆的状态。这三个变量包括：

可提取性（R）：指某人在某一时刻成功回忆特定信息的可能性。它受到自上次复习以来经过的时间和记忆稳定性（S）的影响。
稳定性（S）：指 R 从 100% 下降到 90% 所需的天数。举例来说，S = 365 表示需要过去整整一年，回忆特定卡片的概率才会降到 90%。
难度（D）：特定信息本身的复杂程度。它反映了在复习后提升记忆稳定性的难易程度。

在 FSRS 中，这三个变量共同构成了所谓的「记忆状态」。用户每次复习一张卡片，与这张卡片相关的记忆状态便会相应改变，但也有例外，比如发生在同一天内的后续复习不会引起变化。对于每张卡片，FSRS 每天只考虑一次复习，也就是最早的那次。每张卡片都有其独特的 DSR 值，也就是说，每张卡片都有自己的记忆状态。

为了精确计算 DSR 值，FSRS 会分析用户的复习记录，并利用机器学习算法计算出拟合复习记录的参数。最新版的 FSRS 在计算 D 和 S 的公式中用到了 17 个参数（而计算可提取性的公式则不需要任何参数）。如果你对细节感兴趣，可以查阅以下页面：[《算法》](https://link.zhihu.com/?target=https%3A//github.com/open-spaced-repetition/fsrs4anki/wiki/The-Algorithm)和[《优化机制》](https://link.zhihu.com/?target=https%3A//github.com/open-spaced-repetition/fsrs4anki/wiki/The-mechanism-of-optimization)。如果用户的复习记录不足，系统会默认使用预设的参数。这些参数是在数亿条复习数据（来自约两万名用户的）上运行 FSRS 优化器得出的。即使是用预设参数，FSRS 的效果也优于 Anki 默认的算法。

请注意，用户不应自行调整这些参数。如果你想调整复习计划，只需要选择一个合适的期望保留率。一般来说，70% 到 97% 的保留率是合理的。也就是说，用 FSRS 的用户可以设定一个特定的保留率，以在他们记忆保留率和复习压力之间权衡。更高的保留率意味着每天花在复习上对时间更多。

除了让用户自主选择他们期望达到的记忆保留率外，FSRS 相较于 Anki 的默认算法还有其他几个优点。使用 FSRS 时，在保持同样的记忆水平的条件下，用户所需的复习次数比 Anki 默认算法少 20% 到 30%。如果用户有段时间没使用 Anki，FSRS 在安排这些延后复习的卡片上也更加高效。此外，[FSRS4Anki 助手插件](https://link.zhihu.com/?target=https%3A//github.com/open-spaced-repetition/fsrs4anki-helper)还提供了一些原本无法实现的便捷功能。

如果你使用的是 23.10 版本或更高版本的 Anki，请参考[这个指南](https://link.zhihu.com/?target=https%3A//github.com/open-spaced-repetition/fsrs4anki/blob/main/docs/tutorial.md)[1]。如果你的 Anki 版本低于 23.10，你可以使用 FSRS 的独立版本，安装方法请参考[这个指南](https://link.zhihu.com/?target=https%3A//github.com/open-spaced-repetition/fsrs4anki%23how-to-get-started)[2]。

想了解 FSRS 与其他算法的比较效果，可以阅读以下页面：[基准测试](https://link.zhihu.com/?target=https%3A//github.com/open-spaced-repetition/fsrs-benchmark)，以及 [FSRS 与 SuperMemo 最新算法之一 SM-17 的对比](https://link.zhihu.com/?target=https%3A//github.com/open-spaced-repetition/fsrs-vs-sm17)。

更多有关 FSRS 的问题，可查阅[常见问题](https://link.zhihu.com/?target=https%3A//github.com/open-spaced-repetition/fsrs4anki/wiki/FAQ)。

如果你想更深入了解间隔重复算法，可以阅读[《间隔重复记忆算法：e 天内，从入门到入土》](https://link.zhihu.com/?target=https%3A//github.com/open-spaced-repetition/fsrs4anki/wiki/Spaced-Repetition-Algorithm%3A-A-Three%25E2%2580%2590Day-Journey-from-Novice-to-Expert)[3]。

> 原文：[ABC of FSRS · open-spaced-repetition/fsrs4anki Wiki (github.com)](https://link.zhihu.com/?target=https%3A//github.com/open-spaced-repetition/fsrs4anki/wiki/ABC-of-FSRS)
> 作者：[Expertium](https://link.zhihu.com/?target=https%3A//github.com/Expertium), [user1823](https://link.zhihu.com/?target=https%3A//github.com/user1823) and [L-M-Sherlock](https://link.zhihu.com/?target=https%3A//github.com/L-M-Sherlock)
> 译者：GPT-4
> 校对：Jarrett Ye
