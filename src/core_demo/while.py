i = 0
while i < 10:
    if i < 3:
        print(i)
    else:
        break
    i += 1
# break后，else不执行
else:
    print('break else = ' + str(i))

i = 0
while i < 10:
    if i < 3:
        print(i)
    i += 1
# while条件为false时执行
else:
    print('no break else = ' + str(i))
