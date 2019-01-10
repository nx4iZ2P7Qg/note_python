# 语法
# file object = open(file_name [, access_mode][, buffering])

# 读
# <r>	只读模式，the file offset stays at the root.
# <rb>	二进制只读，the offset remains at the root level.
# 写
# <w>	It allows write-level access to a file. 文件存在则覆盖，不存在则新建
# <wb>	Use it to open a file for writing in binary format. Same behavior as for write-only mode.
# <a>	append模式，偏移在文件尾，文件不存在则新建
# <ab>	append二进制，Same behavior as for append mode.
# 读写
# <w+>	读写模式，Same behavior as for write-only mode.
# <wb+>	读写二进制，Same behavior as for write-only mode.
# <r+>	读写模式，the file offset is again at the root level.
# <rb+>	读写二进制，The file offset is again at the root level.
# <a+>	append读，Same behavior as for append mode.
# <ab+>	append读二进制，Same behavior as for append mode.

path_file_origin = 'd:/io_test.txt'
path_file_new = 'd:/io_test.backup.txt'

# python3中，string(text)与byte(8-bits)有明显的不同，除非明示，否则'a'并不代表97，如果打算使用text模式，最好指定encoding
# 如果不指定编码，python在不同平台上默认编码不同，window下是<cp1252>，linux下是<utf-8>
with open(path_file_origin, mode='w+', encoding='utf-8', buffering=512) as f:
    print(f.closed)
    print(f.mode)
    print(f.name)
    print(f.tell())
    char_len = f.write('bio hazard resident evil')
    print(char_len)
    f.write('生化战士')
    # 移动游标, 0文件开始处，1当前位置，2文件尾
    f.seek(10, 0)
    f.flush()
    print(f.tell())
    contents = f.readlines()

for line in contents:
    print(line)
