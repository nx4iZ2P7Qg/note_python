# coding=utf-8
# https://www.jianshu.com/p/152e081fec1b


def B2Q(uchar):
    """单个字符 半角转全角"""
    inside_code = ord(uchar)
    if inside_code < 0x0020 or inside_code > 0x7e: # 不是半角字符就返回原来的字符
        return uchar
    if inside_code == 0x0020: # 除了空格其他的全角半角的公式为: 半角 = 全角 - 0xfee0
        inside_code = 0x3000
    else:
        inside_code += 0xfee0
    return chr(inside_code)


def Q2B(uchar):
    """单个字符 全角转半角"""
    inside_code = ord(uchar)
    if inside_code == 0x3000:
        inside_code = 0x0020
    else:
        inside_code -= 0xfee0
    if inside_code < 0x0020 or inside_code > 0x7e:  # 转完之后不是半角字符返回原来的字符
        return uchar
    return chr(inside_code)


s = 'https：//docplayer.net/54282826-Etsi-gs-mec-015-v1-1-1.html'

re = ''
for c in s:
    re += Q2B(c)
print(re)
