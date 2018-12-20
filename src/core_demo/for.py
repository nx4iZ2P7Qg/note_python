aList = ['a', 'b']
for s in aList:
    print(s)

# 如果要迭代数组下标，可以使用for与range
a = ['Mary', 'had', 'a', 'little', 'lamb']
for i in range(len(a)):
    print('range = ' + str((i, a[i])))

# enumerate()比较方便
for i in enumerate(a):
    print('enumerate = ' + str(i))

# for循环可以接收iterable，list()也可以
for i in list(('a', 'b')):
    print('list = ' + i)

words = [' ', 'tomorrow']
# for内部修改了迭代对象words，如果没有[:]，程序无限循环
# 修改迭代对象时建议先使用[:]复制
for w in words[:]:
    if len(w) > 6:
        # 修改了迭代内容
        words.insert(0, w)
        print(words)

# 范围内素数
# 考查范围
for n in range(2, 10):
    # 范围除开了1和本身
    for x in range(2, n):
        # 只要有整除的情况，就不是素数
        if n % x == 0:
            print(n, 'equals', x, '*', n // x)
            break
    # 迭代完成时执行，break时不执行，迭代完成表示没找到可以整除的数
    else:
        print(n, 'is a prime number')
