import random


# 全局变量

Board = [["."]] # 棋盘
Dimension = 4 # 棋盘大小
Player = "X" # 玩家和电脑
Computer = "O"
Directions = [[0, 1], [0, -1], [1, 0], [-1, 0], [-1, -1], [1, 1], [1, -1], [-1, 1]] # 八个方向
Score = [0, 0] # 黑白双方得分
Winner = "." # 冠军
Power = "easy" # 难度，本Project未实现难度划分
Position = ["a", "a"] # 棋盘上某点



def Init_board(): # 初始化棋盘
    global Board
    global Dimension
    global Player
    global Computer
    Dimension = int (input ("输入棋盘大小："))
    while Dimension % 2 != 0:
        Dimension = int (input ("必须为偶数，请重新输入： "))
    i = Dimension // 2
    Board = [["." for i in range(Dimension)] for i in range(Dimension)]
    Board[i][i], Board[i-1][i], Board[i][i-1], Board[i-1][i-1] = "O" ,"X" ,"X" ,"O"
    Player = random.choice(["O", "X"])
    if Player == "X":
        print("您执黑棋，标志为X！")
        Computer = "O"
    else:
        print("您执白棋，标志为O！")
        Computer = "X"
    printBoard()
    return



def printBoard(): # 打印棋盘
    print ("  ", end = "")
    for i in range(Dimension):
        print (chr (ord ("a") + i), end = " ")
    print()
    for i in range(Dimension):
        print (chr (ord ("a") + i), end = " ")
        for j in range(Dimension):
            print (Board[i][j], end = " ")
        print()
    return



def isInRange(x, y): # 输入点是否在棋盘范围内
    if x < 0 or x >= Dimension or y < 0 or y >= Dimension:
        return False
    return True


def canAttack(X, Y, c, d): # 是否能攻击到其他点，如不能则无法在此落子
    x, y = ord(X) - ord("a"), ord(Y) - ord("a")
    if isInRange (x, y) == False:
        return False
    for i in Directions:
        if canAttackHelper (i, x, y, c, d) == True:
            return True
    return False



def canAttackHelper(i, x, y, c, d): # 针对单一方向是否能攻击的判断
    a, b = x, y
    boolean, judge = False, False
    a, b = a + i[0], b + i[1]
    while isInRange(a, b) == True:
        if Board[a][b] == ".":
            return False
        if Board[a][b] == d:
            boolean = True
        if Board[a][b] == c:
            judge = True
            return judge and boolean
        a, b = a + i[0], b + i[1]
    return False



def isLegal(X, Y, c, d): # 是不是合法的落子
    x, y = ord(X) - ord("a"), ord(Y) - ord("a")
    if x < 0 or x >= Dimension or y < 0 or y >= Dimension:
        return False
    if Board[x][y] != ".":
        return False
    return canAttack(X, Y, c, d)



def getAvailable(c, d): # 获得能下的点，没有就返回空list
    result = []
    for i in range(Dimension):
        for j in range(Dimension):
            if isLegal(chr(i + ord("a")), chr(j + ord("a")), c, d) == True:
                result.append([i, j])
    return result



def flip(X, Y, c, d): # 落子之后，翻转其他子
    global Board
    x, y = ord(X) - ord("a"), ord(Y) - ord("a")
    if isInRange(x, y) == False:
        return
    if isLegal(X, Y, c, d) == False:
        return
    Board[x][y] = c
    for p in Directions:
        if canAttackHelper(p, x, y, c, d) == True:
            a, b = x + p[0], y + p[1]
            while Board[a][b] == d and isInRange(x, y) == True:
                Board[a][b] = c
                a, b = a + p[0], b + p[1]
    return
    



def isFull(): # 判断棋盘是否满了
    for i in range(Dimension):
        for j in range(Dimension):
            if Board[i][j] == ".":
                return False
    return True



def countScore(): # 统计分数
    global Score
    for i in range(Dimension):
        for j in range(Dimension):
            if Board[i][j] == "O":
                Score[0] += 1
            elif Board[i][j] == "X":
                Score[1] += 1
    return Score



def canContinue(X, Y, c, d): # 落子之后是否可以继续下
    global Winner
    global Score
    s = countScore()
    if isLegal(X, Y, c, d) == False:
        print("不能在这里走！")
        Winner = d
        return False
    if isFull() == True:
        print("棋盘已满！")
        if s[0] > s[1]:
            Winner = "O"
        elif s[0] < s[1]:
            Winner = "X"
        else:
            Winner = "."
        return False
    if s[0] == 0:
        print("白方子力已被吃光")
        Winner = "X"
        return False
    if s[1] == 0:
        print("黑方子力已被吃光")
        Winner = "O"
        return False
    if getAvailable(c, d) == [] and getAvailable(d, c) == []:
        print("双方均已无棋可走！")
        if s[0] > s[1]:
            Winner = "O"
        elif s[0] < s[1]:
            Winner = "X"
        else:
            Winner = "."
        return False
    return True



def canContinue1 (c, d): # 落子之前是否可以继续下
    global Winner
    global Score
    s = countScore()
    if isFull() == True:
        print("棋盘已满！")
        if s[0] > s[1]:
            Winner = "O"
        elif s[0] < s[1]:
            Winner = "X"
        else:
            Winner = "."
        return False
    if s[0] == 0:
        print("白方子力已被吃光")
        Winner = "X"
        return False
    if s[1] == 0:
        print("黑方子力已被吃光")
        Winner = "O"
        return False
    if getAvailable(c, d) == [] and getAvailable(d, c) == []:
        print("双方均已无棋可走！")
        if s[0] > s[1]:
            Winner = "O"
        elif s[0] < s[1]:
            Winner = "X"
        else:
            Winner = "."
        return False
    return True



def end(): # 游戏结束
    print("游戏结束！")
    if Winner == "O":
        print("白方胜利！")
    elif Winner == "X":
        print("黑方胜利！")
    else:
        print("和棋！")



Init_board()
if Player == "X":
    while True:
        if canContinue1(Computer, Player) == False:
            break
        Available = getAvailable(Player, Computer)
        if Available == []:
            print("无棋可走，跳过本轮")
        else:
            print("轮到您走了！")
            pos = input("请输入坐标：")
            Position[0], Position[1] = pos[0], pos[1]
            if canContinue(Position[0], Position[1], Player, Computer) == False:
                break
            print("您选择了走：",Position[0], Position[1])
            flip(Position[0], Position[1], Player, Computer)
            printBoard()
        if canContinue1(Player, Computer) == False:
            break
        Available = getAvailable(Computer, Player)
        if Available == []:
            print("无棋可走，跳过本轮")
            continue
        temp = random.choice(Available)
        t = ["a", "a"]
        t[0], t[1] = chr(temp[0] + ord("a")), chr(temp[1] + ord("a"))
        Position[0], Position[1] = t[0], t[1]
        if canContinue(Position[0], Position[1], Computer, Player) == False:
            break
        flip(Position[0], Position[1], Computer, Player)
        print("电脑走了", Position[0], Position[1])
        printBoard()
        if canContinue1(Player, Computer) == False:
            break
else:
    while True:
        if canContinue1(Computer, Player) == False:
            break
        Available = getAvailable(Computer, Player)
        if Available == []:
            print("无棋可走，跳过本轮")
        else:
            temp = random.choice(Available)
            t = ["a", "a"]
            t[0], t[1] = chr(temp[0] + ord("a")), chr(temp[1] + ord("a"))
            Position[0], Position[1] = t[0], t[1]
            if canContinue(Position[0], Position[1], Computer, Player) == False:
                break
            flip(Position[0], Position[1], Computer, Player)
            print("电脑走了", Position[0], Position[1])
            printBoard()
        if canContinue1(Player, Computer) == False:
            break
        Available = getAvailable(Player, Computer)
        if Available == []:
            print("无棋可走，跳过本轮")
            continue
        print("轮到您走了！")
        pos = input("请输入坐标：")
        Position[0], Position[1] = pos[0], pos[1]
        if canContinue(Position[0], Position[1], Player, Computer) == False:
            break
        print("您选择了走：",Position[0], Position[1])
        flip(Position[0], Position[1], Player, Computer)
        printBoard()
        if canContinue1(Computer, Player) == False:
            break
end()
