## Task



### 1. Task Introduction

现在要做的是从两个 knowledge graph 中, 制作一个对应的 Correspond-graphs dataset.

因此需要三个数据源 : L-Graph, R-Graph, Homo-Pairs(homologous)

L-Graph : 用于映射的 graph 1.

G-Graph : 用于映射的 graph 2.

Homo-Pairs : 用于两个图中信息的对应.

### 2. Three datasets

#### 2.1 Datasets

- **L-Graph** : 这里使用的是 [DBpedia](http://fragments.dbpedia.org/2016-04/en), 这里用的是在线 API. 
- **R-Graph** : 这里使用的是 FreeBase, 由于 API 被谷歌停掉 这里只能自己处理, 也是这次的主要问题所在. 有 **1.9 billion** triples. 
- **Homo-Pairs** : DBpedia 中的 freebase_links_en.ttl. 其中共有 **10169316** 的对应条目



#### 2.2 Datasets pruning

由于这里的数据集太大, 因此我们需要一个子集. 目标:

L-Graph, R-Graph 这里仿照 FB15K 的大小, 大约各采15000个entities. 



#### 2.2 Graph requirement

##### 1)  Full correspondence Vs Half correspondence ? 

###### Question & Answer

L-Graph, R-Graph的全部node是否应该是 Full correspondence 的 ?

答案是 : 两个 Graph 不能是全对应的, 因为, 这样就变成了两个极为相似的graph的映射问题. 之所以说极为相似是因为, 在两个 Graph 中, 即使 entity 对应, 其 Relation 也不一定是对应的.

###### Overlap rate

两个 Graph 重合部分的比例. 在这里, 我比较倾向于将其作为参数来看待. 会创造出 0.2-0.8 比例的重合比例, 因此最初获取的 Graph 必须要各自能满足 0.2 的比例, 也就是要有 15000*4 个, 两者互不重合的 entities. 这样, 对每个 Graph 的要求就上升到 60000 个. 

##### 2)  Property

这里的问题是, 如何去 sample 子集. Graph 有一定的性质, 首先看有那些性质:

- 平均度数
- 平均距离
- 聚集系数

如果我们采用随机采样的方式去采子图很有可能出现的问题是及其稀疏的. 因此, 我们需要一种采子图的方式可以使我们的图在采完之后还和原图保有