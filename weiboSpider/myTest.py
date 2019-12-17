import csv
import datetime
import json
import os
import random
import re
import time
import math
import pyecharts
import requests
import urllib3
from bs4 import BeautifulSoup
from pyecharts import options as opt
from pyecharts.commons.utils import JsCode
import jieba
from collections import Counter
from pyecharts.globals import SymbolType

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class WeiBo:
    def getHeader(self):
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Accept-Encoding": "gzip, deflate, br"
        }
        # 随机请求体
        user_agent_list = [
            "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
            "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15",
        ]

        # 有些页面需要登录才能爬取信息
        # 需要 从 Edge浏览器 登录 m.weibo.com 获得cookie
        # chrome浏览器可能会获取不到
        cookies = [
            "_ga=GA1.2.1786443411.1572615119; _T_WM=51649568104; ALF=1578251148; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhXUmlARsJwXKRD_U1gz9qx5JpX5K-hUgL.FoeN1K2XSoB4eoM2dJLoIEXLxKML1--L12eLxKML1-BLBK2LxK-LBKBLBKMLxKnLBK-LB.qLxKML1KeL1-et; MLOGIN=1; WEIBOCN_FROM=1110006030; SCF=Ah8XD87cbmuICeTdk7Z9PKmZhDhhWuFxD_nBvGDYqtgw4Cl7j-qom00LvDjT7uK1Ha_iisQwLTjYIBvmL4Yai-o.; SUB=_2A25w7zznDeRhGeVJ4lMV9irFyTuIHXVQEESvrDV6PUJbktAKLRjYkW1NT9r6UClQqH97xssPHoPFoCVHCR4nT2o4; SUHB=0WGc7cZ52Vwy2B; SSOLoginState=1575701688; XSRF-TOKEN=9b1881; M_WEIBOCN_PARAMS=oid%3D4446809286461446%26luicode%3D20000061%26lfid%3D4446809286461446%26uicode%3D20000174"
            # "WEIBOCN_FROM=1110006030; M_WEIBOCN_PARAMS=oid%3D4446830295014937%26luicode%3D20000061%26lfid%3D4446830295014937%26uicode%3D20000061%26fid%3D4446830295014937; _T_WM=29566791574; MLOGIN=0; XSRF-TOKEN=98d1c1"
        ]
        headers['User-Agent'] = random.choice(user_agent_list)
        headers["Cookie"] = random.choice(cookies)
        return headers

    def getRealTimeHot(self):
        # 热搜榜接口地址
        url = "https://m.weibo.cn/api/container/getIndex?containerid=106003type%3D25%26t%3D3%26disable_hot%3D1%26filter_type%3Drealtimehot&title=%E5%BE%AE%E5%8D%9A%E7%83%AD%E6%90%9C"
        resp = self.requestGet(url)
        result = []
        for i in range(2):  # 0 为头条 ，1为上升头条
            for item in resp.json()["data"]["cards"][i]["card_group"]:  # 获取感兴趣的信息： 热度，标题，浏览数，讨论数
                try:
                    hot = int(item["desc_extr"])
                except:
                    hot = 0
                tmp = {
                    "title": item["desc"],
                    "hot": hot
                }
                detailUrl = "https://s.weibo.com/weibo?q=%23{}%23&Refer=top".format(item["desc"])  # 热搜榜 浏览数讨论数接口

                try:
                    detail = self.requestGet(detailUrl)  # 请求频繁可能会需要输入验证码，此时跳过
                except:
                    continue
                if detail.status_code == 200:  # 如果电脑端接口没有返回200，尝试使用手机端接口
                    soup = BeautifulSoup(detail.text, 'lxml')
                    infoTag = soup.find("div", class_="total")
                    try:
                        spanList = infoTag.find_all("span")
                    except:
                        tmp["viewNum"] = 0
                        tmp["discussNum"] = 0
                        result.append(tmp)
                        continue
                    infoList = [i.text.replace("阅读", "").replace("讨论", "") for i in spanList]
                else:  # 手机端接口
                    detailUrl = "https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D1%26t%3D10%26q%3D%23{}%23&isnewpage=1".format(
                        item["desc"])
                    detail = self.requestGet(detailUrl)
                    resDict = detail.json()
                    resDictData = resDict["data"]
                    cardListInfo = resDictData["cardlistInfo"]
                    head = cardListInfo["cardlist_head_cards"][0]["head_data"]
                    infoList = head["midtext"].replace("阅读", "").replace("讨论", "").replace("  ", " ").split(" ")[:-1]
                for i, v in enumerate(infoList):
                    if v[-1] == "万":
                        infoList[i] = float(v[:-1]) * 10000
                    elif v[-1] == "亿":
                        infoList[i] = float(v[:-1]) * 100000000
                    else:
                        infoList[i] = float(v)
                tmp["viewNum"] = infoList[0]
                tmp["discussNum"] = infoList[1]
                print(tmp)
                result.append(tmp)
                # time.sleep(0.2)
        return result

    def requestGet(self, url, proxies=None):
        if not proxies:
            resp = requests.get(url, headers=self.getHeader(), verify=False)
        else:
            curProxy = proxies
            if type(proxies) == list:
                curProxy = random.choice(proxies)
            resp = requests.get(url, headers=self.getHeader(), verify=False, proxies=curProxy)
        resp.encoding = "UTF-8"
        return resp

    # 话题榜
    def getTopicRank(self):
        # 话题榜接口
        url = "https://m.weibo.cn/api/container/getIndex?containerid=106003type%3D25%26t%3D3%26disable_hot%3D1%26filter_type%3Dtopicband&title=%E5%BE%AE%E5%8D%9A%E7%83%AD%E6%90%9C"
        resp = self.requestGet(url)
        result = []
        for item in resp.json()["data"]["cards"][0]["card_group"][:-1]:  # 感兴趣的信息
            tmp = {
                "title": item["title_sub"],
                "desc": item["desc1"],
            }
            count = item["desc2"]
            infoList = count.replace("讨论", "").replace("阅读", "").replace("  ", " ").strip().split(" ")
            for i, v in enumerate(infoList):
                if v[-1] == "万":
                    infoList[i] = float(v[:-1]) * 10000
                elif v[-1] == "亿":
                    infoList[i] = float(v[:-1]) * 100000000
                else:
                    infoList[i] = float(v)
            tmp["viewNum"] = math.ceil(infoList[1])
            tmp["discussNum"] = math.ceil(infoList[0])
            result.append(tmp)
        return result

    # 新时代榜单
    def getGovBandRank(self):
        result = []
        # 接口地址
        url = "https://m.weibo.cn/api/container/getIndex?containerid=106003type%3D25%26t%3D3%26disable_hot%3D1%26filter_type%3Dgovband&title=%E5%BE%AE%E5%8D%9A%E7%83%AD%E6%90%9C&page={}"
        currentPage = 1

        # 循环获取每页内容 直到页面返回 ok=0
        while True:
            resp = self.requestGet(url.format(currentPage))

            if resp.json()["ok"] == 0:
                break
            for item in resp.json()["data"]["cards"][0]["card_group"]:
                tmp = {
                    "title": item["title_sub"],
                    "desc": item["desc1"],
                }
                count = item["desc2"]
                host = count.split("|")[-1].strip()
                count = count.split("|")[0]
                infoList = count.replace("讨论", "").replace("阅读", "").replace("  ", " ").strip().split(" ")
                for i, v in enumerate(infoList):
                    if v[-1] == "万":
                        infoList[i] = float(v[:-1]) * 10000
                    elif v[-1] == "亿":
                        infoList[i] = float(v[:-1]) * 100000000
                    else:
                        infoList[i] = float(v)
                tmp["viewNum"] = infoList[1]
                tmp["discussNum"] = infoList[0]
                tmp["host"] = host
                result.append(tmp)
            currentPage += 1
            time.sleep(2)
        return result

    # 获取单个微博信息， 默认获取最大评论数为200条，innerCommentNum为200条，这个指的是楼中楼回复
    def getWeiBoItem(self, url, commentNum=200, innerCommentNum=200):
        resp = self.requestGet(url)
        # print(url)
        reStr = re.findall(r"render_data = (.*?)\[0\]", resp.text, re.S)[0]  # 正则获取script标签里面的内容， 因为正文信息直接返回在html里面
        itemInfo = json.loads(reStr)[0]

        result = {
            "comments_count": itemInfo["status"]["comments_count"],
            "attitudes_count": itemInfo["status"]["attitudes_count"],
            "reposts_count": itemInfo["status"]["reposts_count"],
            "text": BeautifulSoup(itemInfo["status"]["text"], 'lxml').text,
            "user": {
                "name": itemInfo["status"]["user"]["screen_name"],
                "fans": itemInfo["status"]["user"]["followers_count"],
                "id": itemInfo["status"]["user"]["id"],
            },
            "comments": []
        }

        # print(result)


        # 评论接口
        originUrl = "https://m.weibo.cn/comments/hotflow?id={}&mid={}&max_id_type=0"
        startCommentUrl = originUrl.format(itemInfo["status"]["id"], itemInfo["status"]["mid"])



        # 循环获取每页评论
        while True:

            resp = requests.get(startCommentUrl, headers=self.getHeader(), verify=False)
            resp.encoding = "GBK"
            try:
                print(startCommentUrl)
                resDict = resp.json()
            except Exception as e:
                print(e)
                #print(startCommentUrl)
                time.sleep(2)
                continue

            if resDict["ok"] == 0:
                break

            try:
                for item in resDict["data"]["data"]:
                    text = BeautifulSoup(item["text"], 'lxml').text
                    result["comments"].append(text)
                    # 如果有楼中楼回复
                    if "comments" in item and item["comments"]:
                        if item["total_number"] > 2:  # 楼中楼回复次数大于2
                            # 从楼中楼接口获取详细信息
                            self.getInnerComment(item["id"], result, innerCommentNum)
                        else:
                            # 直接获取信息
                            for innerItem in item["comments"]:
                                text = BeautifulSoup(innerItem["text"], 'lxml').text
                                result["comments"].append(text)
            except Exception as e:
                import traceback
                traceback.print_exc()
                break
            if len(result["comments"]) >= commentNum:
                break
            startCommentUrl = startCommentUrl + "&max_id={}".format(resDict["data"]["max_id"])
            time.sleep(1)
        return result

    # 获取楼中楼信息
    def getInnerComment(self, id, result, innerCommentNum=200):
        # 接口
        innerCommentUrl = "https://m.weibo.cn/comments/hotFlowChild?cid={}&max_id={}&max_id_type=0"
        currentPage = 0
        currentPageId = id
        innerCount = 0
        # 循环获取每页信息
        while True:
            url = innerCommentUrl.format(currentPageId, currentPage)  # 构造接口
            resp = self.requestGet(url)
            try:
                resDict = resp.json()
            except Exception as e:
                break
            for t in resDict["data"]:
                text = BeautifulSoup(t["text"], 'lxml').text
                if ":" in text:
                    text = "".join(BeautifulSoup(t["text"], 'lxml').text.split(":")[1:])
                if text:
                    result["comments"].append(text)
            currentPage = resDict["max_id"]
            if innerCount >= innerCommentNum or currentPage == 0:
                break
            time.sleep(0.5)

    # 保存csv
    def saveCsv(self, data, path):
        now = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S") # 时间格式化
        headers = data[0].keys()
        try:
            os.makedirs("{}".format(path))
        except:
            pass
        with open("{}/{}.csv".format(path, now), 'w+', encoding="utf-8-sig", newline='') as f:
            writer = csv.DictWriter(f, headers)
            writer.writeheader()
            for row in data:
                writer.writerow(row)
        print("data has been save to {}/{}.csv".format(path, now))

    # 保存txt
    def saveTxt(self, data, path):
        now = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        try:
            os.makedirs("{}".format(path))
        except:
            pass
        with open("{}/{}.txt".format(path, now), 'w+', encoding="utf-8") as f:
            f.write(data["text"] + "\n\n\n")
            for i in data["comments"]:
                f.write(i + "\n\n")

        print("data has been save to {}/{}.txt".format(path, now))

    # 讨论数以及阅读数
    def drawViewDiscussRank(self, inputData, showNum=15, size=None, sub=True):
        x = []
        y1 = []
        y2 = []
        inputData = sorted(inputData, key=lambda x: x["viewNum"], reverse=True)
        for i in inputData:
            x.append(i["title"])
            y1.append(math.ceil(i["viewNum"] / 10000))
            y2.append(math.ceil(i["discussNum"] / 10000))

        if sub:
            formatJsCode = JsCode("(a,b,c)=> a.length-2 >= 7 ? a.substring(1,6) + '...': a.substring(1,a.length-1)")
        else:
            formatJsCode = JsCode("(a,b,c)=> a.length-2 >= 7 ? a.substring(0,6) + '...': a")

        x = x[:showNum]
        y1 = y1[:showNum]

        if size:
            bar1 = pyecharts.charts.Bar(init_opts=opt.InitOpts(height=size["height"], width=size["width"]))
        else:
            bar1 = pyecharts.charts.Bar()
        bar1.add_xaxis(x)
        bar1.add_yaxis("阅读量(万)", y1)
        bar1.set_global_opts(title_opts=opt.TitleOpts(title="阅读量排行榜"),
                             xaxis_opts=opt.AxisOpts(
                                 axislabel_opts=opt.LabelOpts(rotate=30, formatter=formatJsCode)))

        if size:
            bar2 = pyecharts.charts.Bar(init_opts=opt.InitOpts(height=size["height"], width=size["width"]))
        else:
            bar2 = pyecharts.charts.Bar()
        bar2.add_xaxis(x)
        y2 = y2[:showNum]
        y2 = sorted(y2, reverse=True)
        bar2.add_yaxis("讨论量(万)", y2, )
        bar2.set_global_opts(title_opts=opt.TitleOpts(title="讨论量排行榜"),
                             xaxis_opts=opt.AxisOpts(
                                 axislabel_opts=opt.LabelOpts(rotate=30, formatter=formatJsCode)))
        return bar1, bar2

    # 热度榜
    def drawHotRank(self, inputData, showNum=15, size=None):
        x = []
        y = []
        for i in inputData:
            x.append(i["title"])
            y.append(i["hot"])
        if size:
            bar = pyecharts.charts.Bar(init_opts=opt.InitOpts(height=size["height"], width=size["width"]))
        else:
            bar = pyecharts.charts.Bar(init_opts=opt.InitOpts(height="600px", width="900px"))
        formatJsCode = JsCode("(a,b,c)=> a.length-2 >= 7 ? a.substring(0,6) + '...': a")    # pyecharts的format需要使用js代码， 这个代码的意思是 如果字符长度超过7，就截取前6个， 缩略表示
        bar.add_xaxis(x[:showNum])
        y = sorted(y, reverse=True)
        bar.add_yaxis("热度", y[:showNum])
        bar.set_global_opts(title_opts=opt.TitleOpts(title="热度排行榜"),
                            xaxis_opts=opt.AxisOpts(
                                axislabel_opts=opt.LabelOpts(rotate=30, formatter=formatJsCode)))
        return bar

    # 词云图
    def drawWordCloud(self, inputData, size=None, userWord=None):
        if size:
            c = pyecharts.charts.WordCloud(init_opts=opt.InitOpts(height=size["height"], width=size["width"]))
        else:
            c = pyecharts.charts.WordCloud()
        s = "\n".join(inputData["comments"])
        stop = []
        if userWord:
            for i in userWord:
                jieba.add_word(i)
        with open("停用词.txt", 'r', encoding="utf-8") as f:
            for i in f:
                stop.append(i.strip())
        realList = []
        for i in jieba.cut(s, cut_all=False):
            tmp = str(i).strip()
            if tmp not in stop and len(tmp) >= 2:
                realList.append(str(i).strip())

        counter = Counter(realList)  # 获得单词和词频
        num = 50
        if len(counter) < num:
            num = len(counter)
        c.add("", counter.most_common(num), word_size_range=[10, 100], shape=SymbolType.DIAMOND)
        return c


if __name__ == "__main__":
    WeiBo().getWeiBoItem("https://m.weibo.cn/detail/4446809286461446")
