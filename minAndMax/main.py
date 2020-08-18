import os
import time
import re
import numpy

def main():

    # init  
    fileDir = "data"  # input data dir
    minX = 845        # min x value
    maxX = 865        # max x value
    outputType = "txt"   # output file type, txt or csv
    #outputType = "csv"


    # make output dir 
    f_dir = os.path.split(os.path.realpath(__file__))[0] + "\\" + "output"
    try:
        os.mkdir(f_dir)
    except:
        pass
    
    # find shape 
    listDir = os.listdir(fileDir)
    shape = {}
    for i in listDir:
        tmp = re.findall(r"full_edge_(.*?)_(.*?).txt",i)[0][0]
        if int(tmp) not in shape:
            shape[int(tmp)] = []
        shape[int(tmp)].append(i)
    
    # find maxY of edgeFile
    result = []
    for i in sorted(shape.keys(),reverse = False):
        currenEdgeMaxY = []
        for fileName in sorted(shape[i],key = lambda x : (int(re.findall(r"_(\d*?).txt",x)[0]))):
            with open(f"{fileDir}/{fileName}","r",encoding="utf-8") as f:
                maxY = 0
                count = 1
                for line in f:
                    x,y = line.strip().split()
                    x = float(x)
                    y = float(y)
                    if count == 1:
                        maxY = y
                    if x < 845:
                        continue
                    if x > 865:
                        break
                    if y > maxY:
                        maxY = y
                currenEdgeMaxY.append(maxY)
                print(maxY,fileName)
        result.append(currenEdgeMaxY)
         
    currentTime = time.strftime("%Y%m%d%H%M", time.localtime(time.time()))
    arr = numpy.array(result)
    arr = numpy.around(arr.T,decimals=8)
    numpy.savetxt(f"output/{currentTime}.txt",arr,delimiter=",", fmt='%.08f')


if __name__ == '__main__':
    main()
   
