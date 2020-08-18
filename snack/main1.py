import turtle
import time
import random

# color
RED = "#FF0000"
BLACK = "#000000"
BLUE = "#0000FF"
FUCHSIA = "#FF00FF"

# base variable
snackUpdateSpeed = 200
monsterUpdateSpeed = 200
monsterRandom = [-10, 150]
gameStartFlag = False
gameOverFlag = False  # a flag to express the game over status
stopFlag = False  # a flag to express the game stop status
snackDirection = "w"  # a flag to express the snack's direction
monsterDirection = "w"  # a flag to express the monster's direction
waitFixedLength = 5  # a flag to express the length snack wait push
contacted = 0  # a flag to express the times monster contacted snack's body
baseTime = 0  # start time
snackLength = 1  # snack length
snackPosition = [[0, 0]]  # random position snack's start position
monsterPosition = [random.randint(-20, 20) * 10,
                   random.randint(-20, 20) * 10]  # random position monster's start position
foodItemPosition = [[random.randint(-20, 20) * 10, random.randint(-20, 20) * 10] for i in
                    range(8)]  # random position food's start position
baseTitle = "Snack: Contacted: {}, Time: {}"  # title content

# turtle setter
# update
turtle.tracer(False)

# turtle setter
# snack, monster, food
snack = turtle.Turtle()
snack.hideturtle()
snack.speed(0)
monster = turtle.Turtle()
monster.hideturtle()
monster.speed(0)
food = turtle.Turtle()
food.hideturtle()
food.speed(0)

# screen setter
src = turtle.Screen()
src.setup(500, 500)
src.delay(0)
src.title(baseTitle.format(contacted, baseTime))


def stop():
    """
    stop the world!
    press space to stop the world!
    :return:
    """
    global stopFlag
    if stopFlag:
        stopFlag = False
        snackLoop()
        monsterLoop()
        timerLoop()
        return
    stopFlag = True


def drawSquare(t, position, color, border=None):
    """
    draw a square

    :param t:
    :param position:
    :param color:
    :param border:
    :return:
    """
    t.penup()
    t.goto(*position)
    t.pendown()
    if border:
        t.color(border)
    else:
        t.color(color)
    t.hideturtle()
    t.begin_fill()
    t.fillcolor(color)
    for x in range(1, 5):
        t.forward(10)
        t.right(90)
    t.end_fill()


def drawSnack(position):
    """
    draw a snack
    :param position:
    :return:
    """
    # head
    drawSquare(snack, position[0], RED)
    # body
    for i in position[1:]:
        drawSquare(snack, i, BLACK, BLUE)


def drawMonster(position):
    """
    draw a monster
    :param position:
    :return:
    """
    monster.clear()
    drawSquare(monster, position, FUCHSIA)

    # 怪物与蛇身体相碰
    print("****")
    print(monsterPosition)
    print(snackPosition)
    print(monsterPosition in snackPosition)


def drawFood(t, position):
    """
    draw some food
    :param t:
    :param position:
    :return:
    """
    if not gameStartFlag:
        return
    t.clear()
    for i, v in enumerate(position):
        if not v:
            continue
        t.penup()
        t.goto(*v)
        t.pendown()
        t.write(str(i + 1), align="left", font=("Arial", 10, "normal"))


def up():
    """
    control function ⬆
    :return:
    """
    global snackDirection, snackLength, snackPosition
    if snackDirection == "s" and snackLength != 1:
        return
    if snackDirection == "a" or snackDirection == "d":
        if snackPosition[0][1] == 250:
            return
    snackDirection = "w"


def down():
    """
    control function ⬇
    :return:
    """
    global snackDirection, snackLength
    if snackDirection == "w" and snackLength != 1:
        return
    if snackDirection == "a" or snackDirection == "d":
        if snackPosition[0][1] == -230:
            return
    snackDirection = "s"


def left():
    """
    control function ←
    :return:
    """
    global snackDirection, snackLength, snackPosition
    if snackDirection == "d" and snackLength != 1:
        return
    if snackDirection == "w" or snackDirection == "s":
        if snackPosition[0][0] == -250:
            return
    snackDirection = "a"


def right():
    """
    control function →
    :return:
    """
    global snackDirection, snackLength, snackPosition
    if snackDirection == "a" and snackLength != 1:
        return
    if snackDirection == "w" or snackDirection == "s":
        if snackPosition[0][0] == 230:
            return
    snackDirection = "d"


def isEatFoodItem(headPosition):
    """
    :param headPosition:
    :return:
    """
    global foodItemPosition, snackDirection

    # 文字坐标
    possiblePosition = [headPosition, [headPosition[0] + 10, headPosition[1]], [headPosition[0], headPosition[1] - 10],
                        [headPosition[0] + 10, headPosition[1] - 10]]

    for pos in possiblePosition:
        if pos in foodItemPosition:  # 如果蛇头在食物坐标列表里面 说明吃到了食物
            return foodItemPosition.index(pos) + 1
    return 0


def snackUpdate(updateSpeed=snackUpdateSpeed):
    drawFood(food, foodItemPosition)
    drawSnack(snackPosition)
    turtle.update()
    if not gameStartFlag:
        return

    turtle.ontimer(snackLoop, updateSpeed)


def monsterUpdate(updateSpeed=monsterUpdateSpeed):
    drawMonster(monsterPosition)
    if not gameStartFlag:
        return
    global contacted,gameOverFlag
    if monsterPosition in snackPosition:
        contacted += 1
    src.title(baseTitle.format(contacted, baseTime))
    # print(gameStartFlag)
    # 怪物是否碰到蛇头
    allPoint = [
        monsterPosition,
        [monsterPosition[0] + 10, monsterPosition[1]],
        [monsterPosition[0], monsterPosition[1] - 10],
        [monsterPosition[0] + 10, monsterPosition[1] - 10]
    ]
    headPoint = snackPosition[0]
    snackHead = [
        headPoint,
        [headPoint[0] + 10, headPoint[1]],
        [headPoint[0], headPoint[1] - 10],
        [headPoint[0] + 10, headPoint[1] - 10]
    ]
    touchCount = 0
    for i in allPoint:
        if i in snackHead:
            touchCount += 1
    if touchCount >= 3:
        t = turtle.Turtle()
        t.hideturtle()
        t.speed(0)
        t.penup()
        t.goto(*snackPosition[0])
        t.pendown()
        t.color(RED)
        t.write("fail!!!", font=("arial", 16, "bold"))
        gameOverFlag = True
    turtle.update()
    turtle.ontimer(monsterLoop, random.randint(-monsterRandom[0], monsterRandom[1]) + updateSpeed)


def snackLoop():
    global snack, snackPosition, src, snackDirection, snackLength, waitFixedLength, foodItemPosition, food
    global stopFlag, gameOverFlag

    if stopFlag or gameOverFlag:
        return

    # 边界判断
    if snackPosition[0][0] == -250:
        if snackDirection == "a":
            snackUpdate()
            return
    if snackPosition[0][0] == 230:
        if snackDirection == "d":
            snackUpdate()
            return
    if snackPosition[0][1] == 250:
        if snackDirection == "w":
            snackUpdate()
            return
    if snackPosition[0][1] == -230:
        if snackDirection == "s":
            snackUpdate()
            return

    # 运动
    snack.clear()
    lastBody = snackPosition[-1]
    # 如果蛇移动了，蛇的每一个点都往前移
    for i in reversed(range(1, len(snackPosition))):
        snackPosition[i] = snackPosition[i - 1]
    if snackDirection == "w":
        snackPosition[0] = [snackPosition[0][0], snackPosition[0][1] + 10]
    elif snackDirection == "s":
        snackPosition[0] = [snackPosition[0][0], snackPosition[0][1] - 10]
    elif snackDirection == "a":
        snackPosition[0] = [snackPosition[0][0] - 10, snackPosition[0][1]]
    else:
        snackPosition[0] = [snackPosition[0][0] + 10, snackPosition[0][1]]

    # 吃到食物就追加方块
    foodValue = isEatFoodItem(snackPosition[0])
    if foodValue != 0:
        foodItemPosition[foodValue - 1] = []
    waitFixedLength += foodValue
    if waitFixedLength > 0:
        if not gameStartFlag:
            snackUpdate()
            return
        snackPosition.append(lastBody)
        waitFixedLength -= 1
        snackLength += 1
        snackUpdate(snackUpdateSpeed * 2)  # 伸展身体需要减速
        return

    # 游戏是否胜利
    leaveFood = False
    for i in foodItemPosition:
        if i:
            leaveFood = True
            break
    if not leaveFood and waitFixedLength == 0:
        t = turtle.Turtle()
        t.hideturtle()
        t.speed(0)
        t.penup()
        t.goto(*snackPosition[0])
        t.pendown()
        t.color(RED)
        t.write("winner", font=("arial", 16, "bold"))
        gameOverFlag = True

    snackUpdate()


def monsterLoop():
    global snackPosition, monsterPosition, src, contacted, gameOverFlag
    global stopFlag

    if stopFlag or gameOverFlag:
        return
    # 怪物朝着蛇头移动
    if snackPosition[0][0] > monsterPosition[0]:
        monsterPosition[0] += 10
        monsterUpdate(monsterUpdateSpeed)
        return
    elif snackPosition[0][0] < monsterPosition[0]:
        monsterPosition[0] -= 10
        monsterUpdate(monsterUpdateSpeed)
        return
    if abs(snackPosition[0][0] - monsterPosition[0]) <= 20:
        if snackPosition[0][1] > monsterPosition[1]:
            monsterPosition[1] += 10
        else:
            monsterPosition[1] -= 10
    monsterUpdate(random.randint(-10, 200) + 200)
    return


def timerLoop():
    global baseTime, contacted, src, baseTitle
    global stopFlag

    if not gameStartFlag:
        return

    if stopFlag or gameOverFlag:
        return
    baseTime += 1
    # 时间计数器
    src.title(baseTitle.format(contacted, baseTime))
    turtle.ontimer(timerLoop, 1000)


def startUp(doc):

    t = doc
    t.hideturtle()
    t.speed(0)
    t.color(RED)

    t.penup()
    t.goto(-180, 100)
    t.pendown()

    t.write("Controls\n"
            "a. Use the four arrow keys (Up, Down, Left, Right) to maneuver the snake\n"
            "b. The motion will continue in the direction of the last key pressed.\n"
            "c. Use “Space Bar” to pause or un-pause snake motion\n"
            "d. Snake cannot move beyond the screen area\n"
            "e. Snake can cross its body\n"
            )
    # t.clear()
    # turtle.update()


def clickToStart(x, y):
    global gameStartFlag
    gameStartFlag = True
    doc.clear()
    # turtle.update()
    snackLoop()
    monsterLoop()
    timerLoop()




if __name__ == '__main__':
    doc = turtle.Turtle()
    startUp(doc)
    snackLoop()
    monsterLoop()
    timerLoop()

    src.onkeypress(up, "Up")
    src.onkeypress(down, "Down")
    src.onkeypress(left, "Left")
    src.onkeypress(right, "Right")
    src.onkeypress(stop, "space")
    src.listen()


    src.onclick(clickToStart, btn=1, add=None)
    turtle.done()
