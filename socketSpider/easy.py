import os

import requests
from html.parser import HTMLParser


class MyHtmlParser(HTMLParser):
    stack = []
    pureContent = []
    currentTag = ""
    imgTag = []
    hyperLinks = []

    def error(self, message):
        pass

    def handle_starttag(self, tag, attrs):
        if tag.lower() in ["div", "table"]:
            self.stack.append(tag)
        self.currentTag = tag

        if tag == "a":
            for i in attrs:
                tmp = i[1].strip("//")
                if i[0] == "href" and tmp != "" and tmp != "javascript:;":
                    self.hyperLinks.append(tmp)
                    break

        if tag == "img":
            tmp = []
            for i in attrs:
                tmp.append("{}={}".format(i[0], i[1]))
            self.imgTag.append("<img {} />".format(" ".join(tmp)))
        #

    def handle_endtag(self, tag):
        if tag in ["div", "table"]:
            self.stack.pop()
        # if tag == "img":
        #     self.imgTag.append("")

    def handle_data(self, data):
        if self.stack and self.currentTag.lower() not in ["script", "links", "style"]:
            lineContent = data.strip().replace("\n", "")
            if lineContent:
                self.pureContent.append(lineContent)

    def getPureContent(self):
        return "\n".join(self.pureContent)

    def getImgTag(self):
        return "\nImg Tags :\n{}".format("\n".join(self.imgTag))

    def getHyperLinks(self):
        return "\nHyper Links :\n{}".format("\n".join(self.hyperLinks))


if __name__ == "__main__":
    url = "https://www.baidu.com"
    r = requests.get(url, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36"})
    r.encoding = "utf-8"
    host = url.split("//")
    try:
        os.mkdir(host[-1])
    except:
        pass
    with open("{}/{}.html".format(host[-1], host[-1]), "wb+") as f:
        f.write(r.content)

    parse = MyHtmlParser()
    parse.feed(r.text)
    print(parse.getPureContent())
    print(parse.getImgTag())
    print(parse.getHyperLinks())
