def load_dict(path):
    d={}
    with open(path,encoding='utf-8') as f:
        for line in f.readlines():
            lineArr=line.strip().split(',')
            key=' '.join(lineArr[:2])
            value=' '.join(lineArr[2:])
            d[key]=value
    return d

def change2block(path,d):
    l=[]
    with open(path,encoding='utf-8') as f1:
        for line in f1.readlines():
            lineArr=line.strip().split(',')
            value=lineArr[1:]
            temp=value[0]
            value[0]=value[1]
            value[1]=temp
            value=' '.join(value)
            block=d[value]
            l.append(block)
    return l
def outfile_with_block(block,path,outpath):
    with open(path,encoding='utf-8') as f:
        lines=f.readlines()
    with open(outpath,'w',encoding='utf-8') as f:
        for i in range(len(block)):
            line=lines[i].strip()
            f.write(line+'\t'+block[i]+'\n')
def outfile(blockfile_path,rawdata_path,outfile_path):
    d=load_dict(blockfile_path)
    l=change2block(r'res.txt',d)
    outfile_with_block(l,rawdata_path,outfile_path)

# outfile(r'data\map_block_data\res17.txt',r'data\raw_data\data.txt',r'data\raw_data\data_with_block17.txt')
