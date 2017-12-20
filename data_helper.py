import itertools
import random

#生成dict{1:[轨迹1,序列,轨迹2序列,轨迹3序列]} mintraj表示最短序列值
def createdict(path,mintraj):
    d={}
    with open(path,encoding='utf-8') as f:
        for line in f.readlines():
            lineArr=line.strip().split('\t')
            num=int(lineArr[0])
            temp=lineArr[1:]
            if(len(temp)<mintraj):
                continue
            trac=' '.join(lineArr[1:])
            if(d.get(num) == None):
                d[num]=[]
            d[num].append(trac)
    return d

#生成正样本  maxnum表示每个人最大生成的正样本数量
def get_right_sample(d,rightpath,maxnum):
    with open(rightpath,'w',encoding='utf-8') as f:
        for key,value in d.items():
            iter = itertools.combinations(value, 2)
            l=list(iter)
            random.shuffle(l)
            n=len(l)
            if(n>maxnum):
                l=l[:maxnum]
            for temp in l:
                f.write(str(key)+'\t'+temp[0]+'+++++'+temp[1]+'\n')

d=createdict(r'data/trajectory/traj18.txt',2)
get_right_sample(d,r'data/trajectory/traj18+.txt',50)