import os
import re
import socket
import ssl
import threading


class MyReq:
    def __init__(self):
        self.timeOut = 15
        self.content = bytes()
        self.text = ""
        self.resHeader = {}
        self.Code = 0
        self.redirect = False
        self.url = ""
        self.host = ""
        self.rPath = ""
        self.imgSrc = []
        self.hyperLinks = []

    def baseReq(self, url, headers, method):
        # make a socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(self.timeOut)

        # is https ?
        url = url.strip()
        defaultS = "http"
        if url[:5] == "https":
            s = ssl.wrap_socket(s)
            defaultS = "https"
        port = socket.getservbyname(defaultS, "tcp")

        # make a package
        lineHeader = "{} {} HTTP/1.1".format(method, url)
        tmp = []
        for k, v in headers.items():
            tmp.append("{}:{}".format(k, v))
        headers1 = "\r\n".join(tmp)
        package = "{}\r\n{}\r\n\r\n".format(lineHeader, headers1)

        # connect to a website  send a package
        print("connect to ", headers.get("Host"), port, url)
        s.connect((headers.get("Host"), port))  # connect to url
        s.send(package.encode("utf-8"))  # send package

        # make bytes result
        res = bytes()  # wait response
        while True:
            data = s.recv(1024)
            if data:
                res += data
            else:
                s.close()
                break
        return res

    def Get(self, url, headers=None):
        # http method

        # is a full url ?
        if url[:4] != "http":
            url = "http://" + url

        # get host
        host = re.sub("http.*://", "", url).split("/")[0]
        # is redirect,write forbidden
        if not self.redirect:
            self.host = host
            self.url = url
            self.rPath = re.sub("http.*://.*?/", "", url)
            if self.rPath == self.url:
                self.rPath = ""

        # request header
        if headers is None:
            headers = {
                "Host": host,
                "Connection": "close",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36",
            }

        # true socket request
        byteData = self.baseReq(url, headers, "GET")

        # parse response to get res header and res body
        self.resParse(byteData)

        # if response code == 301 or 302 , send requests to location
        if self.Code in [301, 302]:
            self.redirect = True
            self.Get(self.resHeader.get("Location"))

    def resParse(self, byteBody):
        byteList = byteBody.split("\r\n\r\n".encode("utf-8"))
        resHeader = byteList[0]
        resBody = byteList[1]
        resHeaderLines = resHeader.split("\r\n".encode("utf-8"))

        self.Code = int(resHeaderLines[0].split(" ".encode("utf-8"))[1])
        resHeaderLines.remove(resHeaderLines[0])

        self.resHeader = {}
        for line in resHeaderLines:
            line = line.split(":".encode("utf-8"), 1)
            key = str(line[0], "utf-8")
            value = str(line[1], "utf-8")
            self.resHeader[key] = value.strip()
        self.content = resBody
        try:
            self.text = resBody.decode("utf-8")
        except:
            pass

    def dataProcess(self):
        dirPath = re.sub("http.*://", "", self.linkProcess(self.url))
        dirPath = dirPath.replace("?", "").replace("=", "/").replace(":", "").replace("@", "/")
        if "." in dirPath.split("/")[-1]:
            dirPath = "/".join(dirPath.split("/")[:-1])
            print(dirPath)
        try:
            os.makedirs(dirPath)
        except Exception as e:
            print("!", e)
            pass

        parser = MyHtmlParser()
        parser.feed(self.text)
        for i, v in enumerate(parser.imgSrc):
            parser.imgSrc[i] = self.linkProcess(v).replace(" ", "")
        for i, v in enumerate(parser.hyperLinks):
            parser.hyperLinks[i] = self.linkProcess(v).replace(" ", "")

        self.imgSrc = parser.imgSrc
        self.hyperLinks = parser.hyperLinks

        # for i in self.imgSrc:
        #     urlRecord[i] = 1
        #     t = threading.Thread(target=imgDownloader, args=(i, dirPath))
        #     t.start()

    def linkProcess(self, link):
        if "http" in link:
            return link.strip("/")

        deep = len(self.url.split("/"))
        truePath = "/"
        if ".." in link:
            for i, v in enumerate(link.split("/")):
                if v == "..":
                    deep -= 1
                elif v == ".":
                    pass
                else:
                    truePath += v + "/"
            return ("/".join(self.url.split("/")[:deep]) + truePath).strip("/")
        else:
            # print("!",link)
            return "http://{}/{}".format(self.host, link.strip("/"))

    def pipLine(self, url):
        self.Get(url)
        self.dataProcess()


class MyHtmlParser:
    imgSrc = []
    hyperLinks = []

    def feed(self, source):
        self.imgSrc = re.findall('<img.*src.*=[\"\'](.*)[\"\'].*>', source)
        self.hyperLinks = re.findall('<a.*href.*=[\"\'](.*)[\"\'].*>.*</a>', source)


def imgDownloader(src):
    tmpR = MyReq()

    n = 0
    while n < 10:
        try:
            tmpR.Get(src)
            src = re.sub("http.*?://", "", src)
            # file_name = src.split("/")
            with open("{}".format(src), 'wb+') as f:
                f.write(tmpR.content)
            break
        except:
            # import traceback
            # traceback.print_exc()
            print("retry...")
            n += 1




if __name__ == "__main__":
    startUrl = input("url: ")
    depth = input("depth : ")

    if startUrl == "":
        print(
            "using default url : http://www.feimax.com/images/")
        startUrl = "http://www.feimax.com/images"

    if depth == "":
        print("use default depth: 5 ")
        depth = 5
    else:
        depth = int(depth)

    startUrl = "http://www.feimax.com/images"
    depth = 5

    urlRecord = {}
    start = [startUrl]
    imgSrc = []
    count = 0
    for i in range(depth + 1):
        print(i)
        tmp = []
        for j in start:
            if j in urlRecord:
                continue
            urlRecord[j] = 1
            r = MyReq()
            try:

                r.pipLine(j)
                imgSrc += r.imgSrc
                # print(count)
            except:
                continue

            tmp += r.hyperLinks
        start = tmp
    for i in imgSrc[:]:
        t = threading.Thread(target=imgDownloader, args=(i,))
        t.start()
