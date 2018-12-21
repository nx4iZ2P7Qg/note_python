from collections import deque
"""
双端队列
"""

empty = deque()
d = deque(['a', 'b', 'c'])

print(d.pop())
print(d.popleft())

d.append('c')
d.appendleft('a')
d.insert(2, 'bb')

d.extend(['e', 'f', 'g'])
d.extendleft(['a', 'b', 'c', 'd'])

d.count('a')

d.index('e')

d.clear()

d.rotate(2)

# 指定队列最大长度，超出长度自动丢弃
d = deque(maxlen=10)
for i in range(20):
    d.append(i)
print(d)
