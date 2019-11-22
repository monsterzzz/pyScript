INIT_STR = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


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
        print(encrypt(message,rotation_value))
    else:
        print(decrypt(message,rotation_value))
