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
                f.write(temp[0]+'+++++'+temp[1]+'\n')

def get_sample(d,num):
    return random.choice(d[num])
#随机生成负样本,samplenum代表需要生成负样本的记录数
def get_left_sample(d,leftpath,samplenum):
    l=[]
    for i in range(len(d)):
        l.append(i+1)
    with open(leftpath,'w',encoding='utf-8') as f:
        iter=itertools.combinations(l,2)
        l=list(iter)
        random.shuffle(l)
        n = len(l)
        if (n > samplenum):
            l = l[:samplenum]
        for temp in l:
            traj1=get_sample(d,temp[0])
            traj2=get_sample(d,temp[1])
            f.write(traj1 + '+++++'+ traj2 + '\n')
d=createdict(r'data/trajectory/traj18.txt',2)
# get_right_sample(d,r'data/trajectory/traj18+.txt',50)
# get_left_sample(d,r'data/trajectory/traj18-.txt',10000)