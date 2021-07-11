import hashlib


def generate_file_md5(file_path, blocksize=2 ** 20):
    m = hashlib.md5()
    with open(file_path, "rb") as fObj:
        while True:
            buf = fObj.read(blocksize)
            if not buf:
                break
            m.update(buf)
    return m.hexdigest()


target = 'Z:/tmp/iso/吞食孔明传/A048'

with open(target + '/' + '把我拖入检测工具.md5') as f:
    for line in f.readlines():
        field = line.split('*')
        file = field[1].strip()
        md5_file = generate_file_md5(target + '/' + file)
        print(f'file = {file}, md5 = {md5_file}')
        if field[0].strip() != md5_file:
            print(f'unmatch md5 line = {line}')
