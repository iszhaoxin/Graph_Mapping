## Graph Mapping 

### 0. Backgroud 

Same entities in real-world have different marks in different datasets. 

For example, In DBpedia, "Jesus is the children of Mary" is represented as triple 

> Head Entity : http://dbpedia.org/resource/Jesus 			
>
> Link : http://dbpedia.org/ontology/parent
>
> Tail Entity : http://dbpedia.org/resource/Mary_(mother_of_Jesus)

But in FB15K, there is another representation of this sentence, as:

> Head Entity : /m/04n7gc6 (Notation of Jesus)
>
> Link : /people/person/children				
>
> Tail Entity : /m/045m1_ (Notation of Mary)

Freebase is a stopped-update database, which DBpedia is still updating. So, with the information in DBpedia, we can enlarge the freebase. 

### 1. Three basic dataset

##### 1.1 FB15K

[FB15K](https://en.wikipedia.org/wiki/Free_base)

13583 entities 592213 triples

Free base is the conjugate base form of an amine, as opposed to its conjugate acid  form. 

##### 1.2 DBpedia

[DBpedia](https://wiki.dbpedia.org/) (crawl online)

DBpedia is a crowd-sourced community effort to extract structured content from the information created in various Wikimedia projects. This structured information resembles an open knowledge graph (OKG) which is available for everyone on the Web. 


##### 1.3 DBs-FBs

DBs-FBs -> download available

Download avaliable from DBpedia website

> Entity in DBs : <http://dbpedia.org/resource/Jesus> 
>
> 
>
> [sameAs] relation : <http://www.w3.org/2002/07/owl#sameAs> 
>
> Entity in FBs : <http://rdf.freebase.com/ns/m.045m1_>

#### 2. Crawler of DBpedia 

##### 2.1 Tools

Crawl by scrapy  2.2 

##### 2.2 Crawl strategy  

###### 1) Only entities in FB15K 

- Without 'wikiPage'-link : (12730 entities 112391 triples) -> using
- With 'wikiPage'-link : (13934 entities 685392 triples)

###### 2) One more layer connect to entities in FB15K

- With 'wikiPage'-link : (6411218 entities 38597471 triples)

- Without 'wikiPage'-link : (4349425 entities 12787660 triples)

  ​



#### 3. Results&Analysis

##### 3.1 Entities 

- 15580 DB items
- 13499 FB items (13583 in raw FB15K)

##### 3.2 Properties

###### 1) One-to-many 

One-to-many mapping relation between two datasets.

###### 2) Overlap rate

- DB, FB -> convert to undirected graph
- Adjacency matrix:
  - FB matrix : $\mathcal{M}_f$
  - DB matrix :  $\mathcal{M}_d$
  - Overlap matrix : $\mathcal{M}_d = \mathcal{M}_f \& \mathcal{M}_d$
  - All matrix : $\mathcal{M}_a = \mathcal{M}_f + \mathcal{M}_d$


- Result:
  - overlap / DB = sum($\mathcal{M}_o$) / sum($\mathcal{M}_d$) = 0.614
  - overlap / FB = sum($\mathcal{M}_o$) / sum($\mathcal{M}_f$) = 0.063
  - overlap / all = sum($\mathcal{M}_o$) / sum($\mathcal{M}_a$) = 0.114


