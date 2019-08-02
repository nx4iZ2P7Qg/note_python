import math


class MSRand:

    def __init__(self):
        self.ID = 0
        self.X = 3830989
        self.A1 = 12996205
        self.B1 = 123453
        self.A1_b = 12184421
        self.B1_b = 8306415
        self.A100 = 13620369
        self.B100 = 7897084
        self.A100_b = 3566705
        self.B100_b = 11088324

    def value_of_ms_rand(self, n):
        if n > self.ID:
            while n - self.ID > 100:
                self.X = (self.X * self.A100 + self.B100) % (1 << 24)
                self.ID += 100
            while n != self.ID:
                self.X = (self.X * self.A1 + self.B1) % (1 << 24)
                self.ID += 1
        else:
            while self.ID - n > 100:
                self.X = (self.X * self.A100_b + self.B100_b) % (1 << 24)
                self.ID -= 100
            while n != self.ID:
                self.X = (self.X * self.A1_b + self.B1_b) % (1 << 24)
                self.ID -= 1
        return self.X


def subPattern(P, ran, sk, sub):
    deru = False
    pattern = ''
    if ran[P] % 10 >= sk:
        pattern += '+x'
        deru = True
    if ran[P - 1] % 10 < sk and ran[P] % 20 >= sk:
        if deru:
            pattern += ',+' + sub[0]
        else:
            pattern = '+' + sub[0]
        deru = True
    if ran[P - 2] % 10 < sk and ran[P - 1] % 20 < sk:
        if ran[P] % 100 >= sk:
            if deru:
                pattern += ',+' + sub[0] + sub[1]
            else:
                pattern = '+' + sub[0] + sub[1]
            deru = True
        else:
            if deru:
                pattern += ',+' + sub[0] + sub[1] + sub[2]
            else:
                pattern = '+' + sub[0] + sub[1] + sub[2]
            deru = True
    if not deru:
        pattern = '---'
    return pattern


def calcTreasureMoney(TR, J, A_SM, ran):
    subPosition = ''
    x = randTableGrade(TR, J, ran)
    if x >= 7:
        y = (ran[J + 4] & 3) + 6
        J += 1
        subPosition = 'left'
    elif x > 0 and x < 7:
        y = x
        subPosition = 'right'
    else:
        y = 0
        subPosition = 'right'
    z = (ran[J + 4] % (y + 1) + ran[J + 5] % (y + 1)) * 50 + 1
    kane = ran[J + 6] % z + 100
    if ran[J + 7] % 10 == 0:
        kane *= 3
    if kane > 2000:
        kane = 2000
    if kane > 999:
        rich = 'YUKICHI'
    else:
        rich = ''
    kingaku = kane * 10
    return kingaku, rich


def randTableGrade(TR, K, ran):
    return math.floor((ran[K] % 5 + ran[K + 1] % 5 + ran[K + 2] % 5 + ran[K + 3] % 5) // 2) + TR - 4



def test():
    Ztable = [
        ["雪", "雪", "雪", "竜剣", "雪"],
        ["炎", "ベルジュ", "ランギ", "青の剣", "紅孔雀"],
        ["PD", "ブリム", "AJ", "レディ", "竜ケレ"],
        ["AM", "魔石", "刀", "ヴォパ", "竜マリ"],
        ["LL", "光", "藤", "竜盾", "水鏡"],
        ["銀", "魔骨", "タイタス", "竜鎧", "黒鎧"]
    ]
    A_TR = ['9']
    A_GR = ['9']
    ID = 0
    N = 3000
    A_ES = [5]
    A_SM = 'full'
    ZdataTable = []
    if len(A_ES) == 0:
        A_ES = [1, 2, 3, 4, 5]
    if len(A_SM) == 0:
        A_SM = 'full'
    R = MSRand()
    ran = []
    for i in range(N + 40):
        ran.append(R.value_of_ms_rand(ID - 20 + i))

    for i in range(N):
        j = i + 20
        Zcolumn = []
        idHtml = ID + i
        Zcolumn.append(idHtml)
        Zk = ran[j] % 6
        for t in range(len(A_TR)):
            TR = int(A_TR[t])

            # 金额
            small = False
            A = randTableGrade(TR, j - 13, ran)
            B = randTableGrade(TR, j - 12, ran)
            if A >= 7 and B >= 7:
                Zkingaku, Kolor = calcTreasureMoney(TR, j - 13, A_SM, ran)
            elif A < 7 and B < 7:
                Zkingaku, Kolor = calcTreasureMoney(TR, j - 12, A_SM, ran)
            elif A >= 7 and B < 7:
                hMiddle, hRich = calcTreasureMoney(TR, j - 13, A_SM, ran)
                lMiddle, lRich = calcTreasureMoney(TR, j - 12, A_SM, ran)
                Zkingaku = str(hMiddle) + '/' + str(lMiddle)
                small = True
                if hRich == 'YUKICHI' or lRich == 'YUKICHI':
                    Kolor = 'YUKICHI'
                else:
                    Kolor = ''
            else:
                Zkingaku = '---'
                Kolor = ''
            Zcolumn.append(Zkingaku)

            # 主
            for g in range(len(A_GR)):
                GR = int(A_GR[g])
                X = (ran[j - 3] % (GR + 1)) + (ran[j - 2] % (TR + 1))
                Lv = ran[j - 1] % ((X - X % 4) // 4 + 1)

                # color

                mainHtml = Ztable[Zk][Lv]
                Zcolumn.append(mainHtml)

        # 副
        sub = []
        Stable = "GSSPPPWWTT"
        for k in range(3):
            sub.append(Stable[ran[j + k * 2 + 2] % 10])
        subCandidate = sub[0] + sub[1] + sub[2]
        Zcolumn.append(subCandidate)

        for s in range(len(A_ES)):
            sk = int(A_ES[s])
            subHtml = subPattern(j - 14, ran, sk, sub) + '/' + subPattern(j - 13, ran, sk, sub)
            Zcolumn.append(subHtml)

        print(Zcolumn)


test()
