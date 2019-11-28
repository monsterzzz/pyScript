# a = ['A', {'B': {'distance': 6, 'pass': []}, 'E': {'distance': 1, 'pass': []}}]
# b = ["B", {"A": {"distance": 6, "pass": []}, "E": {"distance": 8, "pass": []}, "C": {"distance": 1, "pass": []}}]
# c = ["C", {"B": {"distance": 1, "pass": []}, "D": {"distance": 2, "pass": []}}]
# d = ["D", {"C": {"distance": 2, "pass": []}, "E": {"distance": 2, "pass": []}}]
# e = ['E', {'A': {'distance': 1, 'pass': []}, 'B': {'distance': 8, 'pass': []}, 'D': {'distance': 2, 'pass': []}}]
import copy
a = ['F', {'A': {'distance': 3, 'pass': []}, 'B': {'distance': 2, 'pass': ['A']}, 'C': {'distance': 1, 'pass': []}}]
b = ['A', {'B': {'distance': 6, 'pass': []}, 'E': {'distance': 1, 'pass': []}, 'C': {'distance': 5, 'pass': ['E', 'D']}, 'D': {'distance': 3, 'pass': ['E']}}]


def compare(aNode, bNode):
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
            # tmp["pass"].append(a[0])
            b[1][key] = tmp
            update = True
    print(b)
    return update

#
# print(a)
# print(b)
# compare(a, b)




# import socket,struct,json
#
# s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
# s.bind(("127.0.0.1",5685))
# t = json.dumps(['F', {'A': {'distance': 3, 'pass': []}, 'B': {'distance': 2, 'pass': ['A']}, 'C': {'distance': 1, 'pass': []}}])
# fmt = "i{}s".format(len(t))
# d = struct.pack(fmt,len(t),bytes(t,encoding="utf-8"))
# s.sendto(d,('127.0.0.1', 34537))


a = ['E', {'A': {'distance': 1, 'pass': []}, 'B': {'distance': 5, 'pass': ['D', 'C']}, 'D': {'distance': 2, 'pass': []}, 'C': {'distance': 4, 'pass': ['D']}}]

for i in a[1].items():
    start = a[0]
    end = i[0]
    distance = i[1]["distance"]
    tmpWay = [start] + i[1]["pass"] + [end]
    passWay = "->".join(tmpWay)
    fmt = "{} 到 {} 的最短距离为 {} ： 经过路径为 {}".format(start,end,distance,passWay)
    print(fmt)
# a = [True,True,True,True,True]
# b = [False,False,False,False,True]
# print(any(a),any(b))
# print(a)
# print(b)
# compare(a, b)
# print(a)
# print(b)
# print()
# print(b)
# print(c)
# compare(b, c)
# print(b)
# print(c)
# print()
# print(c)
# print(d)
# compare(c, d)
# print(c)
# print(d)
# print()
# print(d)
# print(e)
# compare(d, e)
# print(d)
# print(e)
