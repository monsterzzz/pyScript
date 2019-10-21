import os

fileDir = input("please input the dir of file: ").strip("/")
minNum = float(input("please input the min number: "))
maxNum = float(input("please input the max number: "))
wantedX = -1
wantedY = -1


def readXY(line_string: str):
    return line_string.strip().split()


def findCurrentFileMinMax(file_path):
    global wantedX, wantedY
    with open(file_path, "r") as f:
        for line in f:
            x, y = readXY(line)
            x = float(x)
            y = float(y)
            if minNum < x < maxNum and y > wantedY:
                wantedY = y
                wantedX = x
            if x >= maxNum:
                break


def main():
    global wantedX, wantedY
    listDir = os.listdir(fileDir)
    for fileName in listDir:
        findCurrentFileMinMax(fileDir + "/" + fileName)
    print(wantedX, wantedY)


if __name__ == '__main__':
    main()
