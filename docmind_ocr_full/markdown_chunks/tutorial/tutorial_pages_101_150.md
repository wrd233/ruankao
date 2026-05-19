息，并且辅助决策，就是商业智能要解决的主要问题。  

![5dc0086cf511b4002ec5a4c49b50ceb6.jpeg](http://docmind-api-cn-hangzhou.oss-cn-hangzhou.aliyuncs.com/1617315274244978/publicDocStreamStructure/docmind-20260519-672fb26ef598441da7a1ea2e8ee2ae02/0.png?Expires=1779206878&OSSAccessKeyId=STS.NZebDGdcxohmUjCQd3QTqZtgp&Signature=HLzB3aPTv%2FSDp5Pe753ztQU1kJ8%3D&x-oss-process=image%2Fcrop%2Cx_146%2Cy_321%2Cw_1015%2Ch_1287&security-token=CAIS1wJ1q6Ft5B2yfSjIr5nQKf7zibxZ2KqGV0zytWRmXdtdtbHMkjz2IHhMeHVhCe4Ytfs1nmxX7voZlrp6SJtIXleCZtF94oxN9h2gb4fb4xRsN1SI08%2FLI3OaLjKm9u2wCryLYbGwU%2FOpbE%2B%2B5U0X6LDmdDKkckW4OJmS8%2FBOZcgWWQ%2FKBlgvRq0hRG1YpdQdKGHaONu0LxfumRCwNkdzvRdmgm4NgsbWgO%2Fks0CP0AahlLBL996veMb%2FNfMBZskvD42Hu8VtbbfE3SJq7BxHybx7lqQs%2B02c5onBXwgBvUvdbLCOroI3cFRjFKk2A%2BtIq%2FP5lPt0%2F%2FTajZ%2F6jkwVZ7wQSz7YVABLAzk41i3D3L8ZAlWbUxylurjnXhJFq5mGrt21HrfraghQy27xNG29hwvQXkuNkr7knEkN5aYL3t8Y37R7YXuKmfjOEzylJ9M9udm4napgBytAGoABil%2Fqf5MVplUu7%2BU4BxuSUkUaa02SKOYDC8avK6WNdtkYn0D%2BXqfl9bU8xbeXPrci2hscIAZ0%2BX8aXvgTYjydQRSQKMCg%2FHjlv%2B9b3hANppoB06dPBtIIG3M0IRS%2Bxt1mARqgcjJ60wjWc0nO7Tsoa4sADgcsEbmCjhLeq0uUesIgAA%3D%3D)  

>图1-20作为一种解决方案的商业智能  

80  

商业智能的实现有三个层次：数据报表、多维数据分析和数据挖掘。  

# 1)数据报表  

如何把数据库中存在的数据转变为业务人员需要的信息?大部分的答案是报表系统。简单地说，报表系统是BI的低端实现。传统的报表系统技术上已经相当成熟，大家熟悉的Excel、水晶报表和Reporting Service 等都已经被广泛使用。但是，随着数据的增多，需求的提高，传统报表系统面临的挑战也越来越多。  

(1)数据太多，信息太少。密密麻麻的表格堆砌了大量数据，到底有多少业务人员仔细看过每一个数据?到底这些数据代表了什么信息、什么趋势?级别越高的领导，越需要简明的信息。  

(2)难以交互分析、了解各种组合。定制好的报表过于死板。例如，我们可以在一张表中列出不同地区、不同产品的销量，另一张表中列出不同地区、不同年龄段顾客的销量。但是，这两张表无法回答诸如"华北地区中青年顾客购买数码相机类型产品的情况"等问题。业务问题经常需要多个角度的交互分析。  

(3)难以挖掘出潜在的规则。报表系统列出的往往是表面上的数据信息，但是海量数据深处含有哪些潜在规则呢?什么客户对我们价值最大?产品之间相互关联的程度如何?越是深层的规则，对于决策支持的价值越大，但是，也越难挖掘出来。  

(4)难以追溯历史，形成数据孤岛。长期运行中产生的数据往往存在于不同地方，太旧的数据(例如一年前的数据)可能已被业务系统备份出去，导致宏观分析、长期历史分析难度很大。  

显然，随着时代的发展，传统报表系统已经不能满足日益增长的业务需求了，企业期待着新的技术。数据分析和数据挖掘的时代正在来临。值得注意的是，数据分析和数据挖掘系统的目的是带给我们更多的决策支持价值，并不是取代数据报表。报表系统依然有其不可取代的优势，并且将会长期与数据分析、挖掘系统一起并存下去。  

## 2)多维数据分析  

如果说在线事务处理(OLTP) 侧重于对数据库进行增加、修改和删除等日常事务操作，在线分析处理则侧重于针对宏观问题全面分析数据，获得有价值的信息。  

为了达到OLAP的目的，传统的关系型数据库已经不够了，需要一种新的技术叫做多维数据库。  

多维数据库的概念并不复杂。举一个例子，我们想描述2003年4月份可乐在北部地区销售额10万元时，涉及到几个角度：时间、产品和地区。这些叫做维度。至于销售额，叫做度量值。当然，还有成本、利润等。  

除了时间、产品和地区，我们还可以有很多维度，例如客户的性别、职业、销售部门和促销方式等。实际上，使用中的多维数据库可能是一个8维或者15维的立方体。虽然结构上15维的立方体很复杂，但是概念上非常简单。  

数据分析系统的总体架构分为4个部分：源系统、数据仓库、多维数据库和客户端。  

①源系统：包括现有的所有OLTP系统， 搭建BI系统并不需要更改现有系统。  

②数据仓库：数据大集中，通过数据抽取，把数据从源系统源源不断地抽取出来，可能每天一次，或者每3个小时一次，当然是自动的。数据仓库依然建立在关系型数据库上，往往符合"星型结构"模型。  

③多维数据库：数据仓库的数据经过多维建模，形成了立方体结构。每一个立方体描述了一个业务主题，例如销售、库存或者财务。  

④客户端：好的客户端软件可以把多维立方体中的信息丰富多彩地展现给用户。  

### 3)数据挖掘  

广义上说，任何从数据库中挖掘信息的过程都叫做数据挖掘。从这点看来，数据挖掘就是BI。但从技术术语上说，数据挖掘(Data Mining) 指的是：源数据经过清洗和转换等成为适合于挖掘的数据集。数据挖掘在这种具有固定形式的数据集上完成知识的提炼，最后以合适的知识模式用于进一步分析决策工作。从这种狭义的观点上，我们可以定义：数据挖掘是从特定形式的数据集中提炼知识的过程。数据挖掘往往针对特定的数据、特定的问题，选择一种或者多种挖掘算法，找到数据下面隐藏的规律，这些规律往往被用来预测、支持决策。  

现举一个关联销售的案例。美国的超市有这样的系统：当你采购了一车商品结账时，售货员小姐扫描完了你的产品后，计算机上会显示出一些信息，然后售货员会友好地问你：我们有一种一次性纸杯正在促销，位于F6.货架上，您要购买吗?这句话绝不是一般的促销。因为计算机系统早就算好了，如果你的购物车中有餐巾纸、大瓶可乐和沙拉，则86%的可能性你要买一次性纸杯。结果是你说："啊，谢谢你，我刚才一直没找到纸杯。"  

这不是什么神奇的科学算命，而是利用数据挖掘中的关联规则算法实现的系统。  

每天，新的销售数据会进入挖掘模型，与过去N天的历史数据一起被挖掘模型处理，得到当前最有价值的关联规则。同样的算法，分析网上书店的销售业绩，计算机可以发现产品之间的关联以及关联的强弱。  

# 4.商业智能的软件工具集合  

## 1)终端用户查询和报告工具  

专门用来支持初级用户的原始数据访问，不包括适应于专业人士的成品报告生成工具。  

## 2)数据仓库.(Data Warehouse)和数据集市(Data Mart)产品  

包括数据转换、管理和存取等方面的预配置软件，通常还包括一些业务模型，如财务分析模型。  

## 3)数据挖掘(Data Mining) 软件  

使用诸如神经网络、规则归纳等技术，用来发现数据之间的关系，做出基于数据的推断。  

82  

![f7463ffb9b76c4746267fd4d9fae2bc1.jpeg](http://docmind-api-cn-hangzhou.oss-cn-hangzhou.aliyuncs.com/1617315274244978/publicDocStreamStructure/docmind-20260519-672fb26ef598441da7a1ea2e8ee2ae02/3.png?Expires=1779206878&OSSAccessKeyId=STS.NZebDGdcxohmUjCQd3QTqZtgp&Signature=3o0qpEpKdvDufqmKdV5tqcobcNU%3D&x-oss-process=image%2Fcrop%2Cx_0%2Cy_5%2Cw_1216%2Ch_103&security-token=CAIS1wJ1q6Ft5B2yfSjIr5nQKf7zibxZ2KqGV0zytWRmXdtdtbHMkjz2IHhMeHVhCe4Ytfs1nmxX7voZlrp6SJtIXleCZtF94oxN9h2gb4fb4xRsN1SI08%2FLI3OaLjKm9u2wCryLYbGwU%2FOpbE%2B%2B5U0X6LDmdDKkckW4OJmS8%2FBOZcgWWQ%2FKBlgvRq0hRG1YpdQdKGHaONu0LxfumRCwNkdzvRdmgm4NgsbWgO%2Fks0CP0AahlLBL996veMb%2FNfMBZskvD42Hu8VtbbfE3SJq7BxHybx7lqQs%2B02c5onBXwgBvUvdbLCOroI3cFRjFKk2A%2BtIq%2FP5lPt0%2F%2FTajZ%2F6jkwVZ7wQSz7YVABLAzk41i3D3L8ZAlWbUxylurjnXhJFq5mGrt21HrfraghQy27xNG29hwvQXkuNkr7knEkN5aYL3t8Y37R7YXuKmfjOEzylJ9M9udm4napgBytAGoABil%2Fqf5MVplUu7%2BU4BxuSUkUaa02SKOYDC8avK6WNdtkYn0D%2BXqfl9bU8xbeXPrci2hscIAZ0%2BX8aXvgTYjydQRSQKMCg%2FHjlv%2B9b3hANppoB06dPBtIIG3M0IRS%2Bxt1mARqgcjJ60wjWc0nO7Tsoa4sADgcsEbmCjhLeq0uUesIgAA%3D%3D)  

## 4)OLAP工具  

### (1) OLAP的概念  

OLAP的概念最早是由关系数据库之父E.F.Codd于1993年提出的，他同时提出了关于OLAP的12条准则。OLAP的提出引起了很大的反响， OLAP作为一类产品同OLTP明显区分开来：OLTP属于传统的关系型数据库的一个主要应用，主要用于基本的、日常的事务处理，例如银行交易； OLAP是数据仓库系统的一个主要应用，支持复杂的分析操作，侧重决策支持，并且提供直观易懂的查询结果。OLAP提供多维数据管理环境，其典型的应用是对商业问题的建模与商业数据分析。OLAP也被称为多维分析。  

### (2)"维"的概念  

OLAP的目标是满足决策支持或者满足在多维环境下特定的查询和报表需求，它的技术核心是"维"这个概念。  

OLAP工具是针对特定问题的联机数据访问与分析。它通过多维的方式对数据进行分析、查询和报表。"维"是人们观察数据的特定角度。通过把一个实体的多项重要的属性定义为多个维(dimension)， 使用户能对不同维上的数据进行比较。例如，一个企业在考虑产品的销售情况时，通常从时间、地区和产品的不同角度来深入观察产品的销售情况。这里的时间、地区和产品就是维。而这些维的不同组合和所考察的度量指标构成的多维数组则是OLAP分析的基础，可形式化表示为(维1，维2，…，维n，度量指标)，如(地区，时间，产品， …， 销售额)。多维分析是指对以多维形式组织起来的数据采取切片(slice) 、切块(dice) 、钻取(drill-down和roll-up) 和旋转(pivot)等各种分析动作，以求剖析数据，使用户能从多个角度、多侧面地观察数据库中的数据，从而深入理解包含在数据中的信息。因此OLAP也可以说是多维数据分析工具的集合。  

OLAP的基本多维分析操作有钻取、切片和切块以及旋转、drill across和drill through等。  

钻取是改变维的层次，变换分析的粒度。它包括向上钻取和向下钻取。roll up是在某一维上将低层次的细节数据概括到高层次的汇总数据，或者减少维数；而drill down则相反，它从汇总数据深入到细节数据进行观察或增加新维。  

切片和切块是在一部分维上选定值后，关心度量数据在剩余维上的分布。如果剩余的维只有两个，则是切片；如果有三个，则是切块。  

旋转是变换维的方向，即在表格中重新安排维的放置(例如行列互换)。  

## (3) OLAP的实现方法  

OLAP有多种实现方法，根据存储数据的方式不同可以分为 ROLAP(Relational OLAP)、MOLAP (Multidimensional OLAP) 和HOLAP (Hybrid OLAP)。  

ROLAP表示基于关系数据库的OLAP实现。以关系数据库为核心，以关系型结构进行多维数据的表示和存储。ROLAP 将多维数据库的多维结构划分为两类表：一类是事实表，用来存储数据和维关键字；另一类是维表，即对每个维至少使用一个表来存放维的层次、成员类别等维的描述信息。维表和事实表通过主关键字和外关键字联系在一起，形成了"星型模式"。对于层次复杂的维，为避免冗余数据占用过大的存储空间，可以使用多个表来描述，这种星型模式的扩展称为"雪花模式"  

MOLAP表示基于多维数据组织的OLAP实现。以多维数据组织方式为核心，也就是说， MOLAP使用多维数组存储数据。多维数据在存储中将形成"立方块(Cube)"的结构， 在MOLAP中对"立方块"的"旋转"、"切块"和"切片"是产生多维数据报表的主要技术。  

HOLAP表示基于混合数据组织的OLAP实现。如低层是关系型的，高层是多维矩阵型的。这种方式具有更好的灵活性。  

还有其他的一些实现OLAP的方法，如提供一个专用的SQL Server， 对某些存储模式(如星型、雪片型) 提供对SQL查询的特殊支持，等等。  

主流的商业智能工具包括BO、COGNOS和BRIO。一些国内的软件工具平台如KCOM(http：//www.kcomsoft.com/)也集成了一些基本的商业智能工具。  

# 5.实施商业智能的步骤  

实施商业智能系统是一项复杂的系统工程，整个项目涉及企业管理、运作管理、信息系统、数据仓库、数据挖掘和统计分析等众多门类的知识，因此用户除了要选择合适的商业智能软件工具外，还必须遵循正确的实施方法才能保证项目得以成功。商业智能项目的实施步骤可分为如下6步。  

## 1)需求分析  

需求分析是商业智能实施的第一步，在其他活动开展之前必须明确地定义组织对商业智能的期望和需求， 包括需要分析的主题、查看各主题的角度(维度) 和需要发现组织的哪些方面的规律等。  

## 2)数据仓库建模  

通过对企业需求的分析，建立企业数据仓库的逻辑模型和物理模型，并规划好系统的应用架构，将企业各类数据按照分析主题进行组织和归类。  

## .3)数据抽取  

数据仓库建立后必须将数据从业务系统中抽取到数据仓库中，在抽取的过程中还必须将数据进行转换、清洗，以适应分析的需要。  

## 4)建立商业智能分析报表  

商业智能分析报表需要专业人员按照用户制订的格式进行开发，用户也可自行开发(开发方式简单，快捷)。  

## 5)用户培训和数据模拟测试  

对于开发-使用分离型的商业智能系统，最终用户的使用是相当简单的，只需要单击操作就可针对特定的商业问题进行分析。  

## 6)系统改进和完善  

任何系统的实施都必须是不断完善的，商业智能系统更是如此。在用户使用一段时间后可能会提出更多、更具体的要求，这时需要再按照上述步骤对系统进行重构或完善。  

84  

![d95ab8ecb9868617fa31add7660fad46.jpeg](http://docmind-api-cn-hangzhou.oss-cn-hangzhou.aliyuncs.com/1617315274244978/publicDocStreamStructure/docmind-20260519-672fb26ef598441da7a1ea2e8ee2ae02/5.png?Expires=1779206878&OSSAccessKeyId=STS.NZebDGdcxohmUjCQd3QTqZtgp&Signature=kheXBACP%2BDt4bD2R6Q%2BEqbWGt40%3D&x-oss-process=image%2Fcrop%2Cx_102%2Cy_1%2Cw_1128%2Ch_127&security-token=CAIS1wJ1q6Ft5B2yfSjIr5nQKf7zibxZ2KqGV0zytWRmXdtdtbHMkjz2IHhMeHVhCe4Ytfs1nmxX7voZlrp6SJtIXleCZtF94oxN9h2gb4fb4xRsN1SI08%2FLI3OaLjKm9u2wCryLYbGwU%2FOpbE%2B%2B5U0X6LDmdDKkckW4OJmS8%2FBOZcgWWQ%2FKBlgvRq0hRG1YpdQdKGHaONu0LxfumRCwNkdzvRdmgm4NgsbWgO%2Fks0CP0AahlLBL996veMb%2FNfMBZskvD42Hu8VtbbfE3SJq7BxHybx7lqQs%2B02c5onBXwgBvUvdbLCOroI3cFRjFKk2A%2BtIq%2FP5lPt0%2F%2FTajZ%2F6jkwVZ7wQSz7YVABLAzk41i3D3L8ZAlWbUxylurjnXhJFq5mGrt21HrfraghQy27xNG29hwvQXkuNkr7knEkN5aYL3t8Y37R7YXuKmfjOEzylJ9M9udm4napgBytAGoABil%2Fqf5MVplUu7%2BU4BxuSUkUaa02SKOYDC8avK6WNdtkYn0D%2BXqfl9bU8xbeXPrci2hscIAZ0%2BX8aXvgTYjydQRSQKMCg%2FHjlv%2B9b3hANppoB06dPBtIIG3M0IRS%2Bxt1mARqgcjJ60wjWc0nO7Tsoa4sADgcsEbmCjhLeq0uUesIgAA%3D%3D)  

系统集成项目管理工程师教程(第2版)  

## 1.6新一代信息技术对产业的推动  

战略性新兴产业是以重大技术突破和重大发展需求为基础，对经济社会全局和长远发展具有重大引领带动作用，知识技术密集、物质资源消耗少、成长潜力大、综合效益好的产业。加快培育和发展战略性新兴产业对推进我国现代化建设具有重要战略意义。依据《国务院关于加快培育和发展战略性新兴产业的决定》(国发[2010]32号)，新一代信息技术属于现阶段我国七个战略性新兴产业，要重点培育和发展。到2020年，新一代信息技术与节能环保、生物、高端装备制造产业等将成为国民经济的支柱产业。  

新一代信息技术产业包括：加快建设宽带、泛在、融合、安全的信息网络基础设施，推动新一代移动通信、下一代互联网核心设备和智能终端的研发及产业化，加快推进三网融合，促进物联网、云计算的研发和示范应用。着力发展集成电路、新型显示、高端软件、高端服务器等核心基础产业。提升软件服务、网络增值服务等信息服务能力，加快重要基础设施智能化改造。大力发展数字虚拟等技术，促进文化创意产业发展。  

2015年10月，中央通过了《中共中央关于制定十三五规划的建议》，这份编制"十三五"规划的指导性文件中指出信息通信行业发展的目标是"拓展网络经济空间"，具体是：实施"互联网+"行动计划，发展物联网技术和应用，发展分享经济，促进互联网和经济社会融合发展。实施国家大数据战略，推进数据资源开放共享。完善电信普遍服务机制，开展网络提速降费行动，超前布局下一代互联网。推进产业组织、商业模式、供应链、物流链创新，支持基于互联网的各类创新。  

大数据、云计算、互联网+、智慧城市等是新一代信息技术与信息资源充分利用的全新业态，是信息化发展的主要趋势，也是信息系统集成行业今后面临的主要业务范畴。  

### 1.6.1大数据  

#### 1.大数据概念  

软硬件技术的高速发展，带动各种信息系统特别是互联网应用的全面应用推广以及系统之间的相互整合、融合；同时，传感技术的普及和存储技术的网络化使得数据生产、采集、处理、传输具有泛在化特点，信息系统面临着分析处理"大数据"的任务。大数据(big data)是指无法在可承受的时间范围内用常规软件工具进行捕捉、管理和处理的数据集合，是需要采用新处理模式才能获取很多智能的、深入的、有价值的信息，以期得到更强的决策力、洞察力和流程优化能力的海量、高增长率和多样化的信息资源。针对大数据的分析处理，不能用随机分析法(抽样调查)，而要针对所有数据进行分析处理。大数据具有5V特点： Volume(大量) 、Velocity(高速) 、Variety(多样) 、Value(价值)和Veracity(真实性) 。  

大数据是以容量大、类型多、存取速度快、应用价值高为主要特征的数据集合，正快速发展为对数量巨大、来源分散、格式多样的数据进行采集、存储和关联分析，从中发现新知识、创造新价值、提升新能力的新一代信息技术和服务业态。坚持创新驱动发展，加快大数据部署，深化大数据应用，已成为稳增长、促改革、调结构、惠民生和推动政府治理能力现代化的内在需要和必然选择。  

大数据是具有体量大、结构多样、时效性强等特征的数据，处理大数据需要采用新型计算架构和智能算法等新技术。大数据从数据源经过分析挖掘到最终获得价值一般需要经过5个主要环节，包括数据准备、数据存储与管理、计算处理、数据分析和知识展现。大数据技术涉及到的数据模型、处理模型、计算理论，与之相关的分布计算、分布存储平台技术、数据清洗和挖掘技术，流式计算、增量处理技术，数据质量控制等方面的研究和开发成果丰硕，大数据技术产品也已经进入商用阶段。有关大数据技术架构请参考图1-21。  

![84e506145195a8fa0e57527fa6c134c7.jpeg](http://docmind-api-cn-hangzhou.oss-cn-hangzhou.aliyuncs.com/1617315274244978/publicDocStreamStructure/docmind-20260519-672fb26ef598441da7a1ea2e8ee2ae02/6.png?Expires=1779206879&OSSAccessKeyId=STS.NZebDGdcxohmUjCQd3QTqZtgp&Signature=UVXAeX0T1o4Y56xQwjYjn0aDxxk%3D&x-oss-process=image%2Fcrop%2Cx_239%2Cy_816%2Cw_871%2Ch_575&security-token=CAIS1wJ1q6Ft5B2yfSjIr5nQKf7zibxZ2KqGV0zytWRmXdtdtbHMkjz2IHhMeHVhCe4Ytfs1nmxX7voZlrp6SJtIXleCZtF94oxN9h2gb4fb4xRsN1SI08%2FLI3OaLjKm9u2wCryLYbGwU%2FOpbE%2B%2B5U0X6LDmdDKkckW4OJmS8%2FBOZcgWWQ%2FKBlgvRq0hRG1YpdQdKGHaONu0LxfumRCwNkdzvRdmgm4NgsbWgO%2Fks0CP0AahlLBL996veMb%2FNfMBZskvD42Hu8VtbbfE3SJq7BxHybx7lqQs%2B02c5onBXwgBvUvdbLCOroI3cFRjFKk2A%2BtIq%2FP5lPt0%2F%2FTajZ%2F6jkwVZ7wQSz7YVABLAzk41i3D3L8ZAlWbUxylurjnXhJFq5mGrt21HrfraghQy27xNG29hwvQXkuNkr7knEkN5aYL3t8Y37R7YXuKmfjOEzylJ9M9udm4napgBytAGoABil%2Fqf5MVplUu7%2BU4BxuSUkUaa02SKOYDC8avK6WNdtkYn0D%2BXqfl9bU8xbeXPrci2hscIAZ0%2BX8aXvgTYjydQRSQKMCg%2FHjlv%2B9b3hANppoB06dPBtIIG3M0IRS%2Bxt1mARqgcjJ60wjWc0nO7Tsoa4sADgcsEbmCjhLeq0uUesIgAA%3D%3D)  

>图1-21  大数据技术框架  

#### 2.大数据关键技术  

(1)大数据存储管理技术。大数据存储技术首先需要解决的是数据海量化和快速增长需求。存储的硬件架构和文件系统的性价比要大大高于传统技术，存储容量计划应可以无限制扩展，且要求有很强的容错能力和并发读写能力。目前，谷歌文件系统(GFS)和Hadoop的分布式文件系统HDFS奠定了大数据存储技术的基础。大数据存储技术第二个要解决的是处理格式多样化的数据，这要求大数据存储管理系统能够对各种非结构化数据进行高效管理，代表产品如：谷歌BigTable和HadoopHbase等非关系型数据库(NoSQL)。  

![fd742c3d008cee00e3b8e5a5896fd3f3.jpeg](http://docmind-api-cn-hangzhou.oss-cn-hangzhou.aliyuncs.com/1617315274244978/publicDocStreamStructure/docmind-20260519-672fb26ef598441da7a1ea2e8ee2ae02/7.png?Expires=1779206879&OSSAccessKeyId=STS.NZebDGdcxohmUjCQd3QTqZtgp&Signature=GICnFQIJGwR%2Fr5zY02V%2B2oGeRUk%3D&x-oss-process=image%2Fcrop%2Cx_76%2Cy_5%2Cw_1099%2Ch_102&security-token=CAIS1wJ1q6Ft5B2yfSjIr5nQKf7zibxZ2KqGV0zytWRmXdtdtbHMkjz2IHhMeHVhCe4Ytfs1nmxX7voZlrp6SJtIXleCZtF94oxN9h2gb4fb4xRsN1SI08%2FLI3OaLjKm9u2wCryLYbGwU%2FOpbE%2B%2B5U0X6LDmdDKkckW4OJmS8%2FBOZcgWWQ%2FKBlgvRq0hRG1YpdQdKGHaONu0LxfumRCwNkdzvRdmgm4NgsbWgO%2Fks0CP0AahlLBL996veMb%2FNfMBZskvD42Hu8VtbbfE3SJq7BxHybx7lqQs%2B02c5onBXwgBvUvdbLCOroI3cFRjFKk2A%2BtIq%2FP5lPt0%2F%2FTajZ%2F6jkwVZ7wQSz7YVABLAzk41i3D3L8ZAlWbUxylurjnXhJFq5mGrt21HrfraghQy27xNG29hwvQXkuNkr7knEkN5aYL3t8Y37R7YXuKmfjOEzylJ9M9udm4napgBytAGoABil%2Fqf5MVplUu7%2BU4BxuSUkUaa02SKOYDC8avK6WNdtkYn0D%2BXqfl9bU8xbeXPrci2hscIAZ0%2BX8aXvgTYjydQRSQKMCg%2FHjlv%2B9b3hANppoB06dPBtIIG3M0IRS%2Bxt1mARqgcjJ60wjWc0nO7Tsoa4sADgcsEbmCjhLeq0uUesIgAA%3D%3D)  

系统集成项目管理工程师教程(第2版)  

(2)大数据并行分析技术。大数据的分析挖掘是数据密集型计算，需要巨大的计算能力，对计算单元和存储单元的数据吞吐率要求极高，并要求计算系统有非常好的扩展性和性价比。谷歌的MapReduce是主要的大数据分布式并行计算技术之一，而开源的分布式并行计算技术Apache HadoopMapReduce，已经成为应用最广泛的大数据计算软件平台。  

(3)大数据分析技术。大数据分析技术的发展需要在两个方面取得突破，一是对规模非常庞大的结构化数据和半结构化数据进行高效的深度分析；二是对非结构化数据进行分析，将海量复杂多源的语音、图像和视频数据转化为机器可识别的、具有明确语义的信息，获取隐性的知识。大数据分析的技术路线主要是通过建立人工智能系统，使用大量样本数据进行训练，让机器模仿人工，获得从数据中提取知识的能力。2006年，科学家根据人脑认知过程的分层特性， 提出增加人工神经网络层数和神经元节点数量， 加大机器学习的规模，构建深度神经网络，可以提高训练效果，使得神经网络技术成为机器学习分析技术的热点，并在语音识别和图像识别方面取得了很好的效果。  

有关大数据关键技术和应用更详细的论述参见本书3.8.4节。  

#### 3.大数据的应用领域  

如图1-22所示，随着信息化和信息系统应用的深入，各种数据增长非常迅速， 特别是由于智能传感器广泛部署和数据分析技术的高效，使得大数据的应用可以再现"现实世界模型"，并具有较好的实时性。  

(1)互联网行业应用。互联网访问的行为包括：访问的网站和页面，访问内容，停留时间，访问网页的关联性，购买行为，兴趣点，位置信息，社交信息等等。通过对互联网访问行为的监测分析，可以向访问者提供个性化的商业推荐，精确投放广告；还可以对互联网推广商品的市场行情进行监测；利用网站动态数据对网络状态实时监控，并针对流量、安全进行预警；通过综合分析，向公众提供诸如流行疾病的预警、节假日客运流量预告等服务。  

(2)传统领域的应用。大数据应用起源于互联网，正在向以数据生产、流通和利用为核心的金融、零售、电信、公共管理、医疗卫生等领域渗透。例如，金融机构通过收集互联网用户的微博数据、社交数据、历史交易数据来评估用户的信用级别和消费级别；零售企业通过互联网用户数据分析商品销售趋势、用户偏好。基于大数据的智慧城市(详见1.6.4节)也是大数据应用的重要领域，可整合来自经济、统计、民政、教育、卫生、人力等政府部门内部数据和来自物联网、移动互联网等网络数据，开通智慧医疗、智慧教育、智能物流、智能环保等应用。  

![725b65142c8b28e024581a9f2416a12d.jpeg](http://docmind-api-cn-hangzhou.oss-cn-hangzhou.aliyuncs.com/1617315274244978/publicDocStreamStructure/docmind-20260519-672fb26ef598441da7a1ea2e8ee2ae02/8.png?Expires=1779206878&OSSAccessKeyId=STS.NZebDGdcxohmUjCQd3QTqZtgp&Signature=P%2FLLWvbzywiQK%2BsHsngdJCQJ%2Bls%3D&x-oss-process=image%2Fcrop%2Cx_215%2Cy_246%2Cw_977%2Ch_599&security-token=CAIS1wJ1q6Ft5B2yfSjIr5nQKf7zibxZ2KqGV0zytWRmXdtdtbHMkjz2IHhMeHVhCe4Ytfs1nmxX7voZlrp6SJtIXleCZtF94oxN9h2gb4fb4xRsN1SI08%2FLI3OaLjKm9u2wCryLYbGwU%2FOpbE%2B%2B5U0X6LDmdDKkckW4OJmS8%2FBOZcgWWQ%2FKBlgvRq0hRG1YpdQdKGHaONu0LxfumRCwNkdzvRdmgm4NgsbWgO%2Fks0CP0AahlLBL996veMb%2FNfMBZskvD42Hu8VtbbfE3SJq7BxHybx7lqQs%2B02c5onBXwgBvUvdbLCOroI3cFRjFKk2A%2BtIq%2FP5lPt0%2F%2FTajZ%2F6jkwVZ7wQSz7YVABLAzk41i3D3L8ZAlWbUxylurjnXhJFq5mGrt21HrfraghQy27xNG29hwvQXkuNkr7knEkN5aYL3t8Y37R7YXuKmfjOEzylJ9M9udm4napgBytAGoABil%2Fqf5MVplUu7%2BU4BxuSUkUaa02SKOYDC8avK6WNdtkYn0D%2BXqfl9bU8xbeXPrci2hscIAZ0%2BX8aXvgTYjydQRSQKMCg%2FHjlv%2B9b3hANppoB06dPBtIIG3M0IRS%2Bxt1mARqgcjJ60wjWc0nO7Tsoa4sADgcsEbmCjhLeq0uUesIgAA%3D%3D)  

>图1-222基于大数据的应用  

### 4.大数据发展应用的目标  

为全面推进我国大数据发展和应用，加快建设数据强国，2015年，国务院印发了《促进大数据发展行动纲要》。纲要提出了立足我国国情和现实需要，推动大数据发展和应用在未来5~10年逐步实现以下目标：  

#### 1)打造精准治理、多方协作的社会治理新模式  

将大数据作为提升政府治理能力的重要手段，通过高效采集、有效整合、深化应用政府数据和社会数据，提升政府决策和风险防范水平，提高社会治理的精准性和有效性，增强乡村社会治理能力；助力简政放权，支持从事前审批向事中事后监管转变， 推动商事制度改革；促进政府监管和社会监督有机结合，有效调动社会力量参与社会治理的积极性。2017年底前形成跨部门数据资源共享共用格局。  

#### 2)建立运行平稳、安全高效的经济运行新机制  

充分运用大数据，不断提升信用、财政、金融、税收、农业、统计、进出口、资源环境、产品质量、企业登记监管等领域数据资源的获取和利用能力，丰富经济统计数据来源，实现对经济运行更为准确的监测、分析、预测、预警，提高决策的针对性、科学性和时效性，提升宏观调控以及产业发展、信用体系、市场监管等方面管理效能，保障供需平衡，促进经济平稳运行。  

#### 3)构建以人为本、惠及全民的民生服务新体系  

围绕服务型政府建设，在公用事业、市政管理、城乡环境、农村生活、健康医疗、减灾救灾、社会救助、养老服务、劳动就业、社会保障、文化教育、交通旅游、质量安全、消费维权、社区服务等领域全面推广大数据应用，利用大数据洞察民生需求，优化资源配置，丰富服务内容， 拓展服务渠道，扩大服务范围，提高服务质量，提升城市辐射能力，推动公共服务向基层延伸，缩小城乡、区域差距，促进形成公平普惠、便捷高效的民生服务体系，不断满足人民群众日益增长的个性化、多样化需求。  

88  

![c9fe1c9c8bc6f6b5edbed46f0eb4df60.jpeg](http://docmind-api-cn-hangzhou.oss-cn-hangzhou.aliyuncs.com/1617315274244978/publicDocStreamStructure/docmind-20260519-672fb26ef598441da7a1ea2e8ee2ae02/9.png?Expires=1779206879&OSSAccessKeyId=STS.NZebDGdcxohmUjCQd3QTqZtgp&Signature=cAk9tCccXqS3iLSgXWgdYhSo%2Brk%3D&x-oss-process=image%2Fcrop%2Cx_0%2Cy_3%2Cw_1222%2Ch_119&security-token=CAIS1wJ1q6Ft5B2yfSjIr5nQKf7zibxZ2KqGV0zytWRmXdtdtbHMkjz2IHhMeHVhCe4Ytfs1nmxX7voZlrp6SJtIXleCZtF94oxN9h2gb4fb4xRsN1SI08%2FLI3OaLjKm9u2wCryLYbGwU%2FOpbE%2B%2B5U0X6LDmdDKkckW4OJmS8%2FBOZcgWWQ%2FKBlgvRq0hRG1YpdQdKGHaONu0LxfumRCwNkdzvRdmgm4NgsbWgO%2Fks0CP0AahlLBL996veMb%2FNfMBZskvD42Hu8VtbbfE3SJq7BxHybx7lqQs%2B02c5onBXwgBvUvdbLCOroI3cFRjFKk2A%2BtIq%2FP5lPt0%2F%2FTajZ%2F6jkwVZ7wQSz7YVABLAzk41i3D3L8ZAlWbUxylurjnXhJFq5mGrt21HrfraghQy27xNG29hwvQXkuNkr7knEkN5aYL3t8Y37R7YXuKmfjOEzylJ9M9udm4napgBytAGoABil%2Fqf5MVplUu7%2BU4BxuSUkUaa02SKOYDC8avK6WNdtkYn0D%2BXqfl9bU8xbeXPrci2hscIAZ0%2BX8aXvgTYjydQRSQKMCg%2FHjlv%2B9b3hANppoB06dPBtIIG3M0IRS%2Bxt1mARqgcjJ60wjWc0nO7Tsoa4sADgcsEbmCjhLeq0uUesIgAA%3D%3D)  

#### 4)开启大众创业、万众创新的创新驱动新格局  

形成公共数据资源合理适度开放共享的法规制度和政策体系，2018年底前建成国家政府数据统一开放平台，率先在信用、交通、医疗、卫生、就业、社保、地理、文化、教育、科技、资源、农业、环境、安监、金融、质量、统计、气象、海洋、企业登记监管等重要领域实现公共数据资源合理适度向社会开放，带动社会公众开展大数据增值性、公益性开发和创新应用，充分释放数据红利，激发大众创业、万众创新活力。  

#### 5)培育高端智能、新兴繁荣的产业发展新生态  

推动大数据与云计算、物联网、移动互联网等新一代信息技术融合发展，探索大数据与传统产业协同发展的新业态、新模式，促进传统产业转型升级和新兴产业发展，培育新的经济增长点。形成一批满足大数据重大应用需求的产品、系统和解决方案，建立安全可信的大数据技术体系，大数据产品和服务达到国际先进水平，国内市场占有率显著提高。培育一批面向全球的骨干企业和特色鲜明的创新型中小企业。构建形成政产学研用多方联动、协调发展的大数据产业生态体系。  

#### 5.大数据发展应用的主要任务  

##### 1)加快政府数据开放共享，推动资源整合，提升治理能力  

(1)大力推动政府部门数据共享。加强顶层设计和统筹规划，明确各部门数据共享的范围边界和使用方式，厘清各部门数据管理及共享的义务和权利，依托政府数据统一共享交换平台，大力推进国家人口基础信息库、法人单位信息资源库、自然资源和空间地理基础信息库等国家基础数据资源，以及金税、金关、金财、金审、金盾、金宏、金保、金土、金农、金水、金质等信息系统跨部门、跨区域共享。加快各地区、各部门、各有关企事业单位及社会组织信用信息系统的互联互通和信息共享，丰富面向公众的信用信息服务，提高政府服务和监管水平。结合信息惠民工程实施和智慧城市建设，推动中央部门与地方政府条块结合、联合试点，实现公共服务的多方数据共享、制度对接和协同配合。  

(2)稳步推动公共数据资源开放。在依法加强安全保障和隐私保护的前提下，稳步推动公共数据资源开放。推动建立政府部门和事业单位等公共机构数据资源清单，按照"增量先行"的方式，加强对政府部门数据的国家统筹管理，加快建设国家政府数据统一开放平台。制定公共机构数据开放计划，落实数据开放和维护责任， 推进公共机构数据资源统一汇聚和集中向社会开放，提升政府数据开放共享标准化程度，优先推动信用、交通、医疗、卫生、就业、社保、地理、文化、教育、科技、资源、农业、环境、安监、金融、质量、统计、气象、海洋、企业登记监管等民生保障服务相关领域的政府数据集向社会开放。建立政府和社会互动的大数据采集形成机制，制定政府数据共享开放目录。通过政务数据公开共享，引导企业、行业协会、科研机构、社会组织等主动采集并开放数据。  

(3)统筹规划大数据基础设施建设。结合国家政务信息化工程建设规划，统筹政务数据资源和社会数据资源，布局国家大数据平台、数据中心等基础设施。加快完善国家人口基础信息库、法人单位信息资源库、自然资源和空间地理基础信息库等基础信息资源和健康、就业、社保、能源、信用、统计、质量、国土、农业、城乡建设、企业登记监管等重要领域信息资源，加强与社会大数据的汇聚整合和关联分析。推动国民经济动员大数据应用。加强军民信息资源共享。充分利用现有企业、政府等数据资源和平台设施，注重对现有数据中心及服务器资源的改造和利用，建设绿色环保、低成本、高效率、基于云计算的大数据基础设施和区域性、行业性数据汇聚平台，避免盲目建设和重复投资。加强对互联网重要数据资源的备份及保护。  

(4)支持宏观调控科学化。建立国家宏观调控数据体系，及时发布有关统计指标和数据，强化互联网数据资源利用和信息服务，加强与政务数据资源的关联分析和融合利用，为政府开展金融、税收、审计、统计、农业、规划、消费、投资、进出口、城乡建设、劳动就业、收入分配、电力及产业运行、质量安全、节能减排等领域运行动态监测、产业安全预测预警以及转变发展方式分析决策提供信息支持，提高宏观调控的科学性、预见性和有效性。  

(5)推动政府治理精准化。在企业监管、质量安全、节能降耗、环境保护、食品安全、安全生产、信用体系建设、旅游服务等领域，推动有关政府部门和企事业单位将市场监管、检验检测、违法失信、企业生产经营、销售物流、投诉举报、消费维权等数据进行汇聚整合和关联分析，统一公示企业信用信息，预警企业不正当行为，提升政府决策和风险防范能力，支持加强事中事后监管和服务，提高监管和服务的针对性、有效性。推动改进政府管理和公共治理方式，借助大数据实现政府负面清单、权力清单和责任清单的透明化管理，完善大数据监督和技术反腐体系，促进政府简政放权、依法行政。  

(6)推进商事服务便捷化。加快建立公民、法人和其他组织统一社会信用代码制度，依托全国统一的信用信息共享交换平台，建设企业信用信息公示系统和"信用中国"网站，共享整合各地区、各领域信用信息，为社会公众提供查询注册登记、行政许可、行政处罚等各类信用信息的一站式服务。在全面实行工商营业执照、组织机构代码证和税务登记证"三证合一""一照一码"登记制度改革中，积极运用大数据手段，简化办理程序。建立项目并联审批平台，形成网上审批大数据资源库，实现跨部门、跨层级项目审批、核准、备案的统一受理、同步审查、信息共享、透明公开。鼓励政府部门高效采集、有效整合并充分运用政府数据和社会数据，掌握企业需求，推动行政管理流程优化再造，在注册登记、市场准入等商事服务中提供更加便捷有效、更有针对性的服务。利用大数据等手段，密切跟踪中小微企业特别是新设小微企业运行情况，为完善相关政策提供支持。  

90  

![c3df79991e11dac2503b19f32fd3941f.jpeg](http://docmind-api-cn-hangzhou.oss-cn-hangzhou.aliyuncs.com/1617315274244978/publicDocStreamStructure/docmind-20260519-672fb26ef598441da7a1ea2e8ee2ae02/11.png?Expires=1779206879&OSSAccessKeyId=STS.NZebDGdcxohmUjCQd3QTqZtgp&Signature=NppFhe6tJ1lNyI2jRgZ4q6jk9hw%3D&x-oss-process=image%2Fcrop%2Cx_14%2Cy_5%2Cw_1163%2Ch_101&security-token=CAIS1wJ1q6Ft5B2yfSjIr5nQKf7zibxZ2KqGV0zytWRmXdtdtbHMkjz2IHhMeHVhCe4Ytfs1nmxX7voZlrp6SJtIXleCZtF94oxN9h2gb4fb4xRsN1SI08%2FLI3OaLjKm9u2wCryLYbGwU%2FOpbE%2B%2B5U0X6LDmdDKkckW4OJmS8%2FBOZcgWWQ%2FKBlgvRq0hRG1YpdQdKGHaONu0LxfumRCwNkdzvRdmgm4NgsbWgO%2Fks0CP0AahlLBL996veMb%2FNfMBZskvD42Hu8VtbbfE3SJq7BxHybx7lqQs%2B02c5onBXwgBvUvdbLCOroI3cFRjFKk2A%2BtIq%2FP5lPt0%2F%2FTajZ%2F6jkwVZ7wQSz7YVABLAzk41i3D3L8ZAlWbUxylurjnXhJFq5mGrt21HrfraghQy27xNG29hwvQXkuNkr7knEkN5aYL3t8Y37R7YXuKmfjOEzylJ9M9udm4napgBytAGoABil%2Fqf5MVplUu7%2BU4BxuSUkUaa02SKOYDC8avK6WNdtkYn0D%2BXqfl9bU8xbeXPrci2hscIAZ0%2BX8aXvgTYjydQRSQKMCg%2FHjlv%2B9b3hANppoB06dPBtIIG3M0IRS%2Bxt1mARqgcjJ60wjWc0nO7Tsoa4sADgcsEbmCjhLeq0uUesIgAA%3D%3D)  

(7)促进安全保障高效化。加强有关执法部门间的数据流通，在法律许可和确保安全的前提下，加强对社会治理相关领域数据的归集、发掘及关联分析，强化对妥善应对和处理重大突发公共事件的数据支持，提高公共安全保障能力，推动构建智能防控、综合治理的公共安全体系，维护国家安全和社会安定。  

(8)加快民生服务普惠化。结合新型城镇化发展、信息惠民工程实施和智慧城市建设，以优化提升民生服务、激发社会活力、促进大数据应用市场化服务为重点，引导鼓励企业和社会机构开展创新应用研究，深入发掘公共服务数据，在城乡建设、人居环境、健康医疗、社会救助、养老服务、劳动就业、社会保障、质量安全、文化教育、交通旅游、消费维权、城乡服务等领域开展大数据应用示范，推动传统公共服务数据与互联网、移动互联网、可穿戴设备等数据的汇聚整合，开发各类便民应用，优化公共资源配置，提升公共服务水平。  

##### 2)推动产业创新发展，培育新兴业态，助力经济转型  

(1)发展工业大数据。推动大数据在工业研发设计、生产制造、经营管理、市场营销、售后服务等产品全生命周期、产业链全流程各环节的应用，分析感知用户需求，提升产品附加价值，打造智能工厂。建立面向不同行业、不同环节的工业大数据资源聚合和分析应用平台。抓住互联网跨界融合机遇，促进大数据、物联网、云计算和三维(3D)打印技术、个性化定制等在制造业全产业链集成运用，推动制造模式变革和工业转型升级。  

(2)发展新兴产业大数据。大力培育互联网金融、数据服务、数据探矿、数据化学、数据材料、数据制药等新业态，提升相关产业大数据资源的采集获取和分析利用能力，充分发掘数据资源支撑创新的潜力，带动技术研发体系创新、管理方式变革、商业模式创新和产业价值链体系重构，推动跨领域、跨行业的数据融合和协同创新，促进战略性新兴产业发展、服务业创新发展和信息消费扩大，探索形成协同发展的新业态、新模式，培育新的经济增长点。  

(3)发展农业农村大数据。构建面向农业农村的综合信息服务体系，为农民生产生活提供综合、高效、便捷的信息服务，缩小城乡数字鸿沟，促进城乡发展一体化。加强农业农村经济大数据建设，完善村、县相关数据采集、传输、共享基础设施，建立农业农村数据采集、运算、应用、服务体系，强化农村生态环境治理，增强乡村社会治理能力。统筹国内国际农业数据资源，强化农业资源要素数据的集聚利用，提升预测预警能力。整合构建国家涉农大数据中心，推进各地区、各行业、各领域涉农数据资源的共享开放，加强数据资源发掘运用。加快农业大数据关键技术研发，加大示范力度，提升生产智能化、经营网络化、管理高效化、服务便捷化能力和水平。  

(4)发展万众创新大数据。适应国家创新驱动发展战略，实施大数据创新行动计划，鼓励企业和公众发掘利用开放数据资源，激发创新创业活力，促进创新链和产业链深度融合，推动大数据发展与科研创新有机结合，形成大数据驱动型的科研创新模式，打通科技创新和经济社会发展之间的通道，推动万众创新、开放创新和联动创新。  

(5)推进基础研究和核心技术攻关。围绕数据科学理论体系、大数据计算系统与分析理论、大数据驱动的颠覆性应用模型探索等重大基础研究进行前瞻布局，开展数据科学研究，引导和鼓励在大数据理论、方法及关键应用技术等方面展开探索。采取政产学研用相结合的协同创新模式和基于开源社区的开放创新模式，加强海量数据存储、数据清洗、数据分析发掘、数据可视化、信息安全与隐私保护等领域关键技术攻关，形成安全可靠的大数据技术体系。支持自然语言理解、机器学习、深度学习等人工智能技术创新，提升数据分析处理能力、知识发现能力和辅助决策能力。  

(6)形成大数据产品体系。围绕数据采集、整理、分析、发掘、展现、应用等环节，支持大型通用海量数据存储与管理软件、大数据分析发掘软件、数据可视化软件等软件产品和海量数据存储设备、大数据一体机等硬件产品发展，带动芯片、操作系统等信息技术核心基础产品发展， 打造较为健全的大数据产品体系。大力发展与重点行业领域业务流程及数据应用需求深度融合的大数据解决方案。  

(7)完善大数据产业链。支持企业开展基于大数据的第三方数据分析发掘服务、技术外包服务和知识流程外包服务。鼓励企业根据数据资源基础和业务特色，积极发展互联网金融和移动金融等新业态。推动大数据与移动互联网、物联网、云计算的深度融合，深化大数据在各行业的创新应用，积极探索创新协作共赢的应用模式和商业模式。加强大数据应用创新能力建设，建立政产学研用联动、大中小企业协调发展的大数据产业体系。建立和完善大数据产业公共服务支撑体系，组建大数据开源社区和产业联盟，促进协同创新，加快计量、标准化、检验检测和认证认可等大数据产业质量技术基础建设，加速大数据应用普及。  

##### 3)强化安全保障，提高管理水平，促进健康发展  

(1)健全大数据安全保障体系。加强大数据环境下的网络安全问题研究和基于大数据的网络安全技术研究，落实信息安全等级保护、风险评估等网络安全制度，建立健全大数据安全保障体系。建立大数据安全评估体系。切实加强关键信息基础设施安全防护，做好大数据平台及服务商的可靠性及安全性评测、应用安全评测、监测预警和风险评估。明确数据采集、传输、存储、使用、开放等各环节保障网络安全的范围边界、责任主体和具体要求，切实加强对涉及国家利益、公共安全、商业秘密、个人隐私、军工科研生产等信息的保护。妥善处理发展创新与保障安全的关系，审慎监管，保护创新，探索完善安全保密管理规范措施，切实保障数据安全。  

(2)强化安全支撑。采用安全可信产品和服务，提升基础设施关键设备安全可靠水平。建设国家网络安全信息汇聚共享和关联分析平台，促进网络安全相关数据融合和资源合理分配，提升重大网络安全事件应急处理能力；深化网络安全防护体系和态势感知能力建设，增强网络空间安全防护和安全事件识别能力。开展安全监测和预警通报工作，  

9292  

![d3ee58ee10f53faf53776684cef085a6.jpeg](http://docmind-api-cn-hangzhou.oss-cn-hangzhou.aliyuncs.com/1617315274244978/publicDocStreamStructure/docmind-20260519-672fb26ef598441da7a1ea2e8ee2ae02/13.png?Expires=1779206878&OSSAccessKeyId=STS.NZebDGdcxohmUjCQd3QTqZtgp&Signature=7oPv0fsEBHz5ne8GVHLYyqvcBDA%3D&x-oss-process=image%2Fcrop%2Cx_96%2Cy_5%2Cw_1098%2Ch_116&security-token=CAIS1wJ1q6Ft5B2yfSjIr5nQKf7zibxZ2KqGV0zytWRmXdtdtbHMkjz2IHhMeHVhCe4Ytfs1nmxX7voZlrp6SJtIXleCZtF94oxN9h2gb4fb4xRsN1SI08%2FLI3OaLjKm9u2wCryLYbGwU%2FOpbE%2B%2B5U0X6LDmdDKkckW4OJmS8%2FBOZcgWWQ%2FKBlgvRq0hRG1YpdQdKGHaONu0LxfumRCwNkdzvRdmgm4NgsbWgO%2Fks0CP0AahlLBL996veMb%2FNfMBZskvD42Hu8VtbbfE3SJq7BxHybx7lqQs%2B02c5onBXwgBvUvdbLCOroI3cFRjFKk2A%2BtIq%2FP5lPt0%2F%2FTajZ%2F6jkwVZ7wQSz7YVABLAzk41i3D3L8ZAlWbUxylurjnXhJFq5mGrt21HrfraghQy27xNG29hwvQXkuNkr7knEkN5aYL3t8Y37R7YXuKmfjOEzylJ9M9udm4napgBytAGoABil%2Fqf5MVplUu7%2BU4BxuSUkUaa02SKOYDC8avK6WNdtkYn0D%2BXqfl9bU8xbeXPrci2hscIAZ0%2BX8aXvgTYjydQRSQKMCg%2FHjlv%2B9b3hANppoB06dPBtIIG3M0IRS%2Bxt1mARqgcjJ60wjWc0nO7Tsoa4sADgcsEbmCjhLeq0uUesIgAA%3D%3D)  

系统集成项目管理工程师教程(第2版)  

加强大数据环境下防攻击、防泄露、防窃取的监测、预警、控制和应急处置能力建设。  

### 1.6.2云计算  

云计算是推动信息技术能力实现按需供给、促进信息技术和数据资源充分利用的全新业态，是信息化发展的重大变革和必然趋势。发展云计算，有利于分享信息知识和创新资源，降低全社会创业成本，培育形成新产业和新消费热点，对稳增长、调结构、惠民生和建设创新型国家具有重要意义。  

#### 1.云计算概念  

云计算(Cloud Computing)，是一种基于互联网的计算方式，通过这种方式，在网络上配置为共享的软件资源、计算资源、存储资源和信息资源可以按需求提供给网上终端设备和终端用户。所谓"云"是一种抽象的比喻，表示用网络包裹服务或者资源而隐蔽服务或资源共享的实现细节以及资源位置的一种状态。云计算是继大型机-终端计算模式转变为客户端-服务器计算模式的之后的又一种计算模式的转变。在这种模式下，用户不再需要了解"云"中基础设施的细节，也不必具有相应的专业知识，更无需直接进行控制，可以将信息系统的运行维护完全交给"云"平台的管理者。云计算通常通过互联网来提供动态易扩展而且经常是虚拟化的资源，并且计算能力也可作为一种资源通过互联网流通。  

云计算的主要特点包括：一是宽带网络连接，用户需要通过宽带网络接入"云"中并获得有关的服务，"云"内节点之间也通过内部的高速网络相连：二是快速、按需、弹性的服务，用户可以按照实际需求迅速获取或释放资源，并可以根据需求对资源进行动态扩展。  

#### 2.云计算服务的类型  

按照云计算服务提供的资源层次， 可以分为IaaS、PaaS和SaaS等三种服务类型。  

(1)IaaS(基础设施即服务)，向用户提供计算机能力、存储空间等基础设施方面的服务。这种服务模式需要较大的基础设施投入和长期运营管理经验，但IaaS服务单纯出租资源，盈利能力有限。  

(2)PaaS(平台即服务)，向用户提供虚拟的操作系统、数据库管理系统、Web应用等平台化的服务。PaaS服务的重点不在于直接的经济效益，而更注重构建和形成紧密的产业生态。  

(3)SaaS(软件即服务)，向用户提供应用软件(如CRM、办公软件等) 、组件、工作流等虚拟化软件的服务，SaaS一般采用 Web技术和SOA架构，通过Internet向用户提供多租户、可定制的应用能力，大大缩短了软件产业的渠道链条，减少了软件升级、定制和运行维护的复杂程度，并使软件提供商从软件产品的生产者转变为应用服务的运营者。  

具体实现例子参见本书3.8.1节。  

#### 3.云计算关键技术  

云计算技术架构包括云计算基础设施和云计算操作系统，其中云计算基础设施由数据中心基础设施和信息网络存储资源组成，云计算操作系统负责调度、管理和控制相关资源，支持对外提供IaaS、PaaS、SaaS等服务，如图1-23所示。  

![bcc3abac28259d364c0dab0ef0ab9f94.jpeg](http://docmind-api-cn-hangzhou.oss-cn-hangzhou.aliyuncs.com/1617315274244978/publicDocStreamStructure/docmind-20260519-672fb26ef598441da7a1ea2e8ee2ae02/14.png?Expires=1779206878&OSSAccessKeyId=STS.NZebDGdcxohmUjCQd3QTqZtgp&Signature=G3UynyQhPlO7UpvmkpAQ02WYUrU%3D&x-oss-process=image%2Fcrop%2Cx_189%2Cy_421%2Cw_934%2Ch_765&security-token=CAIS1wJ1q6Ft5B2yfSjIr5nQKf7zibxZ2KqGV0zytWRmXdtdtbHMkjz2IHhMeHVhCe4Ytfs1nmxX7voZlrp6SJtIXleCZtF94oxN9h2gb4fb4xRsN1SI08%2FLI3OaLjKm9u2wCryLYbGwU%2FOpbE%2B%2B5U0X6LDmdDKkckW4OJmS8%2FBOZcgWWQ%2FKBlgvRq0hRG1YpdQdKGHaONu0LxfumRCwNkdzvRdmgm4NgsbWgO%2Fks0CP0AahlLBL996veMb%2FNfMBZskvD42Hu8VtbbfE3SJq7BxHybx7lqQs%2B02c5onBXwgBvUvdbLCOroI3cFRjFKk2A%2BtIq%2FP5lPt0%2F%2FTajZ%2F6jkwVZ7wQSz7YVABLAzk41i3D3L8ZAlWbUxylurjnXhJFq5mGrt21HrfraghQy27xNG29hwvQXkuNkr7knEkN5aYL3t8Y37R7YXuKmfjOEzylJ9M9udm4napgBytAGoABil%2Fqf5MVplUu7%2BU4BxuSUkUaa02SKOYDC8avK6WNdtkYn0D%2BXqfl9bU8xbeXPrci2hscIAZ0%2BX8aXvgTYjydQRSQKMCg%2FHjlv%2B9b3hANppoB06dPBtIIG3M0IRS%2Bxt1mARqgcjJ60wjWc0nO7Tsoa4sADgcsEbmCjhLeq0uUesIgAA%3D%3D)  

>图1-23云计算技术架构  

##### 1)基础设施关键技术  

云计算基础设施关键技术包括服务器、网络和数据中心相关技术。为了实现云计算的成本目标，云计算系统中多采用X86系列刀片式服务器，通过虚拟化形成统一的服务器资源。高速网络连接是确保成千上万服务器高效协调运行的关键，同时，网络技术还应支持节点的在线维护和更换，支持自动节点故障检测和新节点的发现、注册，还要确保服务器节点之间、服务器节点和数据存储节点访问的管理一致性。数据中心的低能耗和绿色环保是发展方向，应主要围绕IT设备、制冷系统和供配电系统采用有效的节能技术。  

##### 2)操作系统关键技术  

云计算操作系统的主要关键技术包括资源池管理技术和向用户提供大规模存储、计算能力的分布式任务和数据管理技术。  

94  

![d585641a954879098b3cda30b3507a8a.jpeg](http://docmind-api-cn-hangzhou.oss-cn-hangzhou.aliyuncs.com/1617315274244978/publicDocStreamStructure/docmind-20260519-672fb26ef598441da7a1ea2e8ee2ae02/15.png?Expires=1779206879&OSSAccessKeyId=STS.NZebDGdcxohmUjCQd3QTqZtgp&Signature=%2BKr7aRZNFsI6%2FYXJw2S%2BNiLjUX4%3D&x-oss-process=image%2Fcrop%2Cx_59%2Cy_6%2Cw_1154%2Ch_117&security-token=CAIS1wJ1q6Ft5B2yfSjIr5nQKf7zibxZ2KqGV0zytWRmXdtdtbHMkjz2IHhMeHVhCe4Ytfs1nmxX7voZlrp6SJtIXleCZtF94oxN9h2gb4fb4xRsN1SI08%2FLI3OaLjKm9u2wCryLYbGwU%2FOpbE%2B%2B5U0X6LDmdDKkckW4OJmS8%2FBOZcgWWQ%2FKBlgvRq0hRG1YpdQdKGHaONu0LxfumRCwNkdzvRdmgm4NgsbWgO%2Fks0CP0AahlLBL996veMb%2FNfMBZskvD42Hu8VtbbfE3SJq7BxHybx7lqQs%2B02c5onBXwgBvUvdbLCOroI3cFRjFKk2A%2BtIq%2FP5lPt0%2F%2FTajZ%2F6jkwVZ7wQSz7YVABLAzk41i3D3L8ZAlWbUxylurjnXhJFq5mGrt21HrfraghQy27xNG29hwvQXkuNkr7knEkN5aYL3t8Y37R7YXuKmfjOEzylJ9M9udm4napgBytAGoABil%2Fqf5MVplUu7%2BU4BxuSUkUaa02SKOYDC8avK6WNdtkYn0D%2BXqfl9bU8xbeXPrci2hscIAZ0%2BX8aXvgTYjydQRSQKMCg%2FHjlv%2B9b3hANppoB06dPBtIIG3M0IRS%2Bxt1mARqgcjJ60wjWc0nO7Tsoa4sADgcsEbmCjhLeq0uUesIgAA%3D%3D)  

资源池管理技术主要实现对物理资源、虚拟资源的统一管理，并根据用户需求实现虚拟资源的自动化生成、分配和迁移。当局部物理主机发生故障或需要进行维护时，运行在此主机上的虚拟机应该可以动态地迁移到其他物理主机(即"热迁移"技术)，并保证用户业务连续。  

分布式任务管理技术实现基于大规模硬件资源上的分布式海量计算，并支持对结构化与非结构化的数据进行存储与管理。  

#### 4.发展云计算的指导思想、基本原则和发展目标  

2015年初，《国务院关于促进云计算创新发展培育信息产业新业态的意见》(国发[2015]5号)发布，在这份文件中指出了我国发展云计算的指导思想、基本原则和目标。  

##### 1)指导思想  

适应推进新型工业化、信息化、城镇化、农业现代化和国家治理能力现代化的需要，以全面深化改革为动力，以提升能力、深化应用为主线，完善发展环境，培育骨干企业，创新服务模式，扩展应用领域，强化技术支撑，保障信息安全，优化设施布局，促进云计算创新发展，培育信息产业新业态，使信息资源得到高效利用，为促进创业兴业、释放创新活力提供有力支持，为经济社会持续健康发展注入新的动力。  

##### 2)基本原则  

(1)市场主导。发挥市场在资源配置中的决定性作用，完善市场准入制度， 减少行政干预，鼓励企业根据市场需求丰富服务种类， 提升服务能力，对接应用市场。建立公平开放透明的市场规则，完善监管政策，维护良好市场秩序。  

(2)统筹协调。以需求为牵引，加强分类指导，推进重点领域的应用、服务和产品协同发展。引导地方根据实际需求合理确定云计算发展定位，避免政府资金盲目投资建设数据中心和相关园区。加强信息技术资源整合，避免行业信息化系统成为信息孤岛。优化云计算基础设施布局，促进区域协调发展。  

(3)创新驱动。以企业为主体，加强产学研用合作，强化云计算关键技术和服务模式创新，提升自主创新能力。积极探索加强国际合作，推动云计算开放式创新和国际化发展。加强管理创新，鼓励新业态发展。  

(4)保障安全。在现有信息安全保障体系基础上，结合云计算特点完善相关信息安全制度，强化安全管理和数据隐私保护，增强安全技术支撑和服务能力， 建立健全安全防护体系，切实保障云计算信息安全。充分运用云计算的大数据处理能力，带动相关安全技术和服务发展。  

3)发展目标  

到2017年，云计算在重点领域的应用得到深化， 产业链条基本健全，初步形成安全保障有力，服务创新、技术创新和管理创新协同推进的云计算发展格局，带动相关产业快速发展。  

(1)服务能力大幅提升。形成若干具有较强创新能力的公共云计算骨干服务企业。面向中小微企业和个人的云计算服务种类丰富，实现规模化运营。云计算系统集成能力显著提升。  

(2)创新能力明显增强。增强原始创新和基础创新能力，突破云计算平台软件、艾字节(EB，约为260字节)级云存储系统、大数据挖掘分析等一批关键技术与产品，云计算技术接近国际先进水平，云计算标准体系基本建立。服务创新对技术创新的带动作用显著增强，产学研用协同发展水平大幅提高。  

(3)应用示范成效显著。在社会效益明显、产业带动性强、示范作用突出的若干重点领域推动公共数据开放、信息技术资源整合和政府采购服务改革，充分利用公共云计算服务资源开展百项云计算和大数据应用示范工程，在降低创业门槛、服务民生、培育新业态、探索电子政务建设新模式等方面取得积极成效，政府自建数据中心数量减少5%以上。  

(4)基础设施不断优化。云计算数据中心区域布局初步优化，新建大型云计算数据中心能源利用效率(PUE) 值优于1.5。宽带发展政策环境逐步完善，初步建成满足云计算发展需求的宽带网络基础设施。  

(5)安全保障基本健全。初步建立适应云计算发展需求的信息安全监管制度和标准规范体系，云计算安全关键技术产品的产业化水平和网络安全防护能力明显提升，云计算发展环境更加安全可靠。  

到2020年，云计算应用基本普及，云计算服务能力达到国际先进水平，掌握云计算关键技术，形成若干具有较强国际竞争力的云计算骨干企业。云计算信息安全监管体系和法规体系健全。大数据挖掘分析能力显著提升。云计算成为我国信息化重要形态和建设网络强国的重要支撑，推动经济社会各领域信息化水平大幅提高。  

##### 5.发展云计算的主要任务  

###### 1)增强云计算服务能力  

大力发展公共云计算服务，实施云计算工程，支持信息技术企业加快向云计算产品和服务提供商转型。大力发展计算、存储资源租用和应用软件开发部署平台服务，以及企业经营管理、研发设计等在线应用服务，降低企业信息化门槛和创新成本，支持中小微企业发展和创业活动。积极发展基于云计算的个人信息存储、在线工具、学习娱乐等服务，培育信息消费。发展安全可信的云计算外包服务，推动政府业务外包。支持云计算与物联网、移动互联网、互联网金融、电子商务等技术和服务的融合发展与创新应用，积极培育新业态、新模式。鼓励大企业开放平台资源，打造协作共赢的云计算服务生态环境。引导专有云有序发展，鼓励企业创新信息化建设思路，在充分利用公共云计算服务资源的基础上，立足自身需求，利用安全可靠的专有云解决方案，整合信息资源，优化业务流程，提升经营管理水平。大力发展面向云计算的信息系统规划咨询、方案设计、系统集成和测试评估等服务。  

![a249b8f346d83f5cb139e928af4c8829.jpeg](http://docmind-api-cn-hangzhou.oss-cn-hangzhou.aliyuncs.com/1617315274244978/publicDocStreamStructure/docmind-20260519-672fb26ef598441da7a1ea2e8ee2ae02/17.png?Expires=1779206879&OSSAccessKeyId=STS.NZebDGdcxohmUjCQd3QTqZtgp&Signature=ABhzQ7MA0JO3dAZJhnuYrhYFPgs%3D&x-oss-process=image%2Fcrop%2Cx_20%2Cy_6%2Cw_1192%2Ch_101&security-token=CAIS1wJ1q6Ft5B2yfSjIr5nQKf7zibxZ2KqGV0zytWRmXdtdtbHMkjz2IHhMeHVhCe4Ytfs1nmxX7voZlrp6SJtIXleCZtF94oxN9h2gb4fb4xRsN1SI08%2FLI3OaLjKm9u2wCryLYbGwU%2FOpbE%2B%2B5U0X6LDmdDKkckW4OJmS8%2FBOZcgWWQ%2FKBlgvRq0hRG1YpdQdKGHaONu0LxfumRCwNkdzvRdmgm4NgsbWgO%2Fks0CP0AahlLBL996veMb%2FNfMBZskvD42Hu8VtbbfE3SJq7BxHybx7lqQs%2B02c5onBXwgBvUvdbLCOroI3cFRjFKk2A%2BtIq%2FP5lPt0%2F%2FTajZ%2F6jkwVZ7wQSz7YVABLAzk41i3D3L8ZAlWbUxylurjnXhJFq5mGrt21HrfraghQy27xNG29hwvQXkuNkr7knEkN5aYL3t8Y37R7YXuKmfjOEzylJ9M9udm4napgBytAGoABil%2Fqf5MVplUu7%2BU4BxuSUkUaa02SKOYDC8avK6WNdtkYn0D%2BXqfl9bU8xbeXPrci2hscIAZ0%2BX8aXvgTYjydQRSQKMCg%2FHjlv%2B9b3hANppoB06dPBtIIG3M0IRS%2Bxt1mARqgcjJ60wjWc0nO7Tsoa4sADgcsEbmCjhLeq0uUesIgAA%3D%3D)  

系统集成项目管理工程师教程(第2版)  

###### 2)提升云计算自主创新能力  

加强云计算相关基础研究、应用研究、技术研发、市场培育和产业政策的紧密衔接与统筹协调。发挥企业创新主体作用，以服务创新带动技术创新，增强原始创新能力，着力突破云计算平台大规模资源管理与调度、运行监控与安全保障、艾字节级数据存储与处理、大数据挖掘分析等关键技术，提高相关软硬件产品研发及产业化水平。加强核心电子器件、高端通用芯片及基础软件产品等科技专项成果与云计算产业需求对接，积极推动安全可靠的云计算产品和解决方案在各领域的应用。充分整合利用国内外创新资源，加强云计算相关技术研发实验室、工程中心和企业技术中心建设。建立产业创新联盟，发挥骨干企业的引领作用，培育一批特色鲜明的创新型中小企业，健全产业生态系统。完善云计算公共支撑体系，加强知识产权保护利用、标准制定和相关评估测评等工作，促进协同创新。  

###### 3)探索电子政务云计算发展新模式  

鼓励应用云计算技术整合改造现有电子政务信息系统，实现各领域政务信息系统整体部署和共建共用，大幅减少政府自建数据中心的数量。新建电子政务系统须经严格论证并按程序进行审批。政府部门要加大采购云计算服务的力度，积极开展试点示范， 探索基于云计算的政务信息化建设运行新机制，推动政务信息资源共享和业务协同，促进简政放权，加强事中事后监管，为云计算创造更大市场空间，带动云计算产业快速发展。  

###### 4)加强大数据开发与利用  

充分发挥云计算对数据资源的集聚作用，实现数据资源的融合共享， 推动大数据挖掘、分析、应用和服务。开展公共数据开放利用改革试点，出台政府机构数据开放管理规定，在保障信息安全和个人隐私的前提下，积极探索地理、人口、知识产权及其他有关管理机构数据资源向社会开放，推动政府部门间数据共享，提升社会管理和公共服务能力。重点在公共安全、疾病防治、灾害预防、就业和社会保障、交通物流、教育科研、电子商务等领域，开展基于云计算的大数据应用示范，支持政府机构和企业创新大数据服务模式。充分发挥云计算、大数据在智慧城市建设中的服务支撑作用，加强推广应用，挖掘市场潜力，服务城市经济社会发展。  

###### 5)统筹布局云计算基础设施  

加强全国数据中心建设的统筹规划，引导大型云计算数据中心优先在能源充足、气候适宜、自然灾害较少的地区部署，以实时应用为主的中小型数据中心在靠近用户所在地、电力保障稳定的地区灵活部署。地方政府和有关企业要合理确定云计算发展定位，杜绝盲目建设数据中心和相关园区。加快推进实施"宽带中国"战略，结合云计算发展布局优化网络结构，加快网络基础设施建设升级， 优化互联网网间互联架构，提升互联互通质量，降低带宽租费水平。支持采用可再生能源和节能减排技术建设绿色云计算中心。  

###### 6)提升安全保障能力  

研究完善云计算和大数据环境下个人和企业信息保护、网络信息安全相关法规与制度，制定信息收集、存储、转移、删除、跨境流动等管理规则，加快信息安全立法进程。加强云计算服务网络安全防护管理，加大云计算服务安全评估力度，建立完善党政机关云计算服务安全管理制度。落实国家信息安全等级保护制度，开展定级备案和测评等工作。完善云计算安全态势感知、安全事件预警预防及应急处置机制，加强对党政机关和金融、交通、能源等重要信息系统的安全评估和监测。支持云计算安全软硬件技术产品的研发生产、试点示范和推广应用，加快云计算安全专业化服务队伍建设。  

## 1.6.3互联网+  

### 1."互联网+"是经济发展的新形态  

"互联网+"是互联网思维的进一步实践成果，它代表一种先进的生产力，推动经济形态不断的发生演变。从而带动社会经济实体的生命力，为改革、创新、发展提供广阔的网络平台。  

"互联网+"是把互联网的创新成果与经济社会各领域深度融合，推动技术进步、效率提升和组织变革，提升实体经济创新力和生产力，形成更广泛的以互联网为基础设施和创新要素的经济社会发展新形态。在全球新一轮科技革命和产业变革中，互联网与各领域的融合发展具有广阔前景和无限潜力，已成为不可阻挡的时代潮流，正对各国经济社会发展产生着战略性和全局性的影响。  

通俗来说，"互联网+"就是"互联网+各个传统行业"，但这并不是简单的两者相加，而是利用信息通信技术以及互联网平台，让互联网与传统行业进行深度融合，创造新的发展生态。它代表一种新的社会形态，即充分发挥互联网在社会资源配置中的优化和集成作用，将互联网的创新成果深度融合于经济、社会各域之中，提升全社会的创新力和生产力，形成更广泛的以互联网为基础设施和实现工具的经济发展新形态。几十年来，"互联网+"已经改造影响了多个行业，当前大众耳熟能详的电子商务、互联网金融(ITFIN) 、在线旅游、在线影视、在线房产等行业都是"互联网+"的杰作。  

积极发挥我国互联网已经形成的比较优势，把握机遇，增强信心，加快推进"互联网+" 发展，有利于重塑创新体系、激发创新活力、培育新兴业态和创新公共服务模式，对打造大众创业、万众创新和增加公共产品、公共服务"双引擎"，主动适应和引领经济发展新常态，形成经济发展新动能，实现中国经济提质增效升级具有重要意义。  

### 2."互联网+"行动  

近年来，我国在互联网技术、产业、应用以及跨界融合等方面取得了积极进展，已具备加快推进"互联网+"发展的坚实基础，但也存在传统企业运用互联网的意识和能力不足、互联网企业对传统产业理解不够深入、新业态发展面临体制机制障碍、跨界融合型人才严重匮乏等问题，亟待加以解决。为加快推动互联网与各领域深入融合和创新发展，充分发挥"互联网+"对稳增长、促改革、调结构、惠民生、防风险的重要作用，2015年，国务院发布了《关于积极推进"互联网+"行动的指导意见》。  

8  

![66a76cb5bd3c350a601db4ab24a1a6de.jpeg](http://docmind-api-cn-hangzhou.oss-cn-hangzhou.aliyuncs.com/1617315274244978/publicDocStreamStructure/docmind-20260519-672fb26ef598441da7a1ea2e8ee2ae02/19.png?Expires=1779206879&OSSAccessKeyId=STS.NZebDGdcxohmUjCQd3QTqZtgp&Signature=rQpuUQdtQFAQhGEMrGDXt8qplLQ%3D&x-oss-process=image%2Fcrop%2Cx_15%2Cy_6%2Cw_1179%2Ch_114&security-token=CAIS1wJ1q6Ft5B2yfSjIr5nQKf7zibxZ2KqGV0zytWRmXdtdtbHMkjz2IHhMeHVhCe4Ytfs1nmxX7voZlrp6SJtIXleCZtF94oxN9h2gb4fb4xRsN1SI08%2FLI3OaLjKm9u2wCryLYbGwU%2FOpbE%2B%2B5U0X6LDmdDKkckW4OJmS8%2FBOZcgWWQ%2FKBlgvRq0hRG1YpdQdKGHaONu0LxfumRCwNkdzvRdmgm4NgsbWgO%2Fks0CP0AahlLBL996veMb%2FNfMBZskvD42Hu8VtbbfE3SJq7BxHybx7lqQs%2B02c5onBXwgBvUvdbLCOroI3cFRjFKk2A%2BtIq%2FP5lPt0%2F%2FTajZ%2F6jkwVZ7wQSz7YVABLAzk41i3D3L8ZAlWbUxylurjnXhJFq5mGrt21HrfraghQy27xNG29hwvQXkuNkr7knEkN5aYL3t8Y37R7YXuKmfjOEzylJ9M9udm4napgBytAGoABil%2Fqf5MVplUu7%2BU4BxuSUkUaa02SKOYDC8avK6WNdtkYn0D%2BXqfl9bU8xbeXPrci2hscIAZ0%2BX8aXvgTYjydQRSQKMCg%2FHjlv%2B9b3hANppoB06dPBtIIG3M0IRS%2Bxt1mARqgcjJ60wjWc0nO7Tsoa4sADgcsEbmCjhLeq0uUesIgAA%3D%3D)  

#### 1)总体思路  

顺应世界"互联网+" 发展趋势，充分发挥我国互联网的规模优势和应用优势，推动互联网由消费领域向生产领域拓展，加速提升产业发展水平，增强各行业创新能力，构筑经济社会发展新优势和新动能。坚持改革创新和市场需求导向，突出企业的主体作用，大力拓展互联网与经济社会各领域融合的广度和深度。着力深化体制机制改革，释放发展潜力和活力；着力做优存量，推动经济提质增效和转型升级；着力做大增量，培育新兴业态，打造新的增长点；着力创新政府服务模式，夯实网络发展基础，营造安全*网络环境，提升公共服务水平。  

2)基本原则  

(1)坚持开放共享。营造开放包容的发展环境，将互联网作为生产生活要素共享的重要平台，最大限度优化资源配置，加快形成以开放、共享为特征的经济社会运行新模式。  

(2)坚持融合创新。鼓励传统产业树立互联网思维，积极与"互联网+"相结合。推动互联网向经济社会各领域加速渗透，以融合促创新，最大程度汇聚各类市场要素的创新力量，推动融合性新兴产业成为经济发展新动力和新支柱。  

(3)坚持变革转型。充分发挥互联网在促进产业升级以及信息化和工业化深度融合中的平台作用，引导要素资源向实体经济集聚， 推动生产方式和发展模式变革。创新网络化公共服务模式，大幅提升公共服务能力。  

(4)坚持引领跨越。巩固提升我国互联网发展优势，加强重点领域前瞻性布局，以互联网融合创新为突破口，培育壮大新兴产业，引领新一轮科技革命和产业变革，实现跨越式发展。  

(5)坚持安全有序。完善互联网融合标准规范和法律法规，增强安全意识，强化安全管理和防护，保障网络安全。建立科学有效的市场监管方式，促进市场有序发展，保护公平竞争，防止形成行业垄断和市场壁垒。  

3)发展目标  

到2018年，互联网与经济社会各领域的融合发展进一步深化，基于互联网的新业态成为新的经济增长动力，互联网支撑大众创业、万众创新的作用进一步增强，互联网成为提供公共服务的重要手段，网络经济与实体经济协同互动的发展格局基本形成。  

(1)经济发展进一步提质增效。互联网在促进制造业、农业、能源、环保等产业转型升级方面取得积极成效，劳动生产率进一步提高。基于互联网的新兴业态不断涌现，电子商务、互联网金融快速发展，对经济提质增效的促进作用更加凸显。  

(2)社会服务进一步便捷普惠。健康医疗、教育、交通等民生领域互联网应用更加丰富，公共服务更加多元，线上线下结合更加紧密。社会服务资源配置不断优化，公众享受到更加公平、高效、优质、便捷的服务。  

(3)基础支撑进一步夯实提升。网络设施和产业基础得到有效巩固加强， 应用支撑和安全保障能力明显增强。固定宽带网络、新一代移动通信网和下一代互联网加快发展，物联网、云计算等新型基础设施更加完备。人工智能等技术及其产业化能力显著增强。  

(4)发展环境进一步开放包容。全社会对互联网融合创新的认识不断深入，互联网融合发展面临的体制机制障碍有效破除，公共数据资源开放取得实质性进展， 相关标准规范、信用体系和法律法规逐步完善。  

到2025年，网络化、智能化、服务化、协同化的"互联网+"产业生态体系基本完善，"互联网+"新经济形态初步形成，"互联网+"成为经济社会创新发展的重要驱动力量。  

### 1.6.4智慧城市  

随着信息技术的迅猛发展，城市智慧化已成为继工业化、电气化、信息化之后的"第四次浪潮"。智慧城市是新一轮信息技术变革和知识经济进一步发展的产物，是工业化、城市化与信息化深度融合的必然趋势。  

#### 1.智慧城市的内涵和意义  

国际电工委员会(IEC) 对智慧城市的定义是：智慧城市是城市发展的新理念，是推动政府职能转变、推进社会管理创新的新方法，目标是使得基础设施更加智能、公共服务更加便捷、社会管理更加精细、生态环境更加宜居、产业体系更加优化。  

智慧城市是利用新一代信息技术来感知、监测、分析、整合城市资源，对各种需求做出迅速、灵活、准确反应，为公众创造绿色、和谐环境，提供泛在、便捷、高效服务的城市形态。通过对新一代信息技术的创新应用来建设和发展智慧城市，是我国社会实现工业化、城镇化、信息化发展目标的重要举措，也是破解城市发展难题、提升公共服务能力、转变经济发展方式的必然要求。新一代信息技术包括云计算、大数据、物联网、地理信息、人工智能、移动计算等，是"互联网+"在现代城市管理的综合应用，是"数字城市"发展的必然和全面跃升。  

智慧城市已经成为全球城市发展关注的热点，随着信息技术迅速发展和深入应用，城市信息化发展向更高阶段的智慧化发展已成为必然趋势。在此背景下，世界主要发达国家的主要城市如东京、伦敦、巴黎、首尔等等纷纷启动智慧城市战略，以增强城市综合竞争力。  

我国政府高度重视对智慧城市建设及发展的指导。2014年3月国务院印发《国家新型城镇化规划(2014一2020年)》， 2014年7月，经国务院同意，国家发展改革委、工业和信息化部等八部委印发《关于促进智慧城市健康发展的指导意见》，为建设智慧城市给出了方向性、规范性和原则性的建议。北京、南京、沈阳、上海、杭州、宁波、无锡等城市结合了城市区域内自身定位和发展需求，陆续出台了智慧城市发展规划，涉及社会管理、应用服务、基础设施、智慧产业、安全保障、建设模式、标准体系等内容，这些规划在发展目标、重点等方面各有特色，在城市普遍面临的诸如人口拥挤、资源短缺、环境污染、交通堵塞等各类"通病"和关键问题上有一定共识，例如：智慧城市建设成败的关键不再是数字城市建设中建设大量IT系统，而是如何有效推进城市范围内数据资源的融合，通过数据和IT系统的融合来实现跨部门的协同共享、行业的行动协调、城市的精细化运行管理等。  

![a2969507c87a376d3c6a65605f826efe.jpeg](http://docmind-api-cn-hangzhou.oss-cn-hangzhou.aliyuncs.com/1617315274244978/publicDocStreamStructure/docmind-20260519-672fb26ef598441da7a1ea2e8ee2ae02/21.png?Expires=1779206879&OSSAccessKeyId=STS.NZebDGdcxohmUjCQd3QTqZtgp&Signature=%2Fej%2F8WfEWF7FWuiW62PGOIyc7Xk%3D&x-oss-process=image%2Fcrop%2Cx_0%2Cy_6%2Cw_1296%2Ch_115&security-token=CAIS1wJ1q6Ft5B2yfSjIr5nQKf7zibxZ2KqGV0zytWRmXdtdtbHMkjz2IHhMeHVhCe4Ytfs1nmxX7voZlrp6SJtIXleCZtF94oxN9h2gb4fb4xRsN1SI08%2FLI3OaLjKm9u2wCryLYbGwU%2FOpbE%2B%2B5U0X6LDmdDKkckW4OJmS8%2FBOZcgWWQ%2FKBlgvRq0hRG1YpdQdKGHaONu0LxfumRCwNkdzvRdmgm4NgsbWgO%2Fks0CP0AahlLBL996veMb%2FNfMBZskvD42Hu8VtbbfE3SJq7BxHybx7lqQs%2B02c5onBXwgBvUvdbLCOroI3cFRjFKk2A%2BtIq%2FP5lPt0%2F%2FTajZ%2F6jkwVZ7wQSz7YVABLAzk41i3D3L8ZAlWbUxylurjnXhJFq5mGrt21HrfraghQy27xNG29hwvQXkuNkr7knEkN5aYL3t8Y37R7YXuKmfjOEzylJ9M9udm4napgBytAGoABil%2Fqf5MVplUu7%2BU4BxuSUkUaa02SKOYDC8avK6WNdtkYn0D%2BXqfl9bU8xbeXPrci2hscIAZ0%2BX8aXvgTYjydQRSQKMCg%2FHjlv%2B9b3hANppoB06dPBtIIG3M0IRS%2Bxt1mARqgcjJ60wjWc0nO7Tsoa4sADgcsEbmCjhLeq0uUesIgAA%3D%3D)  

# 100  

系统集成项目管理工程师教程(第2版)  

#### 2.智慧城市参考模型  

智慧城市建设主要包括以下几部分：首先，通过传感器或信息采集设备全方位地获取城市系统数据；其次，通过网络将城市数据关联、融合、处理、分析为信息；第三，通过充分共享、智能挖掘将信息变成知识；最后，结合信息技术，把知识应用到各行各业形成智慧。  

智慧城市建设参考模型包括有依赖关系的5层和对建设有约束关系的3个支撑体系。如图1-24所示。  

![143366b6f95dbc5fc61823c211c78867.jpeg](http://docmind-api-cn-hangzhou.oss-cn-hangzhou.aliyuncs.com/1617315274244978/publicDocStreamStructure/docmind-20260519-672fb26ef598441da7a1ea2e8ee2ae02/21.png?Expires=1779206879&OSSAccessKeyId=STS.NZebDGdcxohmUjCQd3QTqZtgp&Signature=C7UiMEmlGZeKrjz%2BFnuqmM5UEzk%3D&x-oss-process=image%2Fcrop%2Cx_135%2Cy_948%2Cw_1056%2Ch_692&security-token=CAIS1wJ1q6Ft5B2yfSjIr5nQKf7zibxZ2KqGV0zytWRmXdtdtbHMkjz2IHhMeHVhCe4Ytfs1nmxX7voZlrp6SJtIXleCZtF94oxN9h2gb4fb4xRsN1SI08%2FLI3OaLjKm9u2wCryLYbGwU%2FOpbE%2B%2B5U0X6LDmdDKkckW4OJmS8%2FBOZcgWWQ%2FKBlgvRq0hRG1YpdQdKGHaONu0LxfumRCwNkdzvRdmgm4NgsbWgO%2Fks0CP0AahlLBL996veMb%2FNfMBZskvD42Hu8VtbbfE3SJq7BxHybx7lqQs%2B02c5onBXwgBvUvdbLCOroI3cFRjFKk2A%2BtIq%2FP5lPt0%2F%2FTajZ%2F6jkwVZ7wQSz7YVABLAzk41i3D3L8ZAlWbUxylurjnXhJFq5mGrt21HrfraghQy27xNG29hwvQXkuNkr7knEkN5aYL3t8Y37R7YXuKmfjOEzylJ9M9udm4napgBytAGoABil%2Fqf5MVplUu7%2BU4BxuSUkUaa02SKOYDC8avK6WNdtkYn0D%2BXqfl9bU8xbeXPrci2hscIAZ0%2BX8aXvgTYjydQRSQKMCg%2FHjlv%2B9b3hANppoB06dPBtIIG3M0IRS%2Bxt1mARqgcjJ60wjWc0nO7Tsoa4sADgcsEbmCjhLeq0uUesIgAA%3D%3D)  

>图1-24智慧城市建设参考模型  

##### 1)功能层  

(1)物联感知层：提供对城市环境的智能感知能力，通过各种信息采集设备、各类传感器、监控摄像机、GPS终端等实现对城市范围内的基础设施、大气环境、交通、公共安全等方面信息采集、识别和监测。  

(2)通信网络层：广泛互联，以互联网、电信网、广播电视网以及传输介质为光纤的城市专用网作为骨干传输网络，以覆盖全城的无线网络(如WiFi) 、移动4G为主要接入网，组成网络通信基础设施。  

图1-25是位于北京延庆的GPS卫星信号接收基站，通过计算GPS信号的延迟，可以监测地壳形变和大气水汽的变化，精度可以到毫米级，数据通过网络实时传送到管理中心，综合其他信息，对城市天气预报和城市防震减灾有辅助决策作用。  

![25f9a782cad3e1eee83f4258c82efc39.jpeg](http://docmind-api-cn-hangzhou.oss-cn-hangzhou.aliyuncs.com/1617315274244978/publicDocStreamStructure/docmind-20260519-672fb26ef598441da7a1ea2e8ee2ae02/22.png?Expires=1779206879&OSSAccessKeyId=STS.NZebDGdcxohmUjCQd3QTqZtgp&Signature=h87XN1WDsia%2FseTDANnaMyvUgB0%3D&x-oss-process=image%2Fcrop%2Cx_143%2Cy_714%2Cw_1062%2Ch_824&security-token=CAIS1wJ1q6Ft5B2yfSjIr5nQKf7zibxZ2KqGV0zytWRmXdtdtbHMkjz2IHhMeHVhCe4Ytfs1nmxX7voZlrp6SJtIXleCZtF94oxN9h2gb4fb4xRsN1SI08%2FLI3OaLjKm9u2wCryLYbGwU%2FOpbE%2B%2B5U0X6LDmdDKkckW4OJmS8%2FBOZcgWWQ%2FKBlgvRq0hRG1YpdQdKGHaONu0LxfumRCwNkdzvRdmgm4NgsbWgO%2Fks0CP0AahlLBL996veMb%2FNfMBZskvD42Hu8VtbbfE3SJq7BxHybx7lqQs%2B02c5onBXwgBvUvdbLCOroI3cFRjFKk2A%2BtIq%2FP5lPt0%2F%2FTajZ%2F6jkwVZ7wQSz7YVABLAzk41i3D3L8ZAlWbUxylurjnXhJFq5mGrt21HrfraghQy27xNG29hwvQXkuNkr7knEkN5aYL3t8Y37R7YXuKmfjOEzylJ9M9udm4napgBytAGoABil%2Fqf5MVplUu7%2BU4BxuSUkUaa02SKOYDC8avK6WNdtkYn0D%2BXqfl9bU8xbeXPrci2hscIAZ0%2BX8aXvgTYjydQRSQKMCg%2FHjlv%2B9b3hANppoB06dPBtIIG3M0IRS%2Bxt1mARqgcjJ60wjWc0nO7Tsoa4sADgcsEbmCjhLeq0uUesIgAA%3D%3D)  

>图1-255 (GPS接收基站， 用于监测地壳形变和大气水汽变化，数据通过网络实时传送到管理中心  

(3)计算与存储层：包括软件资源、计算资源和存储资源，为智慧城市提供数据存储和计算，保障上层对于数据汇聚的相关需求。  

102  

![ff1ed6e27b869b5636661c844c7febee.jpeg](http://docmind-api-cn-hangzhou.oss-cn-hangzhou.aliyuncs.com/1617315274244978/publicDocStreamStructure/docmind-20260519-672fb26ef598441da7a1ea2e8ee2ae02/23.png?Expires=1779206878&OSSAccessKeyId=STS.NZebDGdcxohmUjCQd3QTqZtgp&Signature=wBM1VCQ5rZD7ZmEpjBj%2FMZloYkY%3D&x-oss-process=image%2Fcrop%2Cx_114%2Cy_8%2Cw_1043%2Ch_111&security-token=CAIS1wJ1q6Ft5B2yfSjIr5nQKf7zibxZ2KqGV0zytWRmXdtdtbHMkjz2IHhMeHVhCe4Ytfs1nmxX7voZlrp6SJtIXleCZtF94oxN9h2gb4fb4xRsN1SI08%2FLI3OaLjKm9u2wCryLYbGwU%2FOpbE%2B%2B5U0X6LDmdDKkckW4OJmS8%2FBOZcgWWQ%2FKBlgvRq0hRG1YpdQdKGHaONu0LxfumRCwNkdzvRdmgm4NgsbWgO%2Fks0CP0AahlLBL996veMb%2FNfMBZskvD42Hu8VtbbfE3SJq7BxHybx7lqQs%2B02c5onBXwgBvUvdbLCOroI3cFRjFKk2A%2BtIq%2FP5lPt0%2F%2FTajZ%2F6jkwVZ7wQSz7YVABLAzk41i3D3L8ZAlWbUxylurjnXhJFq5mGrt21HrfraghQy27xNG29hwvQXkuNkr7knEkN5aYL3t8Y37R7YXuKmfjOEzylJ9M9udm4napgBytAGoABil%2Fqf5MVplUu7%2BU4BxuSUkUaa02SKOYDC8avK6WNdtkYn0D%2BXqfl9bU8xbeXPrci2hscIAZ0%2BX8aXvgTYjydQRSQKMCg%2FHjlv%2B9b3hANppoB06dPBtIIG3M0IRS%2Bxt1mARqgcjJ60wjWc0nO7Tsoa4sADgcsEbmCjhLeq0uUesIgAA%3D%3D)  

(4)数据及服务支撑层：利用SOA(面向服务的体系架构)、云计算、大数据等技术，通过数据和服务的融合，支撑承载智慧应用层中的相关应用，提供应用所需的各种服务和共享资源。  

(5)智慧应用层：各种基于行业或领域的智慧应用及应用整合，如智慧交通、智慧家政、智慧园区、智慧社区、智慧政务、智慧旅游、智慧环保等，为社会公众、企业、城市管理者等提供整体的信息化应用和服务。  

2)支撑体系  

(1)安全保障体系：为智慧城市建设构建统一的安全平台，实现统一入口、统一认证、统一授权、日志记录服务。  

(2)建设和运营管理体系：为智慧城市建设提供整体的运维管理机制，确保智慧城市整体建设管理和可持续运行。  

(3)标准规范体系：标准规范体系用于指导和支撑我国各地城市信息化用户、各行业智慧应用信息系统的总体规划和工程建设，同时规范和引导我国智慧城市相关IT产业的发展，为智慧城市建设、管理和运行维护提供统一规范，便于互联、共享、互操作和扩展。  

#### 3.智慧城市建设的指导思想、基本原则和主要目标  

1)指导思想  

按照走集约、智能、绿色、低碳的新型城镇化道路的总体要求，发挥市场在资源配置中的决定性作用，加强和完善政府引导，统筹物质、信息和智力资源，推动新一代信息技术创新应用，加强城市管理和服务体系智能化建设，积极发展民生服务智慧应用，强化网络安全保障，有效提高城市综合承载能力和居民幸福感受，促进城镇化发展质量和水平全面提升。  

##### 2)基本原则  

(1)以人为本，务实推进。智慧城市建设要突出为民、便民、惠民，推动创新城市管理和公共服务方式，向城市居民提供广覆盖、多层次、差异化、高质量的公共服务，避免重建设、轻实效，使公众分享智慧城市建设成果。  

(2)因地制宜，科学有序。以城市发展需求为导向，根据城市地理区位、历史文化、资源禀赋、产业特色、信息化基础等，应用先进适用技术科学推进智慧城市建设。在综合条件较好的区域或重点领域先行先试，有序推动智慧城市发展，避免贪大求全、重复建设。  

(3)市场为主，协同创新。积极探索智慧城市的发展路径、管理方式、推进模式和保障机制。鼓励建设和运营模式创新，注重激发市场活力，建立可持续发展机制。鼓励社会资本参与建设投资和运营，杜绝政府大包大揽和不必要的行政干预。  

(4) 可管可控，确保安全。落实国家信息安全等级保护制度，强化网络和信息安全管理，落实责任机制，健全网络和信息安全标准体系，加大依法管理网络和保护个人信息的力度，加强要害信息系统和信息基础设施安全保障，确保安全可控。  

3)主要目标  

到2020年，建成一批特色鲜明的智慧城市，聚集和辐射带动作用大幅增强，综合竞争优势明显提高，在保障和改善民生服务、创新社会管理、维护网络安全等方面取得显著成效。  

(1)公共服务便捷化。在教育文化、医疗卫生、计划生育、劳动就业、社会保障、住房保障、环境保护、交通出行、防灾减灾、检验检测等公共服务领域，基本建成覆盖城乡居民、农民工及其随迁家属的信息服务体系，公众获取基本公共服务更加方便、及时、高效。  

(2)城市管理精细化。市政管理、人口管理、交通管理、公共安全、应急管理、社会诚信、市场监管、检验检疫、食品药品安全、饮用水安全等社会管理领域的信息化体系基本形成，统筹数字化城市管理信息系统、城市地理空间信息及建(构)筑物数据库等资源，实现城市规划和城市基础设施管理的数字化、精准化水平大幅提升，推动政府行政效能和城市管理水平大幅提升。  

(3)生活环境宜居化。居民生活数字化水平显著提高，水、大气、噪声、土壤和自然植被环境智能监测体系和污染物排放、能源消耗在线防控体系基本建成，促进城市人居环境得到改善。  

(4)基础设施智能化。宽带、融合、安全、泛在的下一代信息基础设施基本建成。电力、燃气、交通、水务、物流等公用基础设施的智能化水平大幅提升，运行管理实现精准化、协同化、一体化。工业化与信息化深度融合，信息服务业加快发展。  

(5)网络安全长效化。城市网络安全保障体系和管理制度基本建立，基础网络和要害信息系统安全可控，重要信息资源安全得到切实保障，居民、企业和政府的信息得到有效保护。  

#### 4.智慧城市建设的关键  

1)科学制定智慧城市建设顶层设计  

(1)加强顶层设计。城市人民政府要从城市发展的战略全局出发研究制定智慧城市建设方案。方案要突出为人服务，深化重点领域智慧化应用，提供更加便捷、高效、低成本的社会服务；要明确推进信息资源共享和社会化开发利用、强化信息安全、保障信息准确可靠以及同步加强信用环境建设、完善法规标准等的具体措施；要加强与国民经济和社会发展总体规划、主体功能区规划、相关行业发展规划、区域规划、城乡规划以及有关专项规划的衔接，做好统筹城乡发展布局。  

104  

![9e7b49dc92e20e29fda529baca429b6e.jpeg](http://docmind-api-cn-hangzhou.oss-cn-hangzhou.aliyuncs.com/1617315274244978/publicDocStreamStructure/docmind-20260519-672fb26ef598441da7a1ea2e8ee2ae02/25.png?Expires=1779206879&OSSAccessKeyId=STS.NZebDGdcxohmUjCQd3QTqZtgp&Signature=bAiz%2B6cepWiEr96WnRnV6RodSBU%3D&x-oss-process=image%2Fcrop%2Cx_0%2Cy_2%2Cw_1223%2Ch_123&security-token=CAIS1wJ1q6Ft5B2yfSjIr5nQKf7zibxZ2KqGV0zytWRmXdtdtbHMkjz2IHhMeHVhCe4Ytfs1nmxX7voZlrp6SJtIXleCZtF94oxN9h2gb4fb4xRsN1SI08%2FLI3OaLjKm9u2wCryLYbGwU%2FOpbE%2B%2B5U0X6LDmdDKkckW4OJmS8%2FBOZcgWWQ%2FKBlgvRq0hRG1YpdQdKGHaONu0LxfumRCwNkdzvRdmgm4NgsbWgO%2Fks0CP0AahlLBL996veMb%2FNfMBZskvD42Hu8VtbbfE3SJq7BxHybx7lqQs%2B02c5onBXwgBvUvdbLCOroI3cFRjFKk2A%2BtIq%2FP5lPt0%2F%2FTajZ%2F6jkwVZ7wQSz7YVABLAzk41i3D3L8ZAlWbUxylurjnXhJFq5mGrt21HrfraghQy27xNG29hwvQXkuNkr7knEkN5aYL3t8Y37R7YXuKmfjOEzylJ9M9udm4napgBytAGoABil%2Fqf5MVplUu7%2BU4BxuSUkUaa02SKOYDC8avK6WNdtkYn0D%2BXqfl9bU8xbeXPrci2hscIAZ0%2BX8aXvgTYjydQRSQKMCg%2FHjlv%2B9b3hANppoB06dPBtIIG3M0IRS%2Bxt1mARqgcjJ60wjWc0nO7Tsoa4sADgcsEbmCjhLeq0uUesIgAA%3D%3D)  

系统集成项目管理工程师教程(第2版)  

(2)推动构建普惠化公共服务体系。加快实施信息惠民工程。推进智慧医院、远程医疗建设，普及应用电子病历和健康档案，促进优质医疗资源纵向流动。建设具有随时看护、远程关爱等功能的养老信息化服务体系。建立公共就业信息服务平台，加快推进就业信息全国联网。加快社会保障经办信息化体系建设， 推进医保费用跨市即时结算。推进社会保障卡、金融IC卡、市民服务卡、居民健康卡、交通卡等公共服务卡的应用集成和跨市一卡通用。围绕促进教育公平、提高教育质量和满足市民终身学习需求，建设完善教育信息化基础设施， 构建利用信息化手段扩大优质教育资源覆盖面的有效机制，推进优质教育资源共享与服务。加强数字图书馆、数字档案馆、数字博物馆等公益设施建设。鼓励发展基于移动互联网的旅游服务系统和旅游管理信息平台。  

(3)支撑建立精细化社会管理体系。建立全面设防、一体运作、精确定位、有效管控的社会治安防控体系。整合各类视频图像信息资源，推进公共安全视频联网应用。完善社会化、网络化、网格化的城乡公共安全保障体系，构建反应及时、恢复迅速、支援有力的应急保障体系。在食品药品、消费品安全、检验检疫等领域，建设完善具有溯源追查、社会监督等功能的市场监管信息服务体系，推进药品阳光采购。整合信贷、纳税、履约、产品质量、参保缴费和违法违纪等信用信息记录，加快征信信息系统建设。完善群众诉求表达和受理信访的网络平台，推进政府办事网上公开。  

(4)促进宜居化生活环境建设。建立环境信息智能分析系统、预警应急系统和环境质量管理公共服务系统，对重点地区、重点企业和污染源实施智能化远程监测。依托城市统一公共服务信息平台建设社区公共服务信息系统，拓展社会管理和服务功能，发展面向家政、养老、社区照料和病患陪护的信息服务体系，为社区居民提供便捷的综合信息服务。推广智慧家庭，鼓励将医疗、教育、安防、政务等社会公共服务设施和服务资源接入家庭，提升家庭信息化服务水平。  

(5)建立现代化产业发展体系。运用现代信息化手段，加快建立城市物流配送体系和城市消费需求与农产品供给紧密衔接的新型农业生产经营体系。加速工业化与信息化深度融合，推进大型工业企业深化信息技术的综合集成应用，建设完善中小企业公共信息服务平台，积极培育发展工业互联网等新兴业态。加快发展信息服务业，鼓励信息系统服务外包。建设完善电子商务基础设施， 积极培育电子商务服务业，促进电子商务向旅游、餐饮、文化娱乐、家庭服务、养老服务、社区服务以及工业设计、文化创意等领域发展。  

(6)加快建设智能化基础设施。加快构建城乡一体的宽带网络，推进下一代互联网和广播电视网建设，全面推广三网融合。推动城市公用设施、建筑等智能化改造，完善建筑数据库、房屋管理等信息系统和服务平台。加快智能电网建设。健全防灾减灾预报预警信息平台，建设全过程智能水务管理系统和饮用水安全电子监控系统。建设交通诱导、出行信息服务、公共交通、综合客运枢纽、综合运行协调指挥等智能系统，推进北斗导航卫星地基增强系统建设，发展差异化交通信息增值服务。建设智能物流信息平台和仓储式物流平台枢纽，加强港口、航运、陆运等物流信息的开发共享和社会化应用。  

##### 2)切实加大信息资源开发共享力度  

(1)加快推进信息资源共享与更新。统筹城市地理空间信息及建(构)筑物数据库等资源，加快智慧城市公共信息平台和应用体系建设。建立促进信息共享的跨部门协调机制，完善信息更新机制，进一步加强政务部门信息共享和信息更新管理。各政务部门应根据职能分工，将本部门建设管理的信息资源授权有需要的部门无偿使用，共享部门应按授权范围合理使用信息资源。以城市统一的地理空间框架和人口、法人等信息资源为基础，叠加各部门、各行业相关业务信息，加快促进跨部门协同应用。整合已建政务信息系统，统筹新建系统，建设信息资源共享设施，实现基础信息资源和业务信息资源的集约化采集、网络化汇聚和统一化管理。  

(2)深化重点领域信息资源开发利用。城市人民政府要将提高信息资源开发利用水平作为提升城市综合竞争力的重要手段，大力推动政府部门将企业信用、产品质量、食品药品安全、综合交通、公用设施、环境质量等信息资源向社会开放，鼓励市政公用企事业单位、公共服务事业单位等机构将教育、医疗、就业、旅游、生活等信息资源向社会开放。支持社会力量应用信息资源发展便民、惠民、实用的新型信息服务。鼓励发展以信息知识加工和创新为主的数据挖掘、商业分析等新型服务，加速信息知识向产品、资产及效益转化。  

##### 3)积极运用新技术新业态  

###### (1)加快重点领域物联网应用  

支持物联网在高耗能行业的应用，促进生产制造、经营管理和能源利用智能化。鼓励物联网在农产品生产流通等领域应用。加快物联网在城市管理、交通运输、节能减排、食品药品安全、社会保障、医疗卫生、民生服务、公共安全、产品质量等领域的推广应用，提高城市管理精细化水平，逐步形成全面感知、广泛互联的城市智能管理和服务体系。  

###### (2)促进云计算和大数据健康发展  

鼓励电子政务系统向云计算模式迁移。在教育、医疗卫生、劳动就业、社会保障等重点民生领域，推广低成本、高质量、广覆盖的云服务，支持各类企业充分利用公共云计算服务资源。加强基于云计算的大数据开发与利用，在电子商务、工业设计、科学研究、交通运输等领域，创新大数据商业模式，服务城市经济社会发展。  

![09a9f84294cf23cc63fc06ac1749b690.jpeg](http://docmind-api-cn-hangzhou.oss-cn-hangzhou.aliyuncs.com/1617315274244978/publicDocStreamStructure/docmind-20260519-672fb26ef598441da7a1ea2e8ee2ae02/27.png?Expires=1779206878&OSSAccessKeyId=STS.NZebDGdcxohmUjCQd3QTqZtgp&Signature=spEoXj9hujRktXYDDk1Vn%2BaBGQM%3D&x-oss-process=image%2Fcrop%2Cx_28%2Cy_3%2Cw_1275%2Ch_120&security-token=CAIS1wJ1q6Ft5B2yfSjIr5nQKf7zibxZ2KqGV0zytWRmXdtdtbHMkjz2IHhMeHVhCe4Ytfs1nmxX7voZlrp6SJtIXleCZtF94oxN9h2gb4fb4xRsN1SI08%2FLI3OaLjKm9u2wCryLYbGwU%2FOpbE%2B%2B5U0X6LDmdDKkckW4OJmS8%2FBOZcgWWQ%2FKBlgvRq0hRG1YpdQdKGHaONu0LxfumRCwNkdzvRdmgm4NgsbWgO%2Fks0CP0AahlLBL996veMb%2FNfMBZskvD42Hu8VtbbfE3SJq7BxHybx7lqQs%2B02c5onBXwgBvUvdbLCOroI3cFRjFKk2A%2BtIq%2FP5lPt0%2F%2FTajZ%2F6jkwVZ7wQSz7YVABLAzk41i3D3L8ZAlWbUxylurjnXhJFq5mGrt21HrfraghQy27xNG29hwvQXkuNkr7knEkN5aYL3t8Y37R7YXuKmfjOEzylJ9M9udm4napgBytAGoABil%2Fqf5MVplUu7%2BU4BxuSUkUaa02SKOYDC8avK6WNdtkYn0D%2BXqfl9bU8xbeXPrci2hscIAZ0%2BX8aXvgTYjydQRSQKMCg%2FHjlv%2B9b3hANppoB06dPBtIIG3M0IRS%2Bxt1mARqgcjJ60wjWc0nO7Tsoa4sADgcsEbmCjhLeq0uUesIgAA%3D%3D)  

系统集成项目管理工程师教程(第2版)  

###### (3)推动信息技术集成应用  

面向公众实际需要，重点在交通运输联程联运、城市共同配送、灾害防范与应急处置、家居智能管理、居家看护与健康管理、集中养老与远程医疗、智能建筑与智慧社区、室内外统一位置服务、旅游娱乐消费等领域，加强移动互联网、遥感遥测、北斗导航、地理信息等技术的集成应用，创新服务模式，为城市居民提供方便、实用的新型服务。  

#### 4)着力加强网络信息安全管理和能力建设  

##### (1)严格全流程网络安全管理  

城市人民政府在推进智慧城市建设中要同步加强网络安全保障工作。在重要信息系统设计阶段，要合理确定安全保护等级， 同步设计安全防护方案；在实施阶段，要加强对技术、设备和服务提供商的安全审查，同步建设安全防护手段；在运行阶段，要加强管理，定期开展检查、等级评测和风险评估，认真排查安全风险隐患，增强日常监测和应急响应处置恢复能力。  

##### (2)加强要害信息设施和信息资源安全防护  

加大对党政军、金融、能源、交通、电信、公共安全、公用事业等重要信息系统和涉密信息系统的安全防护，确保安全可控。完善网络安全设施，重点提高网络管理、态势预警、应急处理和信任服务能力。统筹建设容灾备份体系，推行联合灾备和异地灾备。建立重要信息使用管理和安全评价机制。严格落实国家有关法律法规及标准，加强行业和企业自律，切实加强个人信息保护。  

##### (3)强化安全责任和安全意识  

建立网络安全责任制，明确城市人民政府及有关部门负责人、要害信息系统运营单位负责人的网络信息安全责任，建立责任追究机制。加大宣传教育力度，提高智慧城市规划、建设、管理、维护等各环节工作人员的网络信息安全风险意识、责任意识、工作技能和管理水平。鼓励发展专业化、社会化的信息安全认证服务，为保障智慧城市网络信息安全提供支持。  

#### 5.智慧城市典型应用  

(1)公用事业智能化。运用物联网、云计算等新一代信息技术，以水、电、气、热及地下管线等市政公共基础设施的信息采集、信息网络和数据中心建设为重点，建设智能供水、供电、供暖、供气和城市地下管线综合管理体系，提高公用事业智能化运行水平。  

(2)城市智能交通。实现对车辆、道路、泊位等交通信息的精确采集、及时发布与共享，提高调度管理智能化水平。图1-26所示的交通流量监测系统，通过随车的移动终端上的交通软件，实时获取道路流量信息和车辆速度信息，经过计算平台的综合分析，可以获得城市主要道路、路口的交通实时信息并做出交通预测。  

![857db28c17ed8367856d375e50b0ae84.jpeg](http://docmind-api-cn-hangzhou.oss-cn-hangzhou.aliyuncs.com/1617315274244978/publicDocStreamStructure/docmind-20260519-672fb26ef598441da7a1ea2e8ee2ae02/28.png?Expires=1779206878&OSSAccessKeyId=STS.NZebDGdcxohmUjCQd3QTqZtgp&Signature=h6omSG07TzEMSB%2FDMRiM3emkwo8%3D&x-oss-process=image%2Fcrop%2Cx_149%2Cy_305%2Cw_1047%2Ch_316&security-token=CAIS1wJ1q6Ft5B2yfSjIr5nQKf7zibxZ2KqGV0zytWRmXdtdtbHMkjz2IHhMeHVhCe4Ytfs1nmxX7voZlrp6SJtIXleCZtF94oxN9h2gb4fb4xRsN1SI08%2FLI3OaLjKm9u2wCryLYbGwU%2FOpbE%2B%2B5U0X6LDmdDKkckW4OJmS8%2FBOZcgWWQ%2FKBlgvRq0hRG1YpdQdKGHaONu0LxfumRCwNkdzvRdmgm4NgsbWgO%2Fks0CP0AahlLBL996veMb%2FNfMBZskvD42Hu8VtbbfE3SJq7BxHybx7lqQs%2B02c5onBXwgBvUvdbLCOroI3cFRjFKk2A%2BtIq%2FP5lPt0%2F%2FTajZ%2F6jkwVZ7wQSz7YVABLAzk41i3D3L8ZAlWbUxylurjnXhJFq5mGrt21HrfraghQy27xNG29hwvQXkuNkr7knEkN5aYL3t8Y37R7YXuKmfjOEzylJ9M9udm4napgBytAGoABil%2Fqf5MVplUu7%2BU4BxuSUkUaa02SKOYDC8avK6WNdtkYn0D%2BXqfl9bU8xbeXPrci2hscIAZ0%2BX8aXvgTYjydQRSQKMCg%2FHjlv%2B9b3hANppoB06dPBtIIG3M0IRS%2Bxt1mARqgcjJ60wjWc0nO7Tsoa4sADgcsEbmCjhLeq0uUesIgAA%3D%3D)  

![315dfe18a31592a92910909b4b78571c.jpeg](http://docmind-api-cn-hangzhou.oss-cn-hangzhou.aliyuncs.com/1617315274244978/publicDocStreamStructure/docmind-20260519-672fb26ef598441da7a1ea2e8ee2ae02/28.png?Expires=1779206878&OSSAccessKeyId=STS.NZebDGdcxohmUjCQd3QTqZtgp&Signature=zlLNed4d%2FUajUUk2Gfvksj8O4jc%3D&x-oss-process=image%2Fcrop%2Cx_1024%2Cy_562%2Cw_176%2Ch_72&security-token=CAIS1wJ1q6Ft5B2yfSjIr5nQKf7zibxZ2KqGV0zytWRmXdtdtbHMkjz2IHhMeHVhCe4Ytfs1nmxX7voZlrp6SJtIXleCZtF94oxN9h2gb4fb4xRsN1SI08%2FLI3OaLjKm9u2wCryLYbGwU%2FOpbE%2B%2B5U0X6LDmdDKkckW4OJmS8%2FBOZcgWWQ%2FKBlgvRq0hRG1YpdQdKGHaONu0LxfumRCwNkdzvRdmgm4NgsbWgO%2Fks0CP0AahlLBL996veMb%2FNfMBZskvD42Hu8VtbbfE3SJq7BxHybx7lqQs%2B02c5onBXwgBvUvdbLCOroI3cFRjFKk2A%2BtIq%2FP5lPt0%2F%2FTajZ%2F6jkwVZ7wQSz7YVABLAzk41i3D3L8ZAlWbUxylurjnXhJFq5mGrt21HrfraghQy27xNG29hwvQXkuNkr7knEkN5aYL3t8Y37R7YXuKmfjOEzylJ9M9udm4napgBytAGoABil%2Fqf5MVplUu7%2BU4BxuSUkUaa02SKOYDC8avK6WNdtkYn0D%2BXqfl9bU8xbeXPrci2hscIAZ0%2BX8aXvgTYjydQRSQKMCg%2FHjlv%2B9b3hANppoB06dPBtIIG3M0IRS%2Bxt1mARqgcjJ60wjWc0nO7Tsoa4sADgcsEbmCjhLeq0uUesIgAA%3D%3D)  

>图1-26 交通流量监测系统  

(3)城市应急联动。共享应急救助资源，增强应急指挥调度协同能力，形成统一指挥、反应灵敏、运转高效的应急联动体系，提高城市应急处置水平。  

# 第2章信息系统集成及服务管理  

## 2.1信息系统集成及服务管理体系  

自1993年以来，在我国多年发展信息产业、推广信息技术应用的基础上，开始全面启动国民经济和社会信息化建设。随着信息技术的飞速发展，信息系统也越来越深入到社会各阶层。这些年来我国在信息系统建设和信息产业发展方面也相应取得了巨大成绩，积累了宝贵经验，主流是健康的。但是，信息系统建设随后也陆续暴露出各种问题，虽然不是主流，但也不容忽视。随着我国信息化建设的逐步推进，对信息系统集成及服务的引导和管理，逐渐形成了我国自有的信息系统集成及服务管理体系。  

### 2.1.1信息系统集成及服务管理的内容  

信息系统集成及服务是一个范围相当广泛的概念，所有以满足企业和机构的业务发展所带来的信息化需求为目的，基于信息技术和信息化理念而提供的专业信息技术咨询服务、系统集成服务、技术支持服务、运行维护服务等工作，都属于信息系统集成及服务的范畴。其中信息技术咨询服务是信息系统集成及服务的前端环节，为企业提供信息化建设规划和解决方案。而根据信息化建设方案选择合适的软硬件产品搭建信息化平台，根据企业的业务流程和管理要求进行软件和应用开发，以及系统建成后的长期维护和升级换代等，属于信息系统集成及服务的中间及下游环节，是信息系统集成及服务在不同时期、不同阶段的具体表现，覆盖了各行各业信息化建设的全过程。  

在我国的信息化建设过程中，信息系统集成及服务存在诸多问题，普遍存在的主要问题如下：  

(1)系统质量不能满足应用的基本需求；  

(2)工程进度拖后延期；  

(3)项目资金使用不合理或严重超出预算；  

(4)项目文档不全甚至严重缺失；  

(5)在项目实施过程中系统业务需求一变再变；  

(6)在项目实施过程中经常出现扯皮、推诿现象；  

(7)系统存在着安全漏洞和隐患；  

(8)重硬件轻软件，重开发轻维护，重建设轻应用；  

(9)信息系统服务企业缺乏规范的流程和能力管理；  

(10)信息系统建设普遍存在产品化与个性化需求的矛盾；  

(11)开放性要求高，而标准和规范更新快。  

这些问题严重阻碍着信息化建设进程，存在重复建设和资金浪费的现象，甚至产生了令人痛心的豆腐渣工程。有些项目，虽然资金投入了，系统却没有建起来：或者，虽然系统建立了，却不能发挥信息系统应有的作用，等等。于是导致投资见不到效果，见不到效益，使国家和用户单位蒙受极大经济损失。  

究其原因，自然要具体问题具体分析，而且不同项目之间也往往存在着差异，但概括起来，主要有以下5点：  

(1)不具备技术实力的系统集成商搅乱信息系统集成及服务市场；  

(2)一些建设单位在选择项目承建商和进行业务需求分析方面经验不足；  

(3)信息系统集成及服务企业自身建设有待加强；  

(4)缺乏相应的机制和制度；  

(5)企业能力建设缺乏相关的指导标准。  

我国信息产业与信息化建设的主管部门和领导机构，在积极推进信息化建设的过程中对所产生的问题予以密切关注并且逐步采取了有效措施，各省、自治区、直辖市、计划单列市等地方政府的信息产业及信息化主管部门也积极参与并且发挥创造性，进行了有益的探索。  

为了保证信息系统工程项目投资、质量、进度及效果各方面处于良好的可控状态，在针对出现的问题不断采取相应措施的探索过程中，逐步形成了中国特色的信息系统集成及服务管理体系，主要内容如下：  

(1)信息系统集成、运维服务和信息系统监理资质管理；  

(2)信息系统集成、运维服务和信息系统监理相关人员管理；  

(3)国家计划(投资)部门对规范的、具备信息系统项目管理能力的企业和人员的建议性要求；  

(4)信息系统用户对规范的、具备信息系统项目管理能力的企业和人员市场性需求。  

在市场经济条件下，政府主管部门的作用是加强"引导、规范、监管、服务"，而信息系统集成及服务工程的突出特点是投资和风险都很巨大，因此政府主管部门对其进行合理规范与监管显得尤为重要。但是，我们也清醒地认识到这些制度需要与时俱进，同时也要考虑发挥市场经济中市场的力量，因此，研究与探讨国际上IT治理与管理的先进经验，规范信息化建设市场的秩序，保证信息系统集成及服务工程的质量，降低风险，提高信息系统集成及服务的效率与效益，培育高素质的中介服务机构和从业人员，是加快推进我国信息化建设步伐的一项重要工作。政府主管部门也在不断探索，逐步引入和推行如信息技术服务标准(ITSS)评估、IT服务管理体系(ITSMS) 认证、信息安全管理体系(ISMS)认证、IT审计、IT治理等制度。  

110  

## 2.1.2信息系统集成及服务管理的推进  

我国信息系统集成及服务管理体系的形成，可以说是在解决问题的过程中逐步推进产生的，在此，介绍一下我国现行几种信息系统集成及服务管理内容的形成和推进过程。  

### 1.实施信息系统集成及服务资质管理制度  

#### 1)推荐优秀系统集成商  

针对1993年以后开展"金"系列工程中出现的少数单位鱼目混珠、搅乱信息系统集成市场的问题，1996年7月，由原电子工业部"金"系列工程办公室主办，中国软件评测中心承办，开展了"全国优秀系统集成商推荐活动"。此次共评选出内资优秀系统集成企业、外资优秀系统集成企业、技术最强系统集成企业、最佳增值服务系统集成企业、最受用户欢迎系统集成企业、最佳经营系统集成企业、最佳售后服务系统集成企业七大类40家优秀系统集成企业，共收集这些公司及另外一些公司的系统集成案例125个。这次活动架起了企业和用户之间的桥梁，为信息系统的建设单位选择承建商创造了条件，为产业主管部门制订相关政策提供了参考依据，也为后来开展信息系统集成及服务资质认证工作积累了经验。  

#### 2)对信息系统集成企业进行资质认证  

1998年原信息产业部成立后，便开始酝酿推行信息系统集成资质认证制度，并将其列为1999年重点工作之一。经过将近一年的调查研究、文件起草等筹备过程，1999年11月原信息产业部发出了《计算机信息系统集成资质管理办法(试行)》(信部规[1999]1047号文，以下简称1047号文)，决定从2000年1月1日起实施计算机信息系统集成资质认证制度。1047号文明确界定：计算机信息系统集成是指从事计算机应用系统工程和网络系统工程的总体策划、设计、开发、实施、服务及保障；计算机信息系统集成的资质是指从事计算机信息系统集成的综合能力，包括技术水平、管理水平、服务水平、质量保证能力、技术装备、系统建设质量、人员构成与素质、经营业绩、资产状况等要素；计算机信息系统集成资质等级从高到低依次为一、 二、三、四级。  

与此同时，《计算机信息系统集成资质等级评定条件(试行)》也已完成起草工作，并且在首批申请资质的21个企业中试行，经修改后于2000年9月发布《关于发布计算机信息系统集成资质等级评定条件的通知》(信部规[2000]821号文， 以下简称821号文)。  

经过3年多的系统集成资质认证评审实践，证明821号文所发布的等级条件是切实可行的。但是，随着计算机信息系统集成事业的不断发展和计算机信息系统集成企业综合能力的不断提高，需要对821号文规定的等级条件进行相应调整。为此，原信息产业部于2003年10月颁布了《关于发布计算机信息系统集成资质等级评定条件(修订版)的通知》(参见信部规[2003]440号文，以下简称440号文)。  

为完善计算机信息系统集成企业资质管理工作，进一步规范信息系统集成行业，促进市场健康和良性发展，推动软件和信息技术服务业做大做强，工业和信息化部计算机信息系统集成资质认证工作办公室对原信息产业部《计算机信息系统集成资质等级评定条件(修定版)》(信部规[2003]440号)再次进行了修订，2012年5月，颁布了《计算机信息系统集成企业资质等级评定条件(2012年修定版)》(工信计资[2012]6号)，同时出台的还有《计算机信息系统集成企业资质等级评定条件实施细则》。  

随着《国务院关于取消和下放一批行政审批项目的决定》(国发〔2014)5号)的发布，为充分发挥市场机制的作用，进一步调动企业积极性，有效行使政府行业监管职能，进一步提高信息技术服务能力和水平，计算机信息系统集成企业资质等信息技术服务资质资格认定由相关行业组织自律管理，行业主管部门做好事中事后监管工作。工业和信息化部自2014年2月15日起，停止计算机信息系统集成企业和人员资质认定行政审批，信息系统集成及服务资质认定工作由中国电子信息行业联合会负责实施。各省、自治区、直辖市及计划单列市、新疆生产建设兵团工业和信息化主管部门也停止资质认定行政审批相关工作。  

自2000年9月11日公布首批获得计算机信息系统集成资质证书名单(共21家企业)开始，2015年7月该证书更名为信息系统集成及服务资质证书，至2015年12月止，已有6157家企业获得信息系统集成及服务资质证书，其中：一级251家：二级706家：三级3469家；四级1731家。  

信息系统集成及服务资质认证工作开展以来，成绩显著，影响巨大，主要表现在以下几个方面。  

(1)认证工作及结果被各级政府和社会各界广泛认同，例如：  

2000年12月28日发布的北京市人民政府令(第67号)第十条规定："未经资质认证的单位，不得承揽或者以其他单位名义承揽信息化工程"；第十一条规定："建设单位不得将信息化工程项目发包给不具备相关资质等级的单位"。  

2001年9月12日国家保密局发出的《关于印发(涉及国家秘密的计算机信息系统集成资质管理办法(试行))的通知》中，把"具有信息产业部颁发的《计算机信息系统集成资质证书》(一级或二级)"作为"涉密系统集成单位"的必要条件。  

2002年9月18日《国务院办公厅转发国务院信息化工作办公室关于振兴软件产业行动纲要的通知》(国办发[2002]47 号文)要求：认真贯彻执行《振兴软件产业行动纲要》。在该行动纲要中要求："对国家重大信息化工程实行招标制、工程监理制，承担单位实行资质认证"；而且，行动纲要明确规定："利用财政性资金建设的信息化工程，用于购买软件产品和服务的资金原则上不得低于总投资的30%"。这就进一步加大了信息产业部信部规[2000]821号文中关于信息系统集成项目中关于"软件费用应占工程项目总值的30%以上"这一要求的贯彻力度。  

现在，企业的信息系统集成及服务资质已成为信息系统建设单位在选择承建商时的重要依据，或者说成为系统集成商承揽信息系统工程特别是重大信息系统工程的必要条件。  

112  

(2)资质认证过程中要对企业的软件开发和系统集成的人员队伍、环境设备、质保体系、客服体系、培训体系、软件成果及所占比例、注册资本及财务状况、营业规模及业绩、项目质量、单位信誉等各方面进行严格审查，还要进行每年一次年度数据填报和每四年进行一次换证等检查。这一方面使系统集成企业受到严格的社会监督，另一方面也使得企业的综合实力和素质有了显著提高。  

(3)有效地规范了信息系统集成市场，使皮包商钻空子和搅乱市场秩序的状况得到控制。  

(4)信息系统工程质量显著提高。  

(5)对于广大用户为支持软件与系统集成业发展创造良好环境起到引导作用。例如，过去普遍重视硬件轻视软件，现在逐步提高了对软件价值、系统集成价值和运行维护价值的认识。  

#### 2.推行项目经理制度  

信息系统建设等都是以项目的形式提供服务。信息系统的建设单位，不仅关心信息系统承建商的资质等级，还关心企业最终委派哪些人投入到该项目，特别是由哪一位出任项目经理。如果项目经理不够格，用户还是难于对该项目的完成建立信心，当然也难于对承建单位放心满意。所以，实行项目经理制是系统集成及服务资质认证深入开展的必然结果，是保证信息系统工程质量的必要措施。  

为此，信息产业部从2001年初就开始实施计算机信息系统集成项目经理制进行调研和相关文件起草的工作。在此过程中得到了社会各界特别是广大信息系统集成企业的大力支持。  

2002年8月28日，信息产业部发出《关于发布<计算机信息系统集成项目经理资质管理办法(试行)>的通知》(信部规[2002]382号文)(以下简称为《项目经理管理办法》)，决定在计算机信息系统集成行业推行项目经理制度。  

●《项目经理管理办法》首先界定了此处所指的项目经理的含义，指出：计算机信息系统集成项目经理是指从事计算机信息系统集成业务的企、事业单位法定代表人在计算机信息系统集成项目中的代表人，是受系统集成企、事业单位法定代表人委托对系统集成项目全面负责的项目管理者。  

·《项目经理管理办法》将系统集成项目经理分为项目经理、高级项目经理两个级别，并且分别列出了这两个级别的评定条件。  

《项目经理管理办法》对系统集成项目经理的职责和职业范围提出了明确要求，对其资质的申请及审批流程做出了明确规定，并且就系统集成项目经理的监督管理做出了较为详细的具体规定。  

2015年7月由中国电子信息行业联合会发布《信息系统集成及服务项目管理人员登记管理办法(暂行)》对项目经理和高级项目经理实施企业聘任制度。  

截止2015年12月止，已有40010 人获得系统集成项目经理资质证书，14194 人获得系统集成高级项目经理资质证书。  

#### 3.推出ITSS标准及评估服务  

2009年4月15日，国务院正式发布《电子信息产业调整和振兴规划》(以下简称：规划)，在强化自主创新能力建设方面明确提出"加快制定信息技术服务标准和规范"。为了贯彻落实规划要求，2009年4月23日，工业和信息化部软件服务业司成立了信息技术服务标准工作组(以下简称：工作组)，负责研究并建立信息技术服务标准体系，制定信息技术服务领域的相关标准，彻底改变信息系统服务领域标准缺乏，概念混乱，业务划分不清的问题。并按照信息服务生命周期推出一套完整的IT服务标准体系 ITSS(Information Technology Service Standards， 信息技术服务标准)，包含了IT服务的规划设计、部署实施、服务运营、持续改进和监督管理等全生命周期阶段应遵循的标准，涉及信息系统建设、运行维护、服务管理、治理及外包等业务领域，是一套体系化的信息技术服务标准库。  

2012年首先推出《信息技术服务分类与代码》(GB/T29264-2012)； 《信息技术服务运行维护第1部分：通用要求》(GB/T28827.1-2012)；《信息技术服务运行维护第2部分：交付规范》(GB/T28827.2-2012)； 《信息技术服务运行维护第3部分：应急响应规范》(GB/T28827.3-2012)，并于2013年6月由"中国电子工业标准化技术协会信息技术服务分会"发布18家第一批通过《信息技术服务运行维护第1部分：通用要求》(GB/T28827.1-2012)符合性评估的企业。  

为进一步推动运维企业管理水平的提高，基于《信息技术服务运行维护第1部分：通用要求》(GB/T28827.1-2012)； 《信息技术服务运行维护第2部分：交付规范》(GB/T28827.2-2012)； 《信息技术服务运行维护第3部分：应急响应规范》(GB/T28827.3-2012)，于2014年2月由"中国电子工业标准化技术协会信息技术服务分会"发布《信息技术服务运行维护服务能力成熟度模型》ITSS.1-2015。该模型把运维企业按照成熟度分为四级，一级最高，四级最低。截止到2015年12月通过运维标准符合性评估单位323家(其中用户单位5家)。  

## 2.2信息系统集成及服务资质管理  

### 2.2.1信息系统集成及服务资质管理的必要性和意义  

这些年系统集成及服务业的发展主流是健康的。但是，也确实存在着一些问题，不容忽视。首先，一个重要问题是用户在选择集成商的时候缺少依据和标准，特别是在重大项目招标和实施过程中，缺少必要的监督、检查；此外，有些重大工程项目中的一些流程，包括软件、程序、存档材料，缺少标准，也比较乱，也给项目中软件升级方面造成不少困难。第二个问题是：由于国家信息系统工程建设要求参与竞标的企业有资质和业绩，而我们当时还没有给企业确认资质等级，所以相当多的企业在参与国际竞争中有困难。第三个问题是：少数不具备承建信息系统工程能力的单位甚至个人，搅乱市场秩序，破坏"游戏规则"， 通过各种各样关系，采用不正当手段，拿到了项目，又不能很好完成这些项目，信息工程完成之日，也是这个项目死亡之时，没有很好发挥作用，为国家和用户部门造成极大经济损失，产生了很坏的社会影响。一些地区和行业主管部门陆续向我们反映这样的情况，已经引起了当时的电子工业部的领导同志的重视，认识到开展计算机信息系统集成企业资质认证工作确实是迫在眉睫，势在必行。1996年7月，.由当时的电子工业部计算机与信息化推进司暨金系列工程办公室主办，中国软件评测中心承办，开展了"全国优秀系统集成商评选推荐活动"。这次共评选出技术最强系统集成企业、最佳增值服务系统集成企业等七大类40家优秀系统集成企业，共收集系统集成案例125个。应该说这次活动为企业和用户之间架起了一个桥梁，为日后信息系统相关政策制定提供了参考依据，为信息系统的主建单位选择承建单位创造了条件，是为日后开展计算机信息系统集成企业资质认证工作进行的有益探索。1998 年信息产业部一成立，便将信息系统企业资质认证列入正式工作日程，并组织有关单位，做了大量调查研究和各项准备工作，于1999年11月份发出了《计算机信息系统集成资质管理办法(试行)》(信部规[1999]1047号文件)，决定从2000年1月1日起开始做试点工作。资质认证工作至少有如下意义：  

114  

![7fa15773134ed6754a63fd35c512148e.jpeg](http://docmind-api-cn-hangzhou.oss-cn-hangzhou.aliyuncs.com/1617315274244978/publicDocStreamStructure/docmind-20260519-672fb26ef598441da7a1ea2e8ee2ae02/35.png?Expires=1779206880&OSSAccessKeyId=STS.NZebDGdcxohmUjCQd3QTqZtgp&Signature=J5IGMIbaNn37UD0twvEfLF1UV3E%3D&x-oss-process=image%2Fcrop%2Cx_0%2Cy_1%2Cw_1230%2Ch_108&security-token=CAIS1wJ1q6Ft5B2yfSjIr5nQKf7zibxZ2KqGV0zytWRmXdtdtbHMkjz2IHhMeHVhCe4Ytfs1nmxX7voZlrp6SJtIXleCZtF94oxN9h2gb4fb4xRsN1SI08%2FLI3OaLjKm9u2wCryLYbGwU%2FOpbE%2B%2B5U0X6LDmdDKkckW4OJmS8%2FBOZcgWWQ%2FKBlgvRq0hRG1YpdQdKGHaONu0LxfumRCwNkdzvRdmgm4NgsbWgO%2Fks0CP0AahlLBL996veMb%2FNfMBZskvD42Hu8VtbbfE3SJq7BxHybx7lqQs%2B02c5onBXwgBvUvdbLCOroI3cFRjFKk2A%2BtIq%2FP5lPt0%2F%2FTajZ%2F6jkwVZ7wQSz7YVABLAzk41i3D3L8ZAlWbUxylurjnXhJFq5mGrt21HrfraghQy27xNG29hwvQXkuNkr7knEkN5aYL3t8Y37R7YXuKmfjOEzylJ9M9udm4napgBytAGoABil%2Fqf5MVplUu7%2BU4BxuSUkUaa02SKOYDC8avK6WNdtkYn0D%2BXqfl9bU8xbeXPrci2hscIAZ0%2BX8aXvgTYjydQRSQKMCg%2FHjlv%2B9b3hANppoB06dPBtIIG3M0IRS%2Bxt1mARqgcjJ60wjWc0nO7Tsoa4sADgcsEbmCjhLeq0uUesIgAA%3D%3D)  

(1)有利于系统集成及服务企业展示自身实力，参与市场竞争；按照等级条件，加强自身建设。  

(2)有利于规范信息系统集成及服务市场。  

(3)有利于保证信息系统及服务工程质量。  

### 2.2.2信息系统集成及服务资质管理办法  

中国电子信息行业联合会(以下简称电子联合会)根据国务院关于标准化改革工作的有关要求，组织制定了《信息系统集成及服务资质认定管理办法(暂行)》，自2015年7月1日起实行，管理办法分为7章，分别为总则，工作机构，资质设定，资质申请与认定，资质证书管理，监督管理及投诉、申诉和罚则，附则。  

#### 1.工作机构  

电子联合会设立信息系统集成资质工作委员会(以下称电子联合会资质工作委员会)，负责协调、管理资质认定工作，对资质认定结果进行审定。电子联合会资质工作委员会下设信息系统集成资质工作办公室(以下称电子联合会资质办)作为电子联合会资质工作委员会的日常办事机构，负责具体组织实施资质认定工作。根据资质认定工作的需要，电子联合会资质办可在获证企业数量较多或有必要的地区设立地方信息系统集成资质服务中心(以下称地方服务中心)。地方服务中心依照电子联合会资质办的委托在本地区开展资质认定服务工作。信息系统集成资质评审机构(以下称评审机构)负责在电子联合会资质办认定的范围内开展资质评审工作，包括对资质申报材料的完整性、真实性、有效性及与资质等级评定条件的符合性等方面进行独立审核，并出具评审报告。评审机构分为A级和B级。A级评审机构可在全国各地区开展资质评审工作。B级评审机构可在本地区开展资质评审工作。为确保评审机构的评审工作公平、公正，并提升评审工作质量，电子联合会资质办可委托见证机构对评审机构的现场评审过程进行见证，并出具见证报告。  

#### 2.资质设定  

信息系统集成及服务资质是对企业从事信息系统集成及服务综合能力和水平的客观评价，集成资质分为一级、二级、三级和四级四个等级，其中一级最高。为适应信息技术发展和市场的需求，电子联合会将适时开展针对信息系统集成及服务不同环节设定的分项资质及针对市场特定需要而专门设定的专项资质的认定工作。分项资质和专项资质的认定，原则上遵守本办法的相关规定，具体管理办法和资质等级评定条件由电子联合会另行制定发布。电子联合会对信息系统集成项目管理人员(以下称项目管理人员)实施登记管理。  

#### 3.资质申请与认定  

凡从事信息系统集成及服务的企业，可根据电子联合会发布的资质等级评定条件和自身能力水平情况，自愿申请相应类别和级别的资质认定。资质认定根据评审与审定分离的原则，按照先由评审机构评审，再由电子联合会审定的程序进行。资质认定分为新申报和换证申报，除特别规定的事项外，新申报和换证申报的评定条件及认定程序相同。  

申请资质认定的企业(以下称申请企业)应具备下列基本条件：  

(1)是在中华人民共和国境内注册的企业法人；  

(2)能够提供与资质等级评定条件相关的证明材料；  

(3)承诺并遵守行业公约，并认同《信息系统集成及服务资质认定管理办法(暂行)》。资质认定程序如下：  

(1)申请企业自主选择符合条件的评审机构并向其提交申报材料。其中，申请一级、二级集成资质的企业应向A级评审机构提交申报材料，申请三级、四级集成资质的企业可向注册所在地的B级评审机构提交申报材料，或向A级评审机构提交申报材料。  

(2)评审机构接收申报材料后，组织实施文件评审和现场评审并出具评审报告。其中，一级、二级集成资质的现场评审， 应由见证机构进行见证并出具见证报告。  

(3)评审机构在出具同意意见的评审报告后，将申请企业的申报材料和评审报告提交至电子联合会资质办或申请企业注册所在地的地方服务中心。  

(4)电子联合会资质办审查申报材料和评审报告，并组织召开资质评审会。对通过评审会的集成一级、二级资质新申报企业，电子联合会资质办在工作网站公示10天。  

(5)电子联合会资质办将资质评审会及公示结果报电子联合会资质工作委员会审定，并向通过审定的企业颁发资质证书。  

![9ebdd10c677baa0eacbd72dc62d31101.jpeg](http://docmind-api-cn-hangzhou.oss-cn-hangzhou.aliyuncs.com/1617315274244978/publicDocStreamStructure/docmind-20260519-672fb26ef598441da7a1ea2e8ee2ae02/37.png?Expires=1779206880&OSSAccessKeyId=STS.NZebDGdcxohmUjCQd3QTqZtgp&Signature=l%2FgL%2FHRqEbmxHO6hJbh29XgYjS0%3D&x-oss-process=image%2Fcrop%2Cx_18%2Cy_4%2Cw_1295%2Ch_121&security-token=CAIS1wJ1q6Ft5B2yfSjIr5nQKf7zibxZ2KqGV0zytWRmXdtdtbHMkjz2IHhMeHVhCe4Ytfs1nmxX7voZlrp6SJtIXleCZtF94oxN9h2gb4fb4xRsN1SI08%2FLI3OaLjKm9u2wCryLYbGwU%2FOpbE%2B%2B5U0X6LDmdDKkckW4OJmS8%2FBOZcgWWQ%2FKBlgvRq0hRG1YpdQdKGHaONu0LxfumRCwNkdzvRdmgm4NgsbWgO%2Fks0CP0AahlLBL996veMb%2FNfMBZskvD42Hu8VtbbfE3SJq7BxHybx7lqQs%2B02c5onBXwgBvUvdbLCOroI3cFRjFKk2A%2BtIq%2FP5lPt0%2F%2FTajZ%2F6jkwVZ7wQSz7YVABLAzk41i3D3L8ZAlWbUxylurjnXhJFq5mGrt21HrfraghQy27xNG29hwvQXkuNkr7knEkN5aYL3t8Y37R7YXuKmfjOEzylJ9M9udm4napgBytAGoABil%2Fqf5MVplUu7%2BU4BxuSUkUaa02SKOYDC8avK6WNdtkYn0D%2BXqfl9bU8xbeXPrci2hscIAZ0%2BX8aXvgTYjydQRSQKMCg%2FHjlv%2B9b3hANppoB06dPBtIIG3M0IRS%2Bxt1mARqgcjJ60wjWc0nO7Tsoa4sADgcsEbmCjhLeq0uUesIgAA%3D%3D)  

系统集成项目管理工程师教程(第2版)  

#### 4.资质证书管理  

资质证书有效期四年，分为正本和副本，正本和副本具有同等效力。在资质证书有效期内，持证企业每年应按时向电子联合会资质办提交年度数据信息，不能按时提交年度数据信息的企业，视为其自动放弃资质证书。在资质证书有效期期满前，持证企业应按时完成换证申报认定，未按时完成换证申报认定的企业，其资质证书视为自动失效。持证企业资质证书记载事项发生变更的，应在变更发生后30日内，向电子联合会资质办或注册所在地的地方服务中心提交资质证书变更申请材料，电子联合会资质办核实无误后，换发资质证书。持证企业遗失资质证书，应按电子联合会资质办要求发布遗失声明后，向电子联合会资质办或注册所在地的地方服务中心提交资质证书遗失补发申请，电子联合会资质办核实无误后，补发资质证书。  

### 2.2.3信息系统集成资质等级条件  

根据国务院关于标准化改革工作的有关要求，电子联合会组织制定了《信息系统集成资质等级评定条件(暂行)》， 自2015年7月1日起实行。系统集成资质等级评定条件主要由综合条件、财务状况、信誉、业绩、管理能力、技术实力、人才实力7个方面描述的。  

#### 1.综合条件  

综合条件从企业的从业年限、获取低一级资质年数、主业是否为系统集成、注册资金等基本情况来衡量。注册资金数目在一定程度上反映了企业的经济实力和承担风险的能力。不同级别要求注册资金大小的差异，表明高级别资质能力更强。  

#### 2.财务状况  

系统集成企业要求财务状况良好。如果企业近三年中连续两年亏损，或虽只有一年亏损，但亏损额较大则反映其财务状况不佳。  

注意，企业的财务状况应由有资质的审计机构提供的财务数据说明，或以其他方式证明企业所提供的财务数据是可信的。  

#### 3.信誉  

企业必须从提高自身的综合实力和提高对客户的服务水平及效果上下功夫以提高并保持其信誉度。  

企业必须重视来自客户的意见反馈。只要有客户投诉，就应该认真调查。  

#### 4.业绩  

业绩要求主要从企业近三年完成的系统集成项目额、项目规模、项目的技术含量、项目的软件费用比例、项目的实施质量、企业所完成项目在主要业务领域的水平等方面衡量。  

不同级别的主要差别，不仅体现在其项目的数量上，而且也体现在项目的规模、技术含量、完成的质量上。  

请注意，此处要求一定是"完成"了的项目才能计入业绩，不包括正在进行中的项目。也就是说，经过建设单位签字、验收了的项目才算完成，这也表明建设单位对项目质量的认可。  

5.管理能力  

管理能力要求主要从质量管理、客户服务、企业的信息管理系统、企业负责人以及技术、财务负责人等方面能力衡量。  

1)质量管理体系  

对不同级别的系统集成企业都要求建立有质量管理体系并能有效实施。对高级资质还要求要通过第三方认证机构的认证，且不同级别还从取得认证的时间上有不同的要求。  

注意，条件中要求有效实施是指：  

①企业在运作过程中严格执行单位制度文件和质量体系文件。  

②有详细完整的实施记录。  

③有可视化的实施效果。  

#### 2)客户服务管理  

对不同级别的系统集成企业要求建立有客户服务制度，并配备专门客服部门和客服人员。越高级别要求越高。  

#### 6.技术实力  

各级别的技术实力要求主要从企业在某些业务领域的实力、软件研发能力、开发环境、研发投入等方面衡量。  

##### 1)业务领域  

对不同级别的系统集成企业都要求有明确或主要的业务领域，而且在主要的业务领域上技术实力、市场占有率有不同的要求。  

2)软件开发能力  

主要从企业自主开发的软件平台、软件产品的情况衡量，同时也要求所开发的软件应应用到系统集成项目上。同时开发能力也体现在开发环境和研发投入费用上。  

7.人才实力  

各级别的人才实力要求主要从工程技术人员、本科以上人员比例、项目经理数目、培训体系和人力资源管理水平等方面衡量。  

项目经理数量是最能体现企业对系统集成项目实施和管理能力的指标。  

## 2.3ITIL与IT服务管理、ITSS与信息技术服务、信息系统审计  

### 2.3.1  ITIL与IT服务管理  

#### 1.ITIL的概念及其发展  

1) ITIL概念  

ITIL的全称是Information Technology Infrastructure Library(信息技术基础架构库)，是CCTA(英国国家计算机和电信局)于20世纪80年代末开发的一套IT服务管理规范库。  

118  

![59c60375009c55308cba0ca475ee90cf.jpeg](http://docmind-api-cn-hangzhou.oss-cn-hangzhou.aliyuncs.com/1617315274244978/publicDocStreamStructure/docmind-20260519-672fb26ef598441da7a1ea2e8ee2ae02/39.png?Expires=1779206879&OSSAccessKeyId=STS.NZebDGdcxohmUjCQd3QTqZtgp&Signature=xqqFyhu3OiMcEJRsSa5iirFv2qY%3D&x-oss-process=image%2Fcrop%2Cx_93%2Cy_9%2Cw_1063%2Ch_108&security-token=CAIS1wJ1q6Ft5B2yfSjIr5nQKf7zibxZ2KqGV0zytWRmXdtdtbHMkjz2IHhMeHVhCe4Ytfs1nmxX7voZlrp6SJtIXleCZtF94oxN9h2gb4fb4xRsN1SI08%2FLI3OaLjKm9u2wCryLYbGwU%2FOpbE%2B%2B5U0X6LDmdDKkckW4OJmS8%2FBOZcgWWQ%2FKBlgvRq0hRG1YpdQdKGHaONu0LxfumRCwNkdzvRdmgm4NgsbWgO%2Fks0CP0AahlLBL996veMb%2FNfMBZskvD42Hu8VtbbfE3SJq7BxHybx7lqQs%2B02c5onBXwgBvUvdbLCOroI3cFRjFKk2A%2BtIq%2FP5lPt0%2F%2FTajZ%2F6jkwVZ7wQSz7YVABLAzk41i3D3L8ZAlWbUxylurjnXhJFq5mGrt21HrfraghQy27xNG29hwvQXkuNkr7knEkN5aYL3t8Y37R7YXuKmfjOEzylJ9M9udm4napgBytAGoABil%2Fqf5MVplUu7%2BU4BxuSUkUaa02SKOYDC8avK6WNdtkYn0D%2BXqfl9bU8xbeXPrci2hscIAZ0%2BX8aXvgTYjydQRSQKMCg%2FHjlv%2B9b3hANppoB06dPBtIIG3M0IRS%2Bxt1mARqgcjJ60wjWc0nO7Tsoa4sADgcsEbmCjhLeq0uUesIgAA%3D%3D)  

ITIL最初是为了提高英国政府部门IT服务质量而开发，但它很快在英国的各个企业中得到了广泛的应用和认可。随之ITIL把英国各个行业在IT管理方面的最佳实践归纳起来形成规范，旨在提高IT资源的利用率和服务质量。目前ITIL已经成为业界通用的事实标准，是目前业界普遍采用的一系类IT服务管理的实际标准及最佳实践指南。  

ITIL包含着如何管理IT基础设施的流程描述，以流程为向导、以客户为中心，通过整合IT服务与企业服务，提高企业的IT服务提供和服务支持的能力和水平。  

##### 2)ITIL的发展  

ITIL到目前为止，已经经历了3个主要版本：  

(1)V1：1989~1995年出版，包含31本书，内容覆盖IT服务提供的所有方面。  

(2)V2：2000~2004年出版，共有7本书，包含服务支持、服务提供、实施服务管理规划、应用管理、安全管理、基础架构管理及ITIL的业务前景7个体系。  

(3)V3：2007年出版，提出IT服务生命周期概念，整合了V1和V2的精华，融入了IT服务管理领域当前的最佳实践。V3的核心为5本书(服务战略、服务设计、服务转换、服务运营、服务持续改进)， 强调ITIL最佳实践的执行支持，以及在改进过程中需要注意的细节。  

(4)ITIL 2011：为V3的更新版本，不是全新改版，更新版纠正了一些错误，更新了一些术语，阐述了整个服务生命周期中各生命周期间的接口及输入输出，提升了内容的清晰程度和整体知识结构。  

#### 2.IT服务管理(ITSM)  

ITSM (IT Service Management， IT服务管理)起源于ITIL，其结合了高质量服务不可缺少的过程、人员和技术这三大要素，通过集成IT服务和业务，协助企业提高其IT服务提供和支持能力，能够帮助企业对IT系统的规划、研发、实施和运营进行有效管理。  

基于不同的出发点和侧重点，人们提出了各种各样的有关IT服务管理的定义。国际IT领域的权威研究机构高德纳(Gartner)认为， ITSM是一套通过服务级别协议(SLA)来保证IT服务质量的协同流程，它融合了系统管理、网络管理、系统开发管理等管理活动和变更管理、资产管理、问题管理等许多流程的理论和实践。而ITSM领域的国际权威组织itSMF则认为ITSM是一种以流程为导向、以客户为中心的方法，它通过整合IT服务与组织业务，提高组织在IT服务提供和服务支持方面的能力及其水平。  

##### 1)ITSM的核心思想  

ITSM的核心思想是，IT组织，不管它是企业内部的还是外部的，都是IT服务提供者，其主要工作就是提供低成本、高质量的IT服务。而IT服务的质量和成本则需从IT服务的客户(购买IT服务的) 和用户 (使用IT服务的)方加以判断。ITSM也是一种IT管理。不过与传统的IT管理不同，它是一种以服务为中心的IT管理。  

我们也可以形象地把ITSM称作是IT管理的"ERP解决方案"。从组织层面上来看，它将企业的IT部门从成本中心转化为服务中心和利润中心；从具体IT运营层面上来看，它不是传统的以职能为中心的IT管理方式，而是以流程为中心，从复杂的IT管理活动中梳理出那些核心的流程，比如事件管理、问题管理和配置管理，将这些流程规范化、标准化，明确定义各个流程的目标和范围、成本和效益、运营步骤、关键成功因素和绩效指标、有关人员的责权利，以及各个流程之间的关系。  

###### 实施ITSM的根本目标有以下三个。  

(1)以客户为中心提供IT服务。  

(2)提供高质量、低成本的服务。  

(3)提供的服务是可准确计价的。  

##### 2)ITSM的基本原理  

ITSM的基本原理可简单地用"二次转换"来概括，第一次是"梳理"，第二次是"打包"，如图2-1所示。  

IT服务提供方                          IT服务接受方  

![94142fc7eb519724dfed01a30dae8591.jpeg](http://docmind-api-cn-hangzhou.oss-cn-hangzhou.aliyuncs.com/1617315274244978/publicDocStreamStructure/docmind-20260519-672fb26ef598441da7a1ea2e8ee2ae02/40.png?Expires=1779206880&OSSAccessKeyId=STS.NZebDGdcxohmUjCQd3QTqZtgp&Signature=QED0YLCCIowC%2Bj1oWfv0vEflBi8%3D&x-oss-process=image%2Fcrop%2Cx_213%2Cy_938%2Cw_861%2Ch_471&security-token=CAIS1wJ1q6Ft5B2yfSjIr5nQKf7zibxZ2KqGV0zytWRmXdtdtbHMkjz2IHhMeHVhCe4Ytfs1nmxX7voZlrp6SJtIXleCZtF94oxN9h2gb4fb4xRsN1SI08%2FLI3OaLjKm9u2wCryLYbGwU%2FOpbE%2B%2B5U0X6LDmdDKkckW4OJmS8%2FBOZcgWWQ%2FKBlgvRq0hRG1YpdQdKGHaONu0LxfumRCwNkdzvRdmgm4NgsbWgO%2Fks0CP0AahlLBL996veMb%2FNfMBZskvD42Hu8VtbbfE3SJq7BxHybx7lqQs%2B02c5onBXwgBvUvdbLCOroI3cFRjFKk2A%2BtIq%2FP5lPt0%2F%2FTajZ%2F6jkwVZ7wQSz7YVABLAzk41i3D3L8ZAlWbUxylurjnXhJFq5mGrt21HrfraghQy27xNG29hwvQXkuNkr7knEkN5aYL3t8Y37R7YXuKmfjOEzylJ9M9udm4napgBytAGoABil%2Fqf5MVplUu7%2BU4BxuSUkUaa02SKOYDC8avK6WNdtkYn0D%2BXqfl9bU8xbeXPrci2hscIAZ0%2BX8aXvgTYjydQRSQKMCg%2FHjlv%2B9b3hANppoB06dPBtIIG3M0IRS%2Bxt1mARqgcjJ60wjWc0nO7Tsoa4sADgcsEbmCjhLeq0uUesIgAA%3D%3D)  

>图2-1ITSM的基本原理图  

首先，将纵向的各种技术管理工作(这是传统IT管理的重点)，如服务器管理、网络管理和系统软件管理等，进行"梳理"，形成典型的流程， 比如ITIL中的10个流程。这是第一次转换。流程主要是IT服务提供方内部使用的，客户对他们并不感兴趣。仅有这些流程并不能保证服务质量而让客户满意，还需将这些流程按需"打包"成特定的IT服务，然后提供给客户。这是第二次转换。第一次转换将技术管理转化为流程管理，第二次转换将流程管理转化为服务管理。  

120  

![1a41fcb76ebf59a22f1c220d99bb87d8.jpeg](http://docmind-api-cn-hangzhou.oss-cn-hangzhou.aliyuncs.com/1617315274244978/publicDocStreamStructure/docmind-20260519-672fb26ef598441da7a1ea2e8ee2ae02/41.png?Expires=1779206880&OSSAccessKeyId=STS.NZebDGdcxohmUjCQd3QTqZtgp&Signature=ahn4p8Ita4gbjRT6eJpwhUFmMS8%3D&x-oss-process=image%2Fcrop%2Cx_0%2Cy_6%2Cw_1273%2Ch_116&security-token=CAIS1wJ1q6Ft5B2yfSjIr5nQKf7zibxZ2KqGV0zytWRmXdtdtbHMkjz2IHhMeHVhCe4Ytfs1nmxX7voZlrp6SJtIXleCZtF94oxN9h2gb4fb4xRsN1SI08%2FLI3OaLjKm9u2wCryLYbGwU%2FOpbE%2B%2B5U0X6LDmdDKkckW4OJmS8%2FBOZcgWWQ%2FKBlgvRq0hRG1YpdQdKGHaONu0LxfumRCwNkdzvRdmgm4NgsbWgO%2Fks0CP0AahlLBL996veMb%2FNfMBZskvD42Hu8VtbbfE3SJq7BxHybx7lqQs%2B02c5onBXwgBvUvdbLCOroI3cFRjFKk2A%2BtIq%2FP5lPt0%2F%2FTajZ%2F6jkwVZ7wQSz7YVABLAzk41i3D3L8ZAlWbUxylurjnXhJFq5mGrt21HrfraghQy27xNG29hwvQXkuNkr7knEkN5aYL3t8Y37R7YXuKmfjOEzylJ9M9udm4napgBytAGoABil%2Fqf5MVplUu7%2BU4BxuSUkUaa02SKOYDC8avK6WNdtkYn0D%2BXqfl9bU8xbeXPrci2hscIAZ0%2BX8aXvgTYjydQRSQKMCg%2FHjlv%2B9b3hANppoB06dPBtIIG3M0IRS%2Bxt1mARqgcjJ60wjWc0nO7Tsoa4sADgcsEbmCjhLeq0uUesIgAA%3D%3D)  

系统集成项目管理工程师教程(第2版)  

之所以要进行这样的转换，有多方面的原因。从客户的角度说，IT只是其运营业务流程的一种手段，不是目的，需要的是IT所实现的功能；客户没有必要，也不可能对IT有太多的了解，他和IT部门之间的交流，应该使用"商业语言"，而不是"技术语言"， IT技术对客户应该是透明的。为此，我们需要提供IT服务。为了灵活、及时和有效地提供这些IT服务，并保证服务质量、准确计算有关成本，服务提供商就必须事先对服务进行一定程度上的分类和"固化"。流程管理是满足这些要求的一种比较理想的方式。  

#### 3)ITSM的范围  

ITSM适用于IT管理而不是企业的业务管理。清楚这点非常重要，因为它明确划分了ITSM与ERP、CRM和SCM等管理方法和软件之间的界限，这个界限是：前者面向IT管理，后者面向业务管理。  

ITSM不是通用的IT规划方法。ITSM的重点是IT的运营和管理，而不是IT的战略规划。如果把组织的业务过程比作安排一辆汽车去完成一趟运输任务，那么IT规划的任务相当于为这次旅行选定正确的路线、合适的汽车和司机。而ITSM的任务则是确保汽车行驶过程中司机遵循操作规程和交通规则，对汽车进行必要的维修和保养，尽量避免其出现故障；一旦出现故障也能很快修复；并且当汽车到达目的地时，整个行驶过程中的所有费用都可以准确地计算出来，这便于衡量成本效益，为做出有关调整提供决策依据。简单地说，IT规划关注的是组织的IT方面的战略问题， 而ITSM是确保IT战略得到有效执行的战术性和运营性活动。  

虽然技术管理是ITSM的重要组成部分， 但ITSM的主要目标不是管理技术。有关IT的技术管理是系统管理和网络管理的任务，ITSM的主要任务是管理客户和用户的IT需求。这有点像营销管理。营销管理的本质是需求管理，其目标在于如何让组织生产的最终产品或提供的服务满足市场(客户) 的需求。同样， 在ITSM中， IT部门或IT外包商是IT服务的提供者， 业务部门是IT部门或IT外包商的客户，如何有效地利用IT资源恰当地满足业务部门的需求就成了ITSM的最终使命。换个角度说，对客户而言，业务部门只需关心IT服务有没有满足其要求，至于IT服务本身能不能或者怎样满足要求，业务部门作为客户不用也没有必要关心。  

关于这一点，可以用下面的例子说明。某个用户急需打印一份页数较多的文件，但恰好此时打印机出现故障， 那么用户传统的处理方式是通知和等待IT部门修复打印机，然后从感情上表达不满， 而"ITSM式"的处理方式是，对IT部门说："我需下午 5：00前使用该机打印文档，OK?"至于打印工作是怎样完成的，比如是通过修复或换一台打印机，那是IT部门的事，业务部门只需为服务本身付费。这就是ITSM与传统的IT管理的本质不同之处。  

4)ITSM的价值  

作为IT管理的"ERP解决方案"，IT服务管理给实施它的企业、企业员工及其他利益相关者提供多方面的价值。《IT服务管理实施规划》将这些价值归纳为商业价值、财务价值、创新价值和内部价值、员工利益。  

(1)商业价值。IT在商业中扮演着越来越重要的角色，通过实施IT服务管理，可以获取多方面的商业价值，例如：  

①确保IT流程支撑业务流程，整体上提高了业务运营的质量。  

②通过事件管理流程、变更管理流程和服务台等提供了更可靠的业务支持。  

③客户对IT有更合理的期望，并更加清楚为达到这些期望他们所需要的付出。  

④提高了客户和业务人员的生产率。  

⑤提供更加及时有效的业务持续性服务。  

⑥客户和IT服务提供者之间建立更加融洽的工作关系。  

⑦提高了客户满意度。  

(2)财务价值。IT服务管理不但提供商业价值，而且使企业在财务上直接受益，例如：  

①降低了实施变更的成本。  

当软件或硬件不再使用时，可以及时取消对其的维护合同。  

③)"量体裁衣"的能力，即根据实际需要提供适当的能力，如磁盘容量。  

④恰当的服务持续性费用。  

(3)内部价值和创新价值。IT服务管理提供的内部价值和创新价值包括：  

①IT服务提供方更为清楚地理解客户的需求，确保IT服务有效支撑业务流程。  

②更多地了解当前提供的IT服务的有关信息。  

改进IT支持，使业务部门能够更加灵活地使用IT。  

)提高了服务的灵活性和可适应性。  

⑤提高了预知未来发展趋势的能力，从而能够更加迅速地采用新的服务需求和进行相应的市场开发。  

(4)员工利益。IT服务管理也使服务人员多方面受益，例如：  

①IT人员更加清楚了解对他们的期望，并有合适的流程和相应的培训以确保他们·能够实现这些期望。  

②提高IT人员的生产率。  

③提高了IT人员的士气和工作满意度。  

④使IT部门的价值得到更好的体现，从而提高了员工的工作积极性。  

### 2.3.2 ITSS与信息技术服务  

#### 1.ITSS简介  

1)ITSS基本概念  

ITSS(Information Technology Service Standards， 信息技术服务标准，简称ITSS)是一套成体系和综合配套的信息技术服务标准库，全面规范了IT服务产品及其组成要素，用于指导实施标准化和可信赖的IT服务。  

122  

![9cf64ba2b971fc16e9fe4b76d3dc2bd5.jpeg](http://docmind-api-cn-hangzhou.oss-cn-hangzhou.aliyuncs.com/1617315274244978/publicDocStreamStructure/docmind-20260519-672fb26ef598441da7a1ea2e8ee2ae02/43.png?Expires=1779206880&OSSAccessKeyId=STS.NZebDGdcxohmUjCQd3QTqZtgp&Signature=JkYDOwWzmmAG6x0rQqlijzd6KA0%3D&x-oss-process=image%2Fcrop%2Cx_38%2Cy_0%2Cw_1216%2Ch_126&security-token=CAIS1wJ1q6Ft5B2yfSjIr5nQKf7zibxZ2KqGV0zytWRmXdtdtbHMkjz2IHhMeHVhCe4Ytfs1nmxX7voZlrp6SJtIXleCZtF94oxN9h2gb4fb4xRsN1SI08%2FLI3OaLjKm9u2wCryLYbGwU%2FOpbE%2B%2B5U0X6LDmdDKkckW4OJmS8%2FBOZcgWWQ%2FKBlgvRq0hRG1YpdQdKGHaONu0LxfumRCwNkdzvRdmgm4NgsbWgO%2Fks0CP0AahlLBL996veMb%2FNfMBZskvD42Hu8VtbbfE3SJq7BxHybx7lqQs%2B02c5onBXwgBvUvdbLCOroI3cFRjFKk2A%2BtIq%2FP5lPt0%2F%2FTajZ%2F6jkwVZ7wQSz7YVABLAzk41i3D3L8ZAlWbUxylurjnXhJFq5mGrt21HrfraghQy27xNG29hwvQXkuNkr7knEkN5aYL3t8Y37R7YXuKmfjOEzylJ9M9udm4napgBytAGoABil%2Fqf5MVplUu7%2BU4BxuSUkUaa02SKOYDC8avK6WNdtkYn0D%2BXqfl9bU8xbeXPrci2hscIAZ0%2BX8aXvgTYjydQRSQKMCg%2FHjlv%2B9b3hANppoB06dPBtIIG3M0IRS%2Bxt1mARqgcjJ60wjWc0nO7Tsoa4sADgcsEbmCjhLeq0uUesIgAA%3D%3D)  

##### 2)ITSS来源  

ITSS是在工业和信息化部、国家标准化管理委员会的联合指导下，由国家信息技术服务标准工作组(以下简称：ITSS工作组)组织研究制定的，是我国IT服务行业最佳实践的总结和提升，也是我国从事IT服务研发、供应、推广和应用等各类组织自主创新成果的固化。  

##### 3)ITSS原理  

ITSS充分借鉴了质量管理原理和过程改进方法的精髓，规定了IT服务的组成要素和生命周期，并对其进行标准化，如图2-2所示。  

![4f1a310a7c464820aab851197b0906ad.jpeg](http://docmind-api-cn-hangzhou.oss-cn-hangzhou.aliyuncs.com/1617315274244978/publicDocStreamStructure/docmind-20260519-672fb26ef598441da7a1ea2e8ee2ae02/43.png?Expires=1779206880&OSSAccessKeyId=STS.NZebDGdcxohmUjCQd3QTqZtgp&Signature=Ok%2F3SKWIZli69o3kg8gDx2Y7sJc%3D&x-oss-process=image%2Fcrop%2Cx_460%2Cy_697%2Cw_429%2Ch_414&security-token=CAIS1wJ1q6Ft5B2yfSjIr5nQKf7zibxZ2KqGV0zytWRmXdtdtbHMkjz2IHhMeHVhCe4Ytfs1nmxX7voZlrp6SJtIXleCZtF94oxN9h2gb4fb4xRsN1SI08%2FLI3OaLjKm9u2wCryLYbGwU%2FOpbE%2B%2B5U0X6LDmdDKkckW4OJmS8%2FBOZcgWWQ%2FKBlgvRq0hRG1YpdQdKGHaONu0LxfumRCwNkdzvRdmgm4NgsbWgO%2Fks0CP0AahlLBL996veMb%2FNfMBZskvD42Hu8VtbbfE3SJq7BxHybx7lqQs%2B02c5onBXwgBvUvdbLCOroI3cFRjFKk2A%2BtIq%2FP5lPt0%2F%2FTajZ%2F6jkwVZ7wQSz7YVABLAzk41i3D3L8ZAlWbUxylurjnXhJFq5mGrt21HrfraghQy27xNG29hwvQXkuNkr7knEkN5aYL3t8Y37R7YXuKmfjOEzylJ9M9udm4napgBytAGoABil%2Fqf5MVplUu7%2BU4BxuSUkUaa02SKOYDC8avK6WNdtkYn0D%2BXqfl9bU8xbeXPrci2hscIAZ0%2BX8aXvgTYjydQRSQKMCg%2FHjlv%2B9b3hANppoB06dPBtIIG3M0IRS%2Bxt1mARqgcjJ60wjWc0nO7Tsoa4sADgcsEbmCjhLeq0uUesIgAA%3D%3D)  

>图2-22ITSS原理  

(1)组成要素。IT服务由人员(People) 、流程(Process) 、技术(Technology)和资源(Resource)组成，简称PPTR。其中：  

·人员：指提供IT服务所需的人员及其知识、经验和技能要求；  

流程：指提供IT服务时，合理利用必要的资源，将输入转化为输出的一组相互关联和结构化的活动；  

·技术：指交付满足质量要求的IT服务应使用的技术或应具备的技术能力；  

·资源：指提供IT服务所依存和产生的有形及无形资产。  

(2)生命周期。IT服务生命周期由规划设计(Planning & Design) 、部署实施(Implementing) 、服务运营(Operation) 、持续改进(Improvement) 和监督管理(Supervision)5个阶段组成，简称 PIOIS。其中：  

·规划设计：从客户业务战略出发，以需求为中心， 参照ITSS对IT服务进行全面系统的战略规划和设计，为IT服务的部署实施做好准备，以确保提供满足客户  

需求的IT服务；  

部署实施：在规划设计基础上，依据ITSS建立管理体系、部署专用工具及服务解决方案；  

服务运营：根据服务部署情况，依据ITSS， 采用过程方法，全面管理基础设施、服务流程、人员和业务连续性，实现业务运营与IT服务运营融合；  

·持续改进：根据服务运营的实际情况，定期评审IT服务满足业务运营的情况，以及IT服务本身存在的缺陷，提出改进策略和方案，并对IT服务进行重新规划设计和部署实施，以提高IT服务质量；  

监督管理：本阶段主要依据ITSS对IT服务服务质量进行评价，并对服务供方的服务过程、交付结果实施监督和绩效评估。  

#### 2.ITSS与信息技术服务  

##### 1)信息技术服务概念  

信息技术服务：是指供方为需方提供如何开发、应用信息技术的服务，以及供方以信息技术为手段提供支持需方业务活动的服务。常见服务形态有信息技术咨询服务、设计与开发服务、信息系统集成服务、数据处理和运营服务及其他信息技术服务。  

##### 2)信息技术服务核心要素  

ITSS定义了IT服务的核心要素由人员、过程、技术和资源组成，并对这些IT服务的组成要素进行标准化，如图2-3所示。对这四个要素及其关系可以概括为：正确选择人员遵从过程规范，正确使用技术，并合理运用资源，向客户提供IT服务。  

![905c46f5aff2f5f9ccdfb9d703d7bac5.jpeg](http://docmind-api-cn-hangzhou.oss-cn-hangzhou.aliyuncs.com/1617315274244978/publicDocStreamStructure/docmind-20260519-672fb26ef598441da7a1ea2e8ee2ae02/44.png?Expires=1779206880&OSSAccessKeyId=STS.NZebDGdcxohmUjCQd3QTqZtgp&Signature=HYf0Qeuhf0arb2e4nJlThD1S6CY%3D&x-oss-process=image%2Fcrop%2Cx_383%2Cy_1075%2Cw_580%2Ch_396&security-token=CAIS1wJ1q6Ft5B2yfSjIr5nQKf7zibxZ2KqGV0zytWRmXdtdtbHMkjz2IHhMeHVhCe4Ytfs1nmxX7voZlrp6SJtIXleCZtF94oxN9h2gb4fb4xRsN1SI08%2FLI3OaLjKm9u2wCryLYbGwU%2FOpbE%2B%2B5U0X6LDmdDKkckW4OJmS8%2FBOZcgWWQ%2FKBlgvRq0hRG1YpdQdKGHaONu0LxfumRCwNkdzvRdmgm4NgsbWgO%2Fks0CP0AahlLBL996veMb%2FNfMBZskvD42Hu8VtbbfE3SJq7BxHybx7lqQs%2B02c5onBXwgBvUvdbLCOroI3cFRjFKk2A%2BtIq%2FP5lPt0%2F%2FTajZ%2F6jkwVZ7wQSz7YVABLAzk41i3D3L8ZAlWbUxylurjnXhJFq5mGrt21HrfraghQy27xNG29hwvQXkuNkr7knEkN5aYL3t8Y37R7YXuKmfjOEzylJ9M9udm4napgBytAGoABil%2Fqf5MVplUu7%2BU4BxuSUkUaa02SKOYDC8avK6WNdtkYn0D%2BXqfl9bU8xbeXPrci2hscIAZ0%2BX8aXvgTYjydQRSQKMCg%2FHjlv%2B9b3hANppoB06dPBtIIG3M0IRS%2Bxt1mARqgcjJ60wjWc0nO7Tsoa4sADgcsEbmCjhLeq0uUesIgAA%3D%3D)  

![e91c167cc19ef3bd0ebdd8d5fd2a2e71.jpeg](http://docmind-api-cn-hangzhou.oss-cn-hangzhou.aliyuncs.com/1617315274244978/publicDocStreamStructure/docmind-20260519-672fb26ef598441da7a1ea2e8ee2ae02/44.png?Expires=1779206880&OSSAccessKeyId=STS.NZebDGdcxohmUjCQd3QTqZtgp&Signature=bfvv1RFchhBrrDBwWLdA16MlqYM%3D&x-oss-process=image%2Fcrop%2Cx_550%2Cy_1152%2Cw_240%2Ch_238&security-token=CAIS1wJ1q6Ft5B2yfSjIr5nQKf7zibxZ2KqGV0zytWRmXdtdtbHMkjz2IHhMeHVhCe4Ytfs1nmxX7voZlrp6SJtIXleCZtF94oxN9h2gb4fb4xRsN1SI08%2FLI3OaLjKm9u2wCryLYbGwU%2FOpbE%2B%2B5U0X6LDmdDKkckW4OJmS8%2FBOZcgWWQ%2FKBlgvRq0hRG1YpdQdKGHaONu0LxfumRCwNkdzvRdmgm4NgsbWgO%2Fks0CP0AahlLBL996veMb%2FNfMBZskvD42Hu8VtbbfE3SJq7BxHybx7lqQs%2B02c5onBXwgBvUvdbLCOroI3cFRjFKk2A%2BtIq%2FP5lPt0%2F%2FTajZ%2F6jkwVZ7wQSz7YVABLAzk41i3D3L8ZAlWbUxylurjnXhJFq5mGrt21HrfraghQy27xNG29hwvQXkuNkr7knEkN5aYL3t8Y37R7YXuKmfjOEzylJ9M9udm4napgBytAGoABil%2Fqf5MVplUu7%2BU4BxuSUkUaa02SKOYDC8avK6WNdtkYn0D%2BXqfl9bU8xbeXPrci2hscIAZ0%2BX8aXvgTYjydQRSQKMCg%2FHjlv%2B9b3hANppoB06dPBtIIG3M0IRS%2Bxt1mARqgcjJ60wjWc0nO7Tsoa4sADgcsEbmCjhLeq0uUesIgAA%3D%3D)  

>图2-33I IT服务组成  

##### 3)信息技术服务生命周期  

ITSS定义的IT服务生命周期由规划设计、部署实施、服务运营、持续改进和监督管理五个阶段组成，并规定了IT服务生命周期各阶段应遵循的标准，涉及咨询设计、集成实施、运行维护及运营服务等领域。如图2-4所示。  

124  

![f71ccdd20c6847fbbd8505e8ecde4a86.jpeg](http://docmind-api-cn-hangzhou.oss-cn-hangzhou.aliyuncs.com/1617315274244978/publicDocStreamStructure/docmind-20260519-672fb26ef598441da7a1ea2e8ee2ae02/45.png?Expires=1779206880&OSSAccessKeyId=STS.NZebDGdcxohmUjCQd3QTqZtgp&Signature=P%2BYbxWp1%2FoSsuyIahN1YMS3Zk84%3D&x-oss-process=image%2Fcrop%2Cx_67%2Cy_6%2Cw_1155%2Ch_115&security-token=CAIS1wJ1q6Ft5B2yfSjIr5nQKf7zibxZ2KqGV0zytWRmXdtdtbHMkjz2IHhMeHVhCe4Ytfs1nmxX7voZlrp6SJtIXleCZtF94oxN9h2gb4fb4xRsN1SI08%2FLI3OaLjKm9u2wCryLYbGwU%2FOpbE%2B%2B5U0X6LDmdDKkckW4OJmS8%2FBOZcgWWQ%2FKBlgvRq0hRG1YpdQdKGHaONu0LxfumRCwNkdzvRdmgm4NgsbWgO%2Fks0CP0AahlLBL996veMb%2FNfMBZskvD42Hu8VtbbfE3SJq7BxHybx7lqQs%2B02c5onBXwgBvUvdbLCOroI3cFRjFKk2A%2BtIq%2FP5lPt0%2F%2FTajZ%2F6jkwVZ7wQSz7YVABLAzk41i3D3L8ZAlWbUxylurjnXhJFq5mGrt21HrfraghQy27xNG29hwvQXkuNkr7knEkN5aYL3t8Y37R7YXuKmfjOEzylJ9M9udm4napgBytAGoABil%2Fqf5MVplUu7%2BU4BxuSUkUaa02SKOYDC8avK6WNdtkYn0D%2BXqfl9bU8xbeXPrci2hscIAZ0%2BX8aXvgTYjydQRSQKMCg%2FHjlv%2B9b3hANppoB06dPBtIIG3M0IRS%2Bxt1mARqgcjJ60wjWc0nO7Tsoa4sADgcsEbmCjhLeq0uUesIgAA%3D%3D)  

系统集成项目管理工程师教程(第2版)  

![0c1f4b19989db37f656c6c4c942683ff.jpeg](http://docmind-api-cn-hangzhou.oss-cn-hangzhou.aliyuncs.com/1617315274244978/publicDocStreamStructure/docmind-20260519-672fb26ef598441da7a1ea2e8ee2ae02/45.png?Expires=1779206880&OSSAccessKeyId=STS.NZebDGdcxohmUjCQd3QTqZtgp&Signature=rBYmHdptrpD9B50CNFP%2BxCEHYss%3D&x-oss-process=image%2Fcrop%2Cx_213%2Cy_352%2Cw_927%2Ch_647&security-token=CAIS1wJ1q6Ft5B2yfSjIr5nQKf7zibxZ2KqGV0zytWRmXdtdtbHMkjz2IHhMeHVhCe4Ytfs1nmxX7voZlrp6SJtIXleCZtF94oxN9h2gb4fb4xRsN1SI08%2FLI3OaLjKm9u2wCryLYbGwU%2FOpbE%2B%2B5U0X6LDmdDKkckW4OJmS8%2FBOZcgWWQ%2FKBlgvRq0hRG1YpdQdKGHaONu0LxfumRCwNkdzvRdmgm4NgsbWgO%2Fks0CP0AahlLBL996veMb%2FNfMBZskvD42Hu8VtbbfE3SJq7BxHybx7lqQs%2B02c5onBXwgBvUvdbLCOroI3cFRjFKk2A%2BtIq%2FP5lPt0%2F%2FTajZ%2F6jkwVZ7wQSz7YVABLAzk41i3D3L8ZAlWbUxylurjnXhJFq5mGrt21HrfraghQy27xNG29hwvQXkuNkr7knEkN5aYL3t8Y37R7YXuKmfjOEzylJ9M9udm4napgBytAGoABil%2Fqf5MVplUu7%2BU4BxuSUkUaa02SKOYDC8avK6WNdtkYn0D%2BXqfl9bU8xbeXPrci2hscIAZ0%2BX8aXvgTYjydQRSQKMCg%2FHjlv%2B9b3hANppoB06dPBtIIG3M0IRS%2Bxt1mARqgcjJ60wjWc0nO7Tsoa4sADgcsEbmCjhLeq0uUesIgAA%3D%3D)  

>图2-4ITSS定义的IT服务生命周期  

IT服务生命周期的引入，改变了IT服务在不同阶段相互割裂、独立实施的局面。同时，通过连贯的逻辑体系，以规划设计为指导，通过部署实施、服务运营，直至持续改进，同时伴随着监督管理的不断完善，将IT服务中的不同阶段的不同过程有机整合为一个井然有序、良性循环的整体， 使IT服务质量得以不断改进和提升。IT服务的供需双方在IT服务生命周期的各个阶段设定面向客户的服务目标，在服务质量、运营效率和业务连续性方面不断改进和提升，并能够有效识别、选择和优化IT服务的有效性， 提高绩效，为组织做出更优的决策提供指导。  

##### 4)信息技术的标准化和产业化  

IT服务的产业化进程分为产品服务化、服务标准化和服务产品化3个阶段，其中：  

·产品服务化：软件服务化已成为软件产业发展的主要方向之一，特别是云计算、物联网、移动互联网等新模式新技术的不断出现，改变了软件的生产和销售模式，软件即服务(SaaS) 、平台即服务(PaaS) 、基础设施即服务(IaaS) 等业务形态的出现，促使软件企业以产品为基础向服务转型。  

·服务标准化：标准化是确保服务实现专业化、规模化生产的前提，也是规范服务  

市场的重要手段。在服务标准化的过程中， ITSS的核心作用是确定IT服务的范围和内容，规范组成服务的人员、过程、技术及资源等要素，从而为IT服务的规划化生产和消费奠定基础。  

服务产品化：产品化是实现产业化的前提和基础，只有用户对市场中存在的服务产品达到一致认识的前提下，服务的规模化生产和消费才能成为可能。总的来说，产品服务化是前提， 服务标准化是保障，服务产品化是趋势。三者之间的关系如图2-5所示。  

![e7a423cd91d8574891a3b771a161d039.jpeg](http://docmind-api-cn-hangzhou.oss-cn-hangzhou.aliyuncs.com/1617315274244978/publicDocStreamStructure/docmind-20260519-672fb26ef598441da7a1ea2e8ee2ae02/46.png?Expires=1779206879&OSSAccessKeyId=STS.NZebDGdcxohmUjCQd3QTqZtgp&Signature=ZMZogRekNhIabmEkkR0W18M4gOE%3D&x-oss-process=image%2Fcrop%2Cx_393%2Cy_566%2Cw_543%2Ch_415&security-token=CAIS1wJ1q6Ft5B2yfSjIr5nQKf7zibxZ2KqGV0zytWRmXdtdtbHMkjz2IHhMeHVhCe4Ytfs1nmxX7voZlrp6SJtIXleCZtF94oxN9h2gb4fb4xRsN1SI08%2FLI3OaLjKm9u2wCryLYbGwU%2FOpbE%2B%2B5U0X6LDmdDKkckW4OJmS8%2FBOZcgWWQ%2FKBlgvRq0hRG1YpdQdKGHaONu0LxfumRCwNkdzvRdmgm4NgsbWgO%2Fks0CP0AahlLBL996veMb%2FNfMBZskvD42Hu8VtbbfE3SJq7BxHybx7lqQs%2B02c5onBXwgBvUvdbLCOroI3cFRjFKk2A%2BtIq%2FP5lPt0%2F%2FTajZ%2F6jkwVZ7wQSz7YVABLAzk41i3D3L8ZAlWbUxylurjnXhJFq5mGrt21HrfraghQy27xNG29hwvQXkuNkr7knEkN5aYL3t8Y37R7YXuKmfjOEzylJ9M9udm4napgBytAGoABil%2Fqf5MVplUu7%2BU4BxuSUkUaa02SKOYDC8avK6WNdtkYn0D%2BXqfl9bU8xbeXPrci2hscIAZ0%2BX8aXvgTYjydQRSQKMCg%2FHjlv%2B9b3hANppoB06dPBtIIG3M0IRS%2Bxt1mARqgcjJ60wjWc0nO7Tsoa4sADgcsEbmCjhLeq0uUesIgAA%3D%3D)  

>图2-5ITSS与IT服务之间的关系  

#### 3. ITSS主要内容  

##### 1)ITSS体系框架  

标准体系是标准化系统为了实现本系统的目标而必须具备一整套具有内在联系的、科学的、由标准组成的有机整体。标准体系是一个概念系统，是人为组织制定的标准而形成的人工系统。  

ITSS体系的提出主要从业务分类、服务管控、服务安全、服务业务、外包、对象、和行业等几个方面考虑，分为基础标准、服务管控标准、服务外包标准、业务标准、安全标准、行业应用标准6大类。ITSS体系框架如图2-6所示。  

###### ITSS主要内容包括：  

·基础标准旨在阐述信息技术服务的业务分类、服务级别协议、服务质量评价方法、服务人员能力要求等；  

·服务管控标准是指通过对信息技术服务的治理、管理和监理活动，以确保信息技术服务的经济有效：  

业务标准按业务类型分为面向IT的服务标准(咨询设计标准、集成实施标准和运行维护标准)和IT驱动的服务标准(服务运营标准)，按标准编写目的分为通用要求、服务规范和实施指南，其中通用要求是对各业务类型的基本能力要素的要求，服务规范是对服务内容和行为的规范，实施指南是对服务的落地指导；  

126  

![5417ebea550e4dc7813b8af719e4f946.jpeg](http://docmind-api-cn-hangzhou.oss-cn-hangzhou.aliyuncs.com/1617315274244978/publicDocStreamStructure/docmind-20260519-672fb26ef598441da7a1ea2e8ee2ae02/47.png?Expires=1779206880&OSSAccessKeyId=STS.NZebDGdcxohmUjCQd3QTqZtgp&Signature=p5hT%2BklhT0OYdOj5q%2F%2BOupxlgJo%3D&x-oss-process=image%2Fcrop%2Cx_81%2Cy_1%2Cw_1130%2Ch_126&security-token=CAIS1wJ1q6Ft5B2yfSjIr5nQKf7zibxZ2KqGV0zytWRmXdtdtbHMkjz2IHhMeHVhCe4Ytfs1nmxX7voZlrp6SJtIXleCZtF94oxN9h2gb4fb4xRsN1SI08%2FLI3OaLjKm9u2wCryLYbGwU%2FOpbE%2B%2B5U0X6LDmdDKkckW4OJmS8%2FBOZcgWWQ%2FKBlgvRq0hRG1YpdQdKGHaONu0LxfumRCwNkdzvRdmgm4NgsbWgO%2Fks0CP0AahlLBL996veMb%2FNfMBZskvD42Hu8VtbbfE3SJq7BxHybx7lqQs%2B02c5onBXwgBvUvdbLCOroI3cFRjFKk2A%2BtIq%2FP5lPt0%2F%2FTajZ%2F6jkwVZ7wQSz7YVABLAzk41i3D3L8ZAlWbUxylurjnXhJFq5mGrt21HrfraghQy27xNG29hwvQXkuNkr7knEkN5aYL3t8Y37R7YXuKmfjOEzylJ9M9udm4napgBytAGoABil%2Fqf5MVplUu7%2BU4BxuSUkUaa02SKOYDC8avK6WNdtkYn0D%2BXqfl9bU8xbeXPrci2hscIAZ0%2BX8aXvgTYjydQRSQKMCg%2FHjlv%2B9b3hANppoB06dPBtIIG3M0IRS%2Bxt1mARqgcjJ60wjWc0nO7Tsoa4sADgcsEbmCjhLeq0uUesIgAA%3D%3D)  

![dd7c60a0f62d9f52e53db06d30097687.jpeg](http://docmind-api-cn-hangzhou.oss-cn-hangzhou.aliyuncs.com/1617315274244978/publicDocStreamStructure/docmind-20260519-672fb26ef598441da7a1ea2e8ee2ae02/47.png?Expires=1779206880&OSSAccessKeyId=STS.NZebDGdcxohmUjCQd3QTqZtgp&Signature=s0oBMXuUZ6XHmwZBQnLTDehdJG0%3D&x-oss-process=image%2Fcrop%2Cx_152%2Cy_395%2Cw_1044%2Ch_601&security-token=CAIS1wJ1q6Ft5B2yfSjIr5nQKf7zibxZ2KqGV0zytWRmXdtdtbHMkjz2IHhMeHVhCe4Ytfs1nmxX7voZlrp6SJtIXleCZtF94oxN9h2gb4fb4xRsN1SI08%2FLI3OaLjKm9u2wCryLYbGwU%2FOpbE%2B%2B5U0X6LDmdDKkckW4OJmS8%2FBOZcgWWQ%2FKBlgvRq0hRG1YpdQdKGHaONu0LxfumRCwNkdzvRdmgm4NgsbWgO%2Fks0CP0AahlLBL996veMb%2FNfMBZskvD42Hu8VtbbfE3SJq7BxHybx7lqQs%2B02c5onBXwgBvUvdbLCOroI3cFRjFKk2A%2BtIq%2FP5lPt0%2F%2FTajZ%2F6jkwVZ7wQSz7YVABLAzk41i3D3L8ZAlWbUxylurjnXhJFq5mGrt21HrfraghQy27xNG29hwvQXkuNkr7knEkN5aYL3t8Y37R7YXuKmfjOEzylJ9M9udm4napgBytAGoABil%2Fqf5MVplUu7%2BU4BxuSUkUaa02SKOYDC8avK6WNdtkYn0D%2BXqfl9bU8xbeXPrci2hscIAZ0%2BX8aXvgTYjydQRSQKMCg%2FHjlv%2B9b3hANppoB06dPBtIIG3M0IRS%2Bxt1mARqgcjJ60wjWc0nO7Tsoa4sADgcsEbmCjhLeq0uUesIgAA%3D%3D)  

>图2-6 ITSS体系框架  

·服务外包标准是对信息技术服务采用外包方式时的通用要求及规范；  

·服务安全标准重点规定事前预防、事中控制、事后审计服务安全以及整个过程的持续改进，并提出组织的服务安全治理规范，以确保服务安全可控；  

·行业应用标准是对各行业进行定制化应用落地的实施指南。  

信息技术服务标准体系是动态发展的，与信息技术服务相关的技术和产业发展紧密相关，同时也与标准化工作的目标和定位紧密相关。  

###### 2)ITSS核心价值  

在信息技术服务产业，主要的利益相关方包括服务需方和服务供方，服务需方主要是各行业用户，服务供方主要是提供相应软件、硬件、服务或人员的服务供应商。除此之外，还有监管机构(工业和信息化部、国家标准化管理委员会、国家认证认可监督管理委员会等)、行业协会、认证/咨询等中介机构、教育培训机构和从业人员等。信息技术服务产业的生命力来源于各行业用户的信息技术服务需求，而在行业用户中包括IT部门、业务部门、CIO等不同角色或主体。ITSS重点考虑了服务标准化对于服务需方内部各个主体的价值。信息技术服务各利益相关方如图2-7所示。  

![bc2a84be4c70495b09997ae05dd085fa.jpeg](http://docmind-api-cn-hangzhou.oss-cn-hangzhou.aliyuncs.com/1617315274244978/publicDocStreamStructure/docmind-20260519-672fb26ef598441da7a1ea2e8ee2ae02/48.png?Expires=1779206880&OSSAccessKeyId=STS.NZebDGdcxohmUjCQd3QTqZtgp&Signature=RK0R%2Fj%2BI9i3BznKSTUUdngPO6lw%3D&x-oss-process=image%2Fcrop%2Cx_239%2Cy_250%2Cw_853%2Ch_331&security-token=CAIS1wJ1q6Ft5B2yfSjIr5nQKf7zibxZ2KqGV0zytWRmXdtdtbHMkjz2IHhMeHVhCe4Ytfs1nmxX7voZlrp6SJtIXleCZtF94oxN9h2gb4fb4xRsN1SI08%2FLI3OaLjKm9u2wCryLYbGwU%2FOpbE%2B%2B5U0X6LDmdDKkckW4OJmS8%2FBOZcgWWQ%2FKBlgvRq0hRG1YpdQdKGHaONu0LxfumRCwNkdzvRdmgm4NgsbWgO%2Fks0CP0AahlLBL996veMb%2FNfMBZskvD42Hu8VtbbfE3SJq7BxHybx7lqQs%2B02c5onBXwgBvUvdbLCOroI3cFRjFKk2A%2BtIq%2FP5lPt0%2F%2FTajZ%2F6jkwVZ7wQSz7YVABLAzk41i3D3L8ZAlWbUxylurjnXhJFq5mGrt21HrfraghQy27xNG29hwvQXkuNkr7knEkN5aYL3t8Y37R7YXuKmfjOEzylJ9M9udm4napgBytAGoABil%2Fqf5MVplUu7%2BU4BxuSUkUaa02SKOYDC8avK6WNdtkYn0D%2BXqfl9bU8xbeXPrci2hscIAZ0%2BX8aXvgTYjydQRSQKMCg%2FHjlv%2B9b3hANppoB06dPBtIIG3M0IRS%2Bxt1mARqgcjJ60wjWc0nO7Tsoa4sADgcsEbmCjhLeq0uUesIgAA%3D%3D)  

>图2-7信息技术服务利益相关方关系图  

ITSS为不同组织所能带来的价值侧重点各有不同，而不同组织对于ITSS所能带来价值的期望也有所差异。如行业用户可以通过采用 ITSS 来规范外包工作，选择恰当的供应商：而服务供应商可以采用ITSS来持续提升服务质量，确保客户满意度和财务收益。  

##### 2.3.3信息系统审计  

###### 1.信息系统审计概念  

信息系统审计是全部审计过程的一个部分，信息系统审计(IS audit) 目前还没有固定通用的定义，美国信息系统审计的权威专家 Ron Weber将它定义为"收集并评估证据以决定一个计算机系统(信息系统)是否有效做到保护资产、维护数据完整、完成组织目标，同时最经济地使用资源"。  

信息系统审计的目的是评估并提供反馈、保证及建议。其关注之处可被分为如下3类。  

·可用性：商业高度依赖的信息系统能否在任何需要的时刻提供服务?信息系统是否被完好保护以应对各种损失和灾难?  

保密性：系统保存的信息是否仅对需要这些信息的人员开放，而不对其他任何人开放?  

完整性：信息系统提供的信息是否始终保持正确、可信、及时?能否防止未授权的对系统数据和软件的修改?  

###### 2.信息系统审计产生动因及其发展  

####### 1)信息系统审计产生动因分析  

关于信息系统审计的产生动因，目前国际上存在两种观点：一种观点认为是从会计审计发展到计算机审计再发展到信息系统审计(计算机审计的范围扩展，最后涵盖整个信息系统)演变过来的；另外一种认为由于信息系统尤其是大型信息系统的建设是一项庞大的系统工程，它投资大、周期长、高技术、高风险，在系统的建设过程中，对工程进行严格、规范的管理和控制至关重要。而正是由于信息系统工程所具有的这些特点，建设单位往往由于技术力量有限，无力对项目的技术、设备、进度、质量和风险进行控制，无法保证项目的实施成功。所以需要有第三方进行独立审计。  

![a461eb78fa32ac87830b623e67d9470b.jpeg](http://docmind-api-cn-hangzhou.oss-cn-hangzhou.aliyuncs.com/1617315274244978/publicDocStreamStructure/docmind-20260519-672fb26ef598441da7a1ea2e8ee2ae02/49.png?Expires=1779206880&OSSAccessKeyId=STS.NZebDGdcxohmUjCQd3QTqZtgp&Signature=n8oWOTnJn%2FwmJwQ9UylMR1ACFDY%3D&x-oss-process=image%2Fcrop%2Cx_112%2Cy_5%2Cw_1046%2Ch_116&security-token=CAIS1wJ1q6Ft5B2yfSjIr5nQKf7zibxZ2KqGV0zytWRmXdtdtbHMkjz2IHhMeHVhCe4Ytfs1nmxX7voZlrp6SJtIXleCZtF94oxN9h2gb4fb4xRsN1SI08%2FLI3OaLjKm9u2wCryLYbGwU%2FOpbE%2B%2B5U0X6LDmdDKkckW4OJmS8%2FBOZcgWWQ%2FKBlgvRq0hRG1YpdQdKGHaONu0LxfumRCwNkdzvRdmgm4NgsbWgO%2Fks0CP0AahlLBL996veMb%2FNfMBZskvD42Hu8VtbbfE3SJq7BxHybx7lqQs%2B02c5onBXwgBvUvdbLCOroI3cFRjFKk2A%2BtIq%2FP5lPt0%2F%2FTajZ%2F6jkwVZ7wQSz7YVABLAzk41i3D3L8ZAlWbUxylurjnXhJFq5mGrt21HrfraghQy27xNG29hwvQXkuNkr7knEkN5aYL3t8Y37R7YXuKmfjOEzylJ9M9udm4napgBytAGoABil%2Fqf5MVplUu7%2BU4BxuSUkUaa02SKOYDC8avK6WNdtkYn0D%2BXqfl9bU8xbeXPrci2hscIAZ0%2BX8aXvgTYjydQRSQKMCg%2FHjlv%2B9b3hANppoB06dPBtIIG3M0IRS%2Bxt1mARqgcjJ60wjWc0nO7Tsoa4sADgcsEbmCjhLeq0uUesIgAA%3D%3D)  

####### 2)信息系统审计在国际上的发展  

信息系统审计的发展是伴随着信息技术的发展而发展的。在数据处理电算化的初期，由于人们对计算机在数据处理中的应用所产生的影响没有足够的认识，认为计算机处理数据准确可靠，不会出现错弊，因而很少对数据处理系统进行审计，主要是对计算机打印出的一部分资料进行传统的手工审计。随着计算机在数据处理系统中应用的逐步扩大，利用计算机犯罪的案件不断出现，使审计人员认识到要应用计算机辅助审计技术对电子数据处理系统本身进行审计，即EDI审计。同时随着社会经济的发展，审计对象、范围越来越大，审计业务也越来越复杂，利用传统的手工方法已不能及时完成审计任务，必须应用计算机辅助审计技术(CAATs) 进行审计。20世纪八九十年代信息技术的进一步发展与普及，使得企业越来越依赖信息及产生信息的信息系统。人们开始更多地关注信息系统的安全性、保密性、完整性及其实现企业目标的效率、效果，真正意义的信息系统审计才出现。随着电子商务的全球普及，信息系统的审计对象、范围及内容将逐渐扩大，采用的技术也将日益复杂。到目前为止，信息系统审计在全球来看，还是一个新的业务，从美国五大会计师事务所的数据看1990年拥有信息系统审计师12名到近百名，1995年已有500名，到2000年时，所拥有的信息系统审计师人数正以每年40%~50%的速度增加，说明信息系统审计正逐渐受到重视。  

美国在计算机进入实用阶段时就开始提出系统审计(SYSTEM AUDIT)， 从成立电子数据处理审计协会(EDPAA后更名为ISACA)以来，从事系统审计活动已有30多年历史，成为信息系统审计的主要推动者，在全球建有一百多个分会，推出了一系列信息系统审计准则、职业道德准则等规范性文件，并开展了大量的理论研究， IT控制的开放式标准COBIT(Control Objectives for Information and Related Technology) 已出版了五版。  

####### 3)信息系统审计在国内的发展  

目前国内有学者提出计算机审计、电算化审计，但基本上停留在对会计信息系统的审计上，只是延伸手工会计信息系统审计，尚未全面探讨信息时代给审计业务带来的深刻变化。以我国在1999年颁布的独立审计准则第20号——计算机信息系统环境下的审计为例，其更多关注的是会计信息系统。在信息时代，面对加入WTO后全球一体化市场，我国IT服务业面临巨大的挑战，开展信息系统审计业务不失为推动我国IT服务业发展的一次机会。  

###### 3.信息系统审计的理论基础  

信息系统审计不仅仅是传统审计业务的简单扩展，信息技术不单影响传统审计人员执行鉴证业务的能力，更重要的是公司和信息系统管理者都认识到信息资产是组织最有价值的资产，和传统资产一样需要控制，组织同时需要审计人员提供对信息资产控制的