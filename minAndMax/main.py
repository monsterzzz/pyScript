import os
import time

fileDir = input("please input the dir of file: ").strip("/")
minNum = float(input("please input the min number: "))
maxNum = float(input("please input the max number: "))
currentTime = time.strftime("%Y%m%d%H%M", time.localtime(time.time()))


def readXY(line_string):
    return line_string.strip().split()


def findCurrentFileMinMax(file_path, save_path):
    with open(file_path, "r") as f:
        wantedX, wantedY = -1, -1
        for line in f:
            x, y = readXY(line)
            x = float(x)
            y = float(y)
            if minNum < x < maxNum and y > wantedY:
                wantedY = y
                wantedX = x
            if x >= maxNum:
                break
    with open(save_path, "a+") as f:
        f.write("{} {}\n".format(wantedX, wantedY))


def main():

    f_dir = os.path.split(os.path.realpath(__file__))[0] + "\\" + "output"

    try:
        os.mkdir(f_dir)
    except:
        pass

    listDir = os.listdir(fileDir)
    listDir = sorted(listDir, key=lambda x: int(x.split(".")[0]))

    for fileName in listDir:
        findCurrentFileMinMax(fileDir + "/" + fileName, "{}/{}.txt".format(f_dir,currentTime))

    print("calc over!")
    print("output dir is in {}".format(f_dir))


if __name__ == '__main__':
    main()

