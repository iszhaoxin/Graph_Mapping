import os, time
from datahelper import DataHelper
from multiprocessing import Pool

class Prepare:
    def __init__(self, datafn):
        self.datafn     = datafn
        self.test       = [['m.01t94_1'], ['m.05zr0xl'], ['m.016z7s']]
        
    def _keys(self, fn):
        helper = DataHelper(fn)
        if not os.path.isfile('../data/middle/entity2id.txt'):
            helper.id2file()
        return list(helper.node2id.keys())

    def _search(self, keys, fn):
        new   = open('../data/results/'+fn, 'w')
        lines = open(self.datafn, 'r').readlines()
        for i in lines:
            spl   = i.split()
            back  = spl[-2][28:-1]
            for key in keys:
                key = '.'.join(key.split('/'))[1:]
                # print(key,back)
                if back == key:
                    new.write(i)
        new.close()

    def search(self, keys, parall):
        arguement = list(zip(keys,map(str,list(range(parall)))))
        with Pool(parall) as pool:
            pool.starmap(self._search, arguement)

    def check(self, testkeys):
        self._search(testkeys, '../../test')
        
def main():
    parall  = 3
    p       = Prepare('../data/raw/DBs-FBs(all)')
    keys    = p._keys('../data/raw/FB15K')
    # index   = list(range(0, len(keys), int(len(keys)/parall)))
    # index.append(-1)
    # indexs  = list(zip(index[:-1],index[1:]))
    # # keys       = [['/m/01t94_1'], ['/m/05zr0xl'], ['/m/016z7s']]
    # keys    = [keys[s:e] for s,e in indexs]
    # p.search(keys, parall)
    

def DB_FB():
    new =  open('../data/all2', 'w')
    with open('../data/all', 'r') as f:
        for l in f:
            db, fb = l.split()
            fb = '/'+fb.replace('.','/')
            new.write(db+' '+fb+'\n')
    new.close()

def file2dict(fn, direction=True):
    d = dict()
    if direction==True:
        with open(fn, 'r') as f:
            for l in f:
                key, value = l.split()
                # print(key)
                if key in d:
                    if value not in d[key]:
                        d[key].append(value)
                else:
                    d.update({key:[value]})
    else:
        with open(fn, 'r') as f:
            for l in f:
                value, key = l.split()
                # print(key)
                if key in d:
                    if value not in d[key]:
                        d[key].append(value)
                else:
                    d.update({key:[value]})
    return d

def FB_DBs():
    d = file2dict('../data/middle/DB-FB(15k)', direction=False)
    with open('../data/FB-DBs(15KOnetoMany)', 'w') as f:
        for k in d.keys():
            f.write(k+' ')
            for i in d[k]:
                f.write(i+' ')
            f.write('\n')
        
def DB_FBs():
    d = file2dict('../data/middle_data/DB-FB(15K)', direction=True)
    with open('../data/DB_FBs(15KOnetoMany)', 'w') as f:
        for k in d.keys():
            f.write(k+' ')
            for i in d[k]:
                f.write(i+' ')
            f.write('\n')
    
def DuplicateRemove(fn, w):
    d = dict()
    if w == 'withWiki':
        new = open('../../data/results/withWiki/DB15K+_rd', 'w') 
    else:
        new = open('../../data/results/withoutWiki/DB15K+_rd', 'w') 
    with open(fn, 'r') as f:
        for l in f:
            if l not in d:
                try:
                    h,r,t = l.split()
                    if w == 'withWiki':
                        new.write(l)
                        d.update({l:1})
                    else:
                        if 'wikiPage' not in r:
                            new.write(l)
                            d.update({l:1})
                except:
                    print(l.split())
                    print(l)
                    print('---------------')
    new.close()

if __name__ == "__main__":
    # p = Prepare('../data/datan')
    # testkeys = ['/m/05lx3']
    # p.check(testkeys)
    # DB_FBs()

    fn = "../../data/results/DB15K+"
    DuplicateRemove(fn, 'withWiki')
    DuplicateRemove(fn, 'withoutWiki')

    # helper = DataHelper("/home/dreamer/codes/my_code/subGraph/data/results/withWiki/DB15K_rd")
    # helper.id2file()
        