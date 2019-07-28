# coding=utf-8

import tts.sapi
import os

voice = tts.sapi.Sapi()
print(voice.get_voice_names())
# 英文
# voice.set_voice('David')
# voice.set_voice('Zira')
# 日文
# voice.set_voice('Haruka')
# 中文
voice.set_voice('Huihui')
voice.set_rate(3)
# voice.say('在 north point 的酒吧')
voice.say('''



''')
# voice.say('エスタミル')
# voice.create_recording('d:/output.wav', '看看效果如何，A C G')


def create_wav_by_file(source_dir, des_dir):
    """
    将目录下的文本转换成语音

    要求文本为utf-8编码
    :param source_dir: 文本目录
    :param des_dir: 合成语音目录
    :return: 无
    """
    voice = tts.sapi.Sapi()
    for file in os.listdir(source_dir):
        with open(source_dir + '/' + file, 'r', encoding='utf-8') as source_file:
            # for line in source_file:
                # 去除换行，以免影响日志
                # line = line.strip()
                # print(f'processing file {file} line {line}')
                # voice.say(line)
            voice.create_recording(des_dir + '/' + file + '.wav', source_file.read())


# create_wav_by_file('D:/Download/saga/tts_text', 'd:/download/saga/tts_voice')
