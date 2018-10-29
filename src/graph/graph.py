import sys
sys.path.append('../prepare')
import numpy as np

def overlap_rate(graph1, graph2, project):
    graphE1, graphE1_R     = {}, {}
    graphE2, graphE2_R     = {}, {}
    unrelated_fb = open('/home/dreamer/codes/my_code/subGraph/data/raw_data/unrelated_fbs', 'w')
    with open(pro, 'r') as f:
        cnt = 0
        for l in f:
            e1, e2 = l.split()
            e1 = e1[1:-1]
            if e1 not in graphE1:
                graphE1.update({e1:[cnt]})
            else:
                graphE1[e1].append(cnt)
                graphE1.update({e1:graphE1[e1]})   
            if e2 not in graphE2:
                graphE2.update({e2:[cnt]})
            else:
                graphE2[e2].append(cnt)
                graphE2.update({e2:graphE2[e2]})
            cnt+=1
    for k in graphE1:
        for i in graphE1[k]:
            graphE1_R.update({i:k})
    for k in graphE2:
        for i in graphE2[k]:
            graphE2_R.update({i:k})
    a = "http://dbpedia.org/resource/The_Sum_of_All_Fears_(film)"
    matrix1 = np.zeros((cnt,cnt), dtype=int)
    matrix2 = np.zeros((cnt,cnt), dtype=int)
    with open(graph1, 'r') as f:
        for l in f:
            h,r,t = l.split()
            for i in graphE1[h]:
                for j in graphE1[t]:
                    matrix1[i][j] = 1
    with open(graph2, 'r') as f:
        for l in f:
            h,r,t = l.split()
            if h in graphE2 and t in graphE2:
                for i in graphE2[h]:
                    for j in graphE2[t]:
                        matrix2[i][j] = 1
            else:
                if h in graphE2:
                    unrelated_fb.write(t+'\n')
                if t in graphE2:
                    unrelated_fb.write(h+'\n')
    
    matrix_integrate = matrix1 + matrix2
    matrix_integrate2 = matrix1 + matrix2
    all_triples = np.sum(matrix_integrate)
    matrix_integrate = matrix_integrate/2
    overlap = np.sum(matrix_integrate.astype(int))*2
    matrix1_sum = np.sum(matrix1)
    matrix2_sum = np.sum(matrix2)
    print("matrix1:",matrix1_sum)
    print("matrix2:",matrix2_sum)
    matrix1_special = np.where(matrix1+matrix_integrate.astype(int)==2)
    matrix2_special = np.where(matrix2+matrix_integrate.astype(int)==2)
    print("overlap/matrix1:",np.sum(len(matrix1_special[0]))/matrix1_sum)
    print("overlap/matrix2:",np.sum(len(matrix2_special[0]))/matrix2_sum)
    print("all_triples:", all_triples)
    print("overlap:",overlap)
    return overlap/all_triples
    

DB = "/home/dreamer/codes/my_code/subGraph/data/results/withoutWiki/DB15K_rd"
FB = "/home/dreamer/codes/my_code/subGraph/data/raw_data/FB15K"
pro= "/home/dreamer/codes/my_code/subGraph/data/conversion/DB-FB(15K)"
overlap = overlap_rate(DB, FB, pro)
print(overlap)
