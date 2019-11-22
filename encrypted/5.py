import random

INIT_STR = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def analysing(Message):
    """
    :param Message: input encrypt or decrypt message
    :return: analyse data
    """

    total = 0
    unique = 0
    mostLetter = ""
    tmp = ""
    for i in Message:
        current = " "
        if not i.isalnum():
            tmp += current
        else:
            tmp += i
    tmp = tmp.strip()

    tmpSplit = tmp.split()
    total = len(tmpSplit)

    tmp = {}
    for i in tmpSplit:
        if i not in tmp:
            tmp[i] = 1
        else:
            tmp[i] += 1
    tmpList = []
    for k, v in tmp.items():
        tmpList.append((k, v))
        if v == 1:
            unique += 1
    tmpList = sorted(tmpList, key=lambda x: x[1], reverse=True)[:10]
    frequency_result = []
    for i in tmpList:
        frequency_result.append("{} : {}".format(i[0], i[1]))
    frequency = "\n".join(frequency_result)

    sumWordLen = 0
    minWordLen = len(tmpSplit[0])
    maxWordLen = len(tmpSplit[0])
    for i, v in enumerate(tmpSplit):
        sumWordLen += len(v)
        if i == 0:
            continue
        if len(v) < minWordLen:
            minWordLen = len(v)

        if len(v) > maxWordLen:
            maxWordLen = len(v)

    averageWordLen = sumWordLen / total

    tmp = {}
    for i in Message:
        if i == " ":
            continue
        if i not in tmp:
            tmp[i] = 1
        else:
            tmp[i] += 1
    tmpList = [(k, v) for k, v in tmp.items()]
    tmpList = sorted(tmpList, key=lambda x: x[1], reverse=True)
    mostLetter = tmpList[0][0]

    result = "analysing:\nTotal number of words: {}\nNumber of unique words: {}\nMinimum : {}\nmaximum : {}\naverage word length: {}\nMost common letter: {}\nThe ten most common words and their frequency: \n{}"
    return result.format(total, unique, minWordLen, maxWordLen, averageWordLen, mostLetter, frequency)


def encrypt(Message, Rotation):
    """
    encrypt data method
    :param Message: input encrypt message
    :param Rotation: far
    :return: encrypt message
    """
    rotation_str = INIT_STR[Rotation:] + INIT_STR[:Rotation]
    password = {}
    for i in range(len(INIT_STR)):
        password[INIT_STR[i]] = rotation_str[i]
    result = ""
    for i in Message:
        i = i.upper()
        if i not in password:
            result += i
            continue
        result += password[i]
    return result


# !# add a random encrypt method
def randomEncrypt(Message):
    """
    random encrypt,in word start and end add a word to show the rotation
    :param Message: encrypt message
    :return: encrypt string
    """
    Rotation = random.randint(1, 25)
    rotation_str = INIT_STR[Rotation:] + INIT_STR[:Rotation]
    password = {}
    for i in range(len(INIT_STR)):
        password[INIT_STR[i]] = rotation_str[i]
    result = []
    wordList = Message.split(" ")
    for word in wordList:

        randIdx = random.randint(0, 25 - Rotation)

        tmp = INIT_STR[randIdx]
        for i in word:
            i = i.upper()
            if i not in password:
                result += i
                continue
            tmp += password[i]
        tmp += INIT_STR[randIdx + Rotation]
        result.append(tmp)
    return " ".join(result)


def decrypt(Message, Rotation):
    """
    decrypt the message
    :param Message: wait to decrypt message
    :param Rotation: value int
    :return: decrypt string data
    """
    rotation_str = INIT_STR[Rotation:] + INIT_STR[:Rotation]
    password = {}
    for i in range(len(INIT_STR)):
        password[rotation_str[i]] = INIT_STR[i].upper()
    result = ""
    for i in Message:
        i = i.upper()
        if i not in password:
            result += i
            continue
        result += password[i.upper()]
    return result


def getInput(preInfo, InputInfo, errInfo, trueSection=None, func=None):
    for i in preInfo:
        print(i)
    while True:
        result = input(InputInfo)
        if trueSection:
            if result not in trueSection:
                for i in errInfo:
                    print(i)
                continue
            break
        else:
            flag = func(result)
            if not flag:
                for i in errInfo:
                    print(i)
                continue
            break
    return result


def getMode():
    mode = getInput(["Should it encrypt or decrypt the message?"], "The cipher mode: ",
                    ["make sure your input is right,encrypt or decrypt"], trueSection=["decrypt", "encrypt"])
    return mode


def getMessage():
    messageFrom = getInput(["message from file or commandLine?"], "your choose: ",
                           ["make sure your input is right,file or commandLine"], trueSection=["file", "commandLine"])

    if messageFrom == "file":
        while True:
            path = input("please input file path: ")
            try:
                with open(path, 'r') as f:
                    message = f.read()
                break
            except FileNotFoundError as e:
                print("file not found!please input again!")
                continue
    else:
        print("The words to be encrypted or decrypted.")
        print("This should be able to take both single line and multi-line messages.")
        message = input("A message: ")

    return message


def getRotationValue():
    rotation_value = int(
        getInput(["How far should the cipher shift?", "This should be a positive integer."],
                 "A rotation value: ",
                 ["This should be a positive integer."], func=lambda x: x.isdigit() and int(x) > 0))
    return rotation_value




if __name__ == "__main__":

    mode = getMode()

    if mode == "decrypt":
        decryptMode = getInput(["you can choose you input rotation value or auto decrypt"], "decryptMode: ",
                               ["make sure your input is right,auto or value"], trueSection=["auto", "value"])
        if decryptMode == "value":
            rotation_value = getRotationValue()
            message = getMessage()
            result = decrypt(message, rotation_value)
            print(result)
        else:
            message = getMessage()
            messageLines = message.split("\n")
            words = {}
            with open("english-dictionary-500.txt", 'r') as f:
                for line in f:
                    words[line.strip()] = 1

            # auto decrypt start!
            result = []  # decrypt line factory
            rotation_tmp = 1
            curLine = 0
            useValue = False
            while True:
                if curLine > len(messageLines) - 1:
                    print("message decrypt over..")
                    break

                if rotation_tmp > 25:
                    print("no word match!", "auto decrypt fail!")
                    if not useValue:
                        print("please try to find by self!")
                        useValue = True
                        rotation_tmp = 1
                        curLine = 0
                        continue
                    else:
                        print("decrypt fail!")
                        break

                finds = decrypt(messageLines[curLine], rotation_tmp)
                findsList = finds.split(" ")
                flag = False
                for word in findsList:
                    if word.lower() in words:
                        flag = True
                        break
                if flag or useValue:
                    ok = getInput(["decrypted line:", finds, "is it true?"], "your answer: ",
                                  ["please input yes or no"],
                                  ["yes", "no"])
                    if ok == "yes":
                        result.append(finds)
                        print(finds)
                        # print("\n".join(result))
                        curLine += 1
                        rotation_tmp = 1
                    else:
                        rotation_tmp += 1
                else:
                    rotation_tmp += 1
                    continue
            result = "\n".join(result)
        message = result

    else:
        rotation_value = getRotationValue()
        message = getMessage()
        print(encrypt(message, rotation_value))
    print(analysing(message))
