class SafeMap:
    def __init__(self, iptStr):
        self.initMap = self.ipt2list(iptStr)
        self.output = []

    def ipt2list(self, iptStr):
        unsafeMap = []
        for line in iptStr.strip().split("\n"):
            tmp = []
            for cell in line:
                tmp.append(int(cell))
            unsafeMap.append(tmp)
        return unsafeMap

    def isSafeCell(self, x, y):
        try:
            if x < 0 or y < 0:
                raise IndexError
            return self.initMap[x][y] == 0
        except IndexError:
            return True

    def isSafeAround(self, x, y):
        N = 3
        startX = x - int(N / 2)
        startY = y - int(N / 2)

        currentX = startX
        currentY = startY
        for i in range(N):
            for j in range(N):
                if not self.isSafeCell(currentX, currentY):
                    return False
                currentX += 1
            currentY += 1
            currentX = startX
        return True

    def genSafeMap(self):
        # output = [["." for i in range(len(self.initMap[0]))] for i in range(len(self.initMap)) ]
        output = []
        safePos = []

        for x in range(len(self.initMap)):
            tmp = []
            for y in range(len(self.initMap[x])):
                if not self.isSafeCell(x, y):
                    tmp.append("#")
                elif not self.isSafeAround(x, y):
                    tmp.append("0")
                else:
                    safePos.append((x, y))
                    tmp.append("1")
            output.append(tmp)

        self.output = output

        for i in safePos:
            if self.find5Level(safePos, i):
                output[i[0]][i[1]] = "2"

        return "\n".join(list(map(lambda x: "".join(x), output)))

    def find5Level(self, safePos, currentPos):
        startX = currentPos[0] - 1
        startY = currentPos[1] - 1
        currentX = startX
        currentY = startY
        for j in range(3):
            for k in range(3):
                if (currentX, currentY) not in safePos:
                    try:
                        if currentX < 0 or currentY < 0:
                            raise IndexError
                        _ = self.output[currentX][currentY]
                        return False
                    except IndexError:
                        pass
                currentX += 1
            currentY += 1
            currentX = startX
        return True


if __name__ == '__main__':
    # with open("input.txt", 'r') as f:
    #     data = f.read()

    firstLine = input()
    n = len(firstLine)
    firstLine += "\n"

    while True:
        if n == 1:
            break
        else:
            tmp = input()
            firstLine += tmp + "\n"
            n -= 1
    data = firstLine

    a = SafeMap(data).genSafeMap()
    print(a)
