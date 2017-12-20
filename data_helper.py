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
#将原始数据后面加上地图块号
def outfile(blockfile_path,rawdata_path,outfile_path):
    d=load_dict(blockfile_path)
    l=change2block(r'res.txt',d)
    outfile_with_block(l,rawdata_path,outfile_path)

#按星期顺序提取每个人的地图格子轨迹
def Extraction_trajectory_by_week(file_with_block,output_file):
    d = {1: 31, 2: 29, 3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}
    dd = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10,
          'Nov': 11, 'Dec': 12}
    with open(file_with_block, encoding='utf-8') as f, open(
            output_file, 'w', encoding='utf-8') as f1:
        this_people = 0
        this_month = ''
        this_week = []
        for line in f.readlines():
            lineArr = line.strip().split('\t')
            block = lineArr[8]
            block=','.join(block.split(' '))
            people = lineArr[0]
            try:
                time = lineArr[7]
            except:
                time = lineArr[6]
            timeArr = time.strip().split(' ')
            # print(timeArr)
            week = timeArr[0]
            month = timeArr[1]
            month = dd[month]
            day = int(timeArr[2])
            if (week == 'Mon'):
                week_start = str(month) + '/' + str(day)
            elif (week == 'Tue'):
                day -= 1
                if (day <= 0):
                    month -= 1
                    if (month <= 0):
                        month = 12
                    day += d[month]
                week_start = str(month) + '/' + str(day)
            elif (week == 'Wed'):
                day -= 2
                if (day <= 0):
                    month -= 1
                    if (month <= 0):
                        month = 12
                    day += d[month]
                week_start = str(month) + '/' + str(day)
            elif (week == 'Thu'):
                day -= 3
                if (day <= 0):
                    month -= 1
                    if (month <= 0):
                        month = 12
                    day += d[month]
                week_start = str(month) + '/' + str(day)
            elif (week == 'Fri'):
                day -= 4
                if (day <= 0):
                    month -= 1
                    if (month <= 0):
                        month = 12
                    day += d[month]
                week_start = str(month) + '/' + str(day)
            elif (week == 'Sat'):
                day -= 5
                if (day <= 0):
                    month -= 1
                    if (month <= 0):
                        month = 12
                    day += d[month]
                week_start = str(month) + '/' + str(day)
            elif (week == 'Sun'):
                day -= 6
                if (day <= 0):
                    month -= 1
                    if (month <= 0):
                        month = 12
                    day += d[month]
                week_start = str(month) + '/' + str(day)
            # print(week_start)
            if (week_start == this_month):
                this_week.append(block)
            else:
                if (len(this_week) > 0):
                    f1.write(this_people + '\t' + '\t'.join(this_week) + '\n')
                    print(len(this_week))
                this_people = people
                this_month = week_start
                this_week = []
                this_week.append(block)

# outfile(r'data\map_block_data\res17.txt',r'data\raw_data\data.txt',r'data\raw_data\data_with_block17.txt')
# Extraction_trajectory_by_week(r'data\raw_data\data_with_block18.txt',r'data/trajectory/traj18.txt')