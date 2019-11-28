import socket
import multiprocessing
import threading
import struct
import random
import json
import copy


class Node:

    def __init__(self, initTable, portTable):
        self.portTable = portTable
        self.node = initTable[0]
        self.neighbors = [k for k in initTable[1].keys()]
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        port = self.portTable.get(self.node)
        # print(("127.0.0.1", port))
        self.s.bind(("127.0.0.1", port))
        self.dv = {}
        self.messageQueue = []

        # 如果1秒内没有收到任何消息，说明已经收敛
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_RCVTIMEO, 1000)

        for k, v in initTable[1].items():
            self.dv[k] = {
                "distance": v,
                "pass": []
            }

    def makeServer(self):
        while True:
            try:
                data, addr = self.s.recvfrom(2048)
            except TimeoutError as e:
                # 收敛之后开始保存自己的dv表
                self.saveDv()
                self.s.close()
                return

            t = self.unpack(data)
            # print("***")
            # print(self.node, "recv from", t[0], t)
            a = copy.deepcopy(self.getDvTable(False))
            # print("current:", a)
            flag = self.compare(t, self.getDvTable(False))
            # print("compare:", flag)
            if flag:
                # print("compareResult: ", self.getDvTable(False))
                self.sendDv()
            # print("***")

    def saveDv(self):
        with open("output/{}.txt".format(self.node), "w+", encoding="utf-8") as f:
            a = self.getDvTable(False)
            for i in a[1].items():
                start = a[0]
                end = i[0]
                distance = i[1]["distance"]
                tmpWay = [start] + i[1]["pass"] + [end]
                passWay = "->".join(tmpWay)
                fmt = "{} 到 {} 的最短距离为 {} ： 经过路径为 {}".format(start, end, distance, passWay)
                f.write(fmt + "\n")

    def compare(self, aNode, bNode):
        a = copy.deepcopy(aNode)
        b = copy.deepcopy(bNode)
        update = False
        if a[0] not in a[1].keys():
            b[1][a[0]] = a[1][b[0]]

        for key in a[1].keys():
            distance = a[1].get(key)["distance"] + b[1].get(a[0])["distance"]
            if key in b[1].keys():
                if distance < b[1].get(key)["distance"]:
                    b[1].get(key)["distance"] = distance
                    b[1].get(key)["pass"] = [a[0]] + b[1].get(a[0])["pass"] + a[1].get(key)["pass"]
                    # b[1].get(key)["pass"].append(a[0])
                    update = True
            elif key != b[0]:
                tmp = copy.deepcopy(a[1].get(key))
                tmp["distance"] = distance
                tmp["pass"] = b[1].get(a[0]).get("pass") + [a[0]]
                # tmp["pass"] = [a[0]] + b[1].get(a[0])["pass"]
                # tmp["pass"].append(a[0])
                b[1][key] = tmp
                update = True
        if update:
            self.dv = b[1]

        return update

    def sendDv(self):
        for i in self.neighbors:
            self.s.sendto(self.pack(), ("127.0.0.1", self.portTable.get(i)))

    def getDvTable(self, string=True):
        t = [self.node, self.dv]
        if string:
            return json.dumps(t)
        return t

    def pack(self):
        data = self.getDvTable()
        fmt = "i{}s".format(len(data))
        result = struct.pack(fmt, len(data), bytes(data, encoding="utf-8"))
        return result

    def unpack(self, data):
        length = struct.unpack_from("i", data, 0)
        byteData = struct.unpack_from("{}s".format(length[0]), data, 4)
        return json.loads(str(byteData[0], encoding="utf-8"))

    def start(self):
        threading.Thread(target=self.makeServer).start()


def startProcess(node):
    node.start()


if __name__ == "__main__":
    f = open("data1.json")
    nodeMsg = json.load(f)
    f.close()
    portTable = {}
    numTable = {}
    n = 0
    for k, v in nodeMsg.items():
        port = random.randint(30000, 65535)
        portTable[k] = port
        numTable[k] = n
        n += 1

    nlist = []
    lock = multiprocessing.Lock()
    pList = []
    for i in nodeMsg.items():
        node = Node(i, portTable)
        nlist.append(node)
        p = multiprocessing.Process(target=startProcess, args=(node,))
        pList.append(p)
        p.start()

    nlist[0].sendDv()
    for i in pList:
        i.join()
