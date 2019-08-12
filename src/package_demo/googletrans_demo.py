from googletrans import Translator

# https://github.com/ssut/py-googletrans

translator = Translator()

text = '''
発掘したいお宝の地図のテーブルランクが既知の場合はそのテーブルランクを選んでください。
'''

translated = translator.translate(text, dest='zh-cn')

print(translated)
print(translated.text)
