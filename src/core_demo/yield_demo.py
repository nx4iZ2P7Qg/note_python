# 包含yield的方法，称为生成器


def count(n):
    print("counting")
    while n > 0:
        print('before yield')
        yield n
        n -= 1
        print('after yield')


# 不执行方法内任何语句
f = count(5)
# 调用next时，才执行到yield
print('first next = %s' % f.__next__())
# 再次调用next时，执行yield后面的语句
print('second next = %s' % f.__next__())
# 执行到没有可迭代的值后，会报错，所以一般不使用next，而使用迭代
for i in count(5):
    print(i)
# 如果方法中有多个yield，则执行时会停在下一个yield前
