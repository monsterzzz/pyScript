

INIT_STR = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def analysing(Message):
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


def decrypt(Message, Rotation):
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

if __name__ == "__main__":
    mode = getInput(["Should it encrypt or decrypt the message?"], "The cipher mode: ",
                    ["make sure your input is right,encrypt or decrypt"], trueSection=["decrypt", "encrypt"])
    rotation_value = int(
        getInput(["How far should the cipher shift?", "This should be a positive integer."], "A rotation value: ",
                 ["This should be a positive integer."], func=lambda x: x.isdigit() and int(x) > 0))

    print("The words to be encrypted or decrypted.")
    print("This should be able to take both single line and multi-line messages.")
    message = input("A message: ")
    if mode == "encrypt":
        print(encrypt(message, rotation_value))
    else:
        print(decrypt(message, rotation_value))
    print(analysing(message))
