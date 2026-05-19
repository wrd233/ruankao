# 在Anki2.1中实验性卡片调度系统(记忆算法)的改变

> [原文链接](https://zhuanlan.zhihu.com/p/46530394)

> 已收录于[「一周年」专栏整理](https://zhuanlan.zhihu.com/p/57637220)
Experiment scheduling changes in Anki 2.1

在Anki2.1中实验性卡片调度系统(记忆算法)的改变

Filtered decks:

筛选牌组

Filtered decks no longer reset (re)learning cards when they are built or emptied, and reviews and learning cards will show up in the correct queue instead of the new queue.

筛选牌组在构建或清空时不再重置学习卡(重新学习卡)，复习和学习卡将显示在正确的队列中，而不是新队列中。

Filtered decks support a second search term, so you can include 100 cards to review and 20 new cards for example.

筛选牌组支持第二个搜索词，所以你可以筛选100张卡片复习，还有20张新卡片。

Scheduling of cards that aren&#39;t yet due has been improved, and will show 4 buttons instead of 3.

未到期的卡片的调度已经改进，将显示4个按钮而不是3个。

Filtered decks no longer support custom steps, and there is now a simple &#34;preview mode&#34; instead of the old option to disable scheduling changes. The new card order does not get forgotten when previewing.

筛选不再支持自定义步骤，现在有了一个简单的“预览模式”，取代了旧的选项，以禁用调度更改。新卡片顺序在预览时不会忘记。

Cards can be buried or suspended while remaining in the filtered deck.

卡片可以被搁置或暂停，而保留在筛选牌组。

Other scheduling changes:

其他安排的变化:

When a deck has children, reviews are taken from all children decks at once, instead of showing each deck&#39;s review cards one by one.

当一个牌组有子排序牌组时，所有子牌组上的复习卡片将被一次取出，而不是一个一个地显示每个子牌组的卡片。

Learning cards have 4 buttons instead of 3 - Hard repeats the current step.

学习卡有4个按钮，而不是3个按钮——选择「困难」按钮将重复当前的步骤。

&#34;Next day starts at&#34; is now relative to the current timezone.

“Next day start at”现在是相对于当前时区而言的。

Lapsed reviews have their review interval updated on the last relearning step, instead of the first step.

失误的复习卡片在最后一个重新学习的步骤上更新它们的复习间隔，而不是第一个步骤。

Anki now distinguishes between manually and automatically buried cards, and you can unbury one set without the other.

Anki现在可以区分手工搁置和自动搁置，你可以保持其中一组搁置的同时解除另一组搁置。

Option in the preferences screen to show day learning cards before reviews.

在设置界面新增“在复习卡片前展示学习卡片”选项

The learn count is now the number of cards instead of the number of steps required to complete.

学习计数现在是卡片的数量而不是需要完成的步骤的数量。

目前只有桌面端和iOS端提供新的卡片调度系统(记忆算法)
