# Anki 合作制卡——如何让牌组与表格之间互相转换？

> [原文链接](https://zhuanlan.zhihu.com/p/58299293)

阅读须知：本文章为《[Anki 学习小组指导手册v0.0.1](https://zhuanlan.zhihu.com/p/57628357)》的具体细节补充

需要的软件：Anki(电脑端)，Excel(或者其他表格应用)

首先，先讲如何让牌组变成表格(方便统一修改、全面检查和共同编辑)：

Step 1：

![](https://pica.zhimg.com/v2-d7436b727daf30f546da720751b65710_1440w.jpg)
打开 Anki ，点击想要导出的牌组的右侧齿轮按钮，在弹出的菜单中点击导出

Step 2：

![](https://pic1.zhimg.com/v2-b4442ebcd2ee81ce7e5ba21860029baa_1440w.jpg)
在导出界面，将导出格式改为纯文本格式的笔记，然后点击导出，得到一个 txt 文本文件

Step 3：

![](https://pic2.zhimg.com/v2-e762e474b0ede5364ff781a66f301ddd_1440w.jpg)
打开 txt 文件，Ctrl + A 全选文本，Ctrl + C 复制选中的文本

Step 4：

![](https://pica.zhimg.com/v2-3523a594aee95a58a7c3576a9bb9b152_1440w.jpg)
打开 Excel，选中左上角第一个表格，Ctrl + V 粘贴，然后调整列举，即可得到上图的效果

注：这里的 Excel 可以换成任何表格应用，使用在线表格也是一样的操作，复制进去就好了

OK，现在讲一下如何把表格内容变成 Anki 牌组：

样例：[《生物目录+样例》(石墨文档)](https://link.zhihu.com/?target=https%3A//shimo.im/sheet/lPI5O23Gei0gxydH/%2520%25E3%2580%258A%25E7%2594%259F%25E7%2589%25A9%25E7%259B%25AE%25E5%25BD%2595%2B%25E6%25A0%25B7%25E4%25BE%258B%25E3%2580%258B%25EF%25BC%258C%25E5%258F%25AF%25E5%25A4%258D%25E5%2588%25B6%25E9%2593%25BE%25E6%258E%25A5%25E5%2590%258E%25E7%2594%25A8%25E7%259F%25B3%25E5%25A2%25A8%25E6%2596%2587%25E6%25A1%25A3%2520App%2520%25E6%2588%2596%25E5%25B0%258F%25E7%25A8%258B%25E5%25BA%258F%25E6%2589%2593%25E5%25BC%2580)

Step 1：

![](https://pic1.zhimg.com/v2-7c9f119966fbc3a01c5fe1b578d51b76_1440w.jpg)
打开上面的网址，可以看到一个在线表格，选中图中的那个区域，然后复制即可

注：快速选中区域的方式：先选中 D4，然后按住 Shift 键，再按方向键 →，保持按住 Shift，并按住 Ctrl，最后按方向键 ↓，即可选中

Step 2：

![](https://pica.zhimg.com/v2-6c808288cd05b3ecc6a6f059a4a68d6a_1440w.jpg)
现在复制选中的部分，复制到一个新建的文本文档里

Step 3：

![](https://pic1.zhimg.com/v2-923fe3e2608c42cba354f9f321676320_1440w.jpg)
重点来了，将文本文件另存为 UTF-8 编码格式，保存到方便找到的地方

Step 4：

![](https://pic3.zhimg.com/v2-e2f7dcfe02be09b82e281362e1d8a97a_1440w.jpg)
好，回到 Anki ，点击导入文件，然后将导入的文件改为 按制表符或者分号分隔的文本

再点击要导入的 txt 文本文件

Step 5：

![](https://pic1.zhimg.com/v2-59c201edd8c1d47f7536b5c75408c53e_1440w.jpg)
最后一步了，这里先选择导入的笔记类型、导入的牌组

然后是每个字段(即第一列、第二列...)对应笔记类型的字段

最后点导入就可以了

注：别忘了把 允许在字段中使用HTML 勾选上，不然有可能会遇到卡片中有乱码

相关阅读：[4.1 电子材料批量制卡 · Anki 备战高考手册 · 看云](https://link.zhihu.com/?target=https%3A//www.kancloud.cn/ankigaokao/ankigaokao/784672) 

之后会介绍一个很方便的导出卡片的 Anki 插件，继续完善 Anki 小组制卡的流程细节。
