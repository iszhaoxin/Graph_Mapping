import os, re, json
import mylib.texthelper.decorator as decorator
import mylib.texthelper.format as texthelper
import numpy as np
import itertools
from scipy.sparse import csr_matrix

Debug = True

class DataHelper:
    def __init__(self, file, NP=False, nodeIndexStart=0, edgeIndexStart=0):
        self.file = file
        self.nodeIndexStart = nodeIndexStart
        self.edgeIndexStart = edgeIndexStart
        self.edges, self.nodes = set(),set()
        self.NP = NP
        self.id()
        self._GraphSet()
        
    def id(self):
        self.node2id = dict()
        self.edge2id = dict()
        nodeIndex = self.nodeIndexStart
        edgeIndex = self.edgeIndexStart
        with open(self.file, 'r') as f:
            for line in f:
                headnode, edge, tailnode = line.split()
                if headnode not in self.node2id.keys():
                    self.node2id.update({headnode:nodeIndex})
                    nodeIndex += 1
                if tailnode not in self.node2id.keys():
                    self.node2id.update({tailnode:nodeIndex})
                    nodeIndex += 1
                if edge not in self.edge2id.keys():
                    self.edge2id.update({edge:edgeIndex})
                    edgeIndex += 1
        self.id2node = {v: k for k, v in self.node2id.items()}
        self.id2edge = {v: k for k, v in self.edge2id.items()}
        # print("nodeIndex:",nodeIndex, "edgeIndex:",edgeIndex, '\n')

    def _GraphSet(self):
        if self.NP == True:
            samples = list(itertools.chain.from_iterable(self.GetSamples())) # 3d->2d
        else:
            samples = self.GetSamples()
        samples = np.array(samples) # list -> np.array
        for triples in samples:
            self.nodes.add(triples[0])
            self.nodes.add(triples[2])
            self.edges.add(triples[1])

    def GetSamples(self):
        triples = []
        with open(self.file, 'r') as tf:
            for line in tf:
                triples.append(line.split())
        triples = np.array(triples)
        if self.NP == True:
            positive_samples = triples[triples[:,3]=="1"][:-1]
            negative_samples = triples[triples[:,3]=="-1"][:-1]
            return positive_samples, negative_samples
        else:
            return triples

    def sampleid2file(self, tf):
        posSamples = self.GetSamples()[0]
        with open(tf, "w") as f:
            for sample in posSamples:
                h = str(self.node2id[sample[0]])
                r = str(self.edge2id[sample[1]])
                t = str(self.node2id[sample[2]])
                f.write(h+' '+r+' '+t+'\n')

    def id2file(self):
        print(os.path.dirname(self.file)+'/entity2id.txt')
        with open(os.path.dirname(self.file)+'/entity2id.txt', 'w') as f:
            for i in texthelper.sortDict(self.node2id, By="value"):
                # print(111)
                f.write(i[0]+' '+str(i[1])+'\n')
        with open(os.path.dirname(self.file)+'/relation2id.txt', 'w') as f:
            for i in texthelper.sortDict(self.edge2id, By="value"):
                f.write(i[0]+' '+str(i[1])+'\n')
    
    @decorator.TimeRecorder
    def tensor(self, debug=Debug):
        nodes_size = len(self.nodes)
        edges_size = len(self.edges)
        print("nodes_size:",nodes_size,"edges_size:",edges_size)
        tensor = []
        triples = self.GetSamples()
        for i in range(edges_size):
            X = np.zeros((nodes_size,nodes_size),dtype=np.int)
            for triple in triples:
                if self.edge2id[triple[1]] == i:
                    X[self.node2id[triple[0]]][self.node2id[triple[2]]] = 1
            tensor.append(csr_matrix(X, dtype=np.int8, shape=(nodes_size, nodes_size)))

if __name__ == "__main__":
    subG1 = "../data/fbtest"
    subG1_helper = DataHelper(subG1)
    subG1_helper.id2file()