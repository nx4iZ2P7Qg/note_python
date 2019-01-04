coefficient = 1024

# 初始化 位 或 字节
# bits = 10 ** 16
bits = 7811938304
# Bytes = bits / 8
Bytes = 7811938304 * 1024

KB = Bytes / coefficient
MB = KB / coefficient
GB = MB / coefficient
TB = GB / coefficient

print('%s MB' % round(MB, 1))
print('%s GB' % round(GB, 1))
print('%s TB' % round(TB, 1))
