import random
import numpy as np
import pandas as pd
import jieba

# 载入语料
raw = pd.read_csv("sd.txt",
                  names=['txt'], sep='aaa', encoding="utf-8", engine='python')


# 章节判断用变量预处理
def m_head(tmpstr):
    return tmpstr[:1]


def m_mid(tmpstr):
    return tmpstr.find("回 ")


raw['head'] = raw.txt.apply(m_head)
raw['mid'] = raw.txt.apply(m_mid)
raw['len'] = raw.txt.apply(len)
# 章节判断
chapnum = 0
for i in range(len(raw)):
    if raw['head'][i] == "第" and raw['mid'][i] > 0 and raw['len'][i] < 30:
        chapnum += 1
    if chapnum >= 40 and raw['txt'][i] == "附录一：成吉思汗家族":
        chapnum = 0
    raw.loc[i, 'chap'] = chapnum

# 删除临时变量
del raw['head']
del raw['mid']
del raw['len']

rawgrp = raw.groupby('chap')
chapter = rawgrp.agg(sum)  # 只有字符串列的情况下，sum函数自动转为合并字符串


# chapter = chapter[chapter.index != 0]

def getOneChapWord(idx):
    # 取出特定的某一回
    chapidx = idx
    raw[raw.chap == chapidx]
    tmpchap = raw[raw.chap == chapidx].copy()

    alltxt = "".join(tmpchap.txt[1:])
    dict = '金庸小说词库.txt'
    jieba.load_userdict(dict)  # dict为自定义词典的路径
    tmpdf = pd.read_csv('停用词.txt',
                        names=['w'], sep='aaa', encoding='utf-8', engine='python')
    # 分词
    # word_list = jieba.lcut(chapter.txt[1])
    # word_list[:10]
    word_list = [w for w in jieba.cut(alltxt) if w not in list(tmpdf.w)]
    return word_list


lines = []

dict = '金庸小说词库.txt'
jieba.load_userdict(dict)  # dict为自定义词典的路径
tmpdf = pd.read_csv('停用词.txt',
                    names=['w'], sep='aaa', encoding='utf-8', engine='python')


def splitChap(idx):
    choice = []
    noChoice = []
    tmpchap = raw[raw.chap == idx].copy()
    wordResult = []
    tmpchapLen = len(tmpchap.txt[1:])
    door = tmpchapLen * 0.4
    print(door,tmpchapLen)
    for i, v in enumerate(tmpchap.txt[1:]):
        alltxt = v

        if i <= door:
            choice.append(i)
        else:
            noChoice.append(i)
        # 分词
        # word_list = jieba.lcut(chapter.txt[1])
        # word_list[:10]
        word_list = [w for w in jieba.cut(alltxt) if w not in list(tmpdf.w)]
        wordResult.append(word_list)
    return choice, noChoice, wordResult


def load_data_set(part1, c1, part2, c2):
    posting_list = []
    labels = []
    for i in c1:
        posting_list.append(part1[i])
        labels.append(0)
    for i in c2:
        posting_list.append(part2[i])
        labels.append(1)
    # print(c1,c2)
    # print(posting_list)
    # print(labels)
    return posting_list, labels


def create_vocab_list(dataset):
    # dataset 包含了多条留言的文本，每一条留言为一个列表
    vocabset = set([])
    for document in dataset:
        vocabset = vocabset | set(document)
    # print(vocabset)
    return list(vocabset)


def wordsToVector(vocabset, inputset):
    # vocabset 是词汇表， inputset 为要转化为向量的文本
    vector = [0] * len(vocabset)
    for word in inputset:
        if word in vocabset:
            vector[vocabset.index(word)] = 1
        # else:
        #     print("The word: {} is not in my Vocabulary.".format(word))
    # print(vector)
    return vector


def traing_bayes(trainset, trainCategory):
    """sovle the conditional probility"""
    # trainCategory 是标记为负类和正类的向量
    num_train = len(trainset)
    # 获取训练集的数量，其中训练集是由文本向量组成
    num_vocab = len(trainset[0])
    # 由于训练集中的每个元素都是文本向量，即包含了整个词汇表

    pAbusive = sum(trainCategory) / num_train
    # 计算负类的概率，负类的数量除以训练集的数目

    pnorm_vector = np.ones(num_vocab)
    # 每个词汇出现在正类中的概率组成的向量
    pabu_vector = np.ones(num_vocab)
    # 每个词汇出现在负类中的概率组成的向量

    pnorm_denom = 2.0
    # 正类中词汇的数目
    pabu_denom = 2.0
    # 负类中词汇的数目

    for i in range(num_train):
        if trainCategory[i] == 1:
            pabu_vector += trainset[i]
            pabu_denom += sum(trainset[i])
        else:
            pnorm_vector += trainset[i]
            pnorm_denom += sum(trainset[i])

    pnorm_vector = np.log(pnorm_vector / pnorm_denom)
    pabu_vector = np.log(pabu_vector / pabu_denom)

    return pnorm_vector, pabu_vector, pAbusive


def classify(testVector, pnorm_vector, pabu_vector, pabusive):
    # 先将测试文本转化为向量
    pnorm = sum(testVector * pnorm_vector) + np.log(1 - pabusive)
    # 计算测试文本为正类的概率
    pabu = sum(testVector * pabu_vector) + np.log(pabusive)
    # 计算测试文本为负类的概率
    if pabu > pnorm:
        return 1
    else:
        return 0


def test_bayes():
    c1, nc1, p1 = splitChap(3)
    c2, nc2, p2 = splitChap(4)
    posts_list, classes_list = load_data_set(p1, c1, p2, c2)
    vocab_list = create_vocab_list(posts_list)

    trainset = []
    for post in posts_list:
        trainset.append(wordsToVector(vocab_list, post))
    pnorm_vector, pabu_vector, pAbusive = traing_bayes(trainset, classes_list)

    class_true = []

    result = []
    for i in nc1[:]:
        class_true.append(0)
        testEntry = p1[i]
        testVector = np.array(wordsToVector(vocab_list, testEntry))

        tmp = classify(testVector, pnorm_vector, pabu_vector, pAbusive)
        result.append(tmp)
        print(i, testEntry, "classified as: {}".format(tmp))

    result2 = []
    for i in nc2[:]:
        class_true.append(1)
        testEntry = p2[i]
        testVector = np.array(wordsToVector(vocab_list, testEntry))

        tmp = classify(testVector, pnorm_vector, pabu_vector, pAbusive)
        result2.append(tmp)
        print(i, testEntry, "classified as: {}".format(tmp))

    from sklearn.metrics import classification_report
    # class_true = ([0] * len(result) ) + ([1] * len(result2))  # 正确的分类结果

    class_pred = result + result2  # 实际的分类结果
    print(class_true)
    print(class_pred)
    target_names = ['class 3', 'class 4']
    print(classification_report(class_true, class_pred, target_names=target_names))

    # testEntry = p2[nc2[2]]
    # testVector = np.array(wordsToVector(vocab_list, testEntry))
    #
    # print(testEntry, "classified as: {}".format(classify(testVector, pnorm_vector, pabu_vector, pAbusive)))


# 结果如下：
# ['love', 'my', 'dalmation'] classified as: 0
# ['stupid', 'garbage'] classified as: 1

test_bayes()
