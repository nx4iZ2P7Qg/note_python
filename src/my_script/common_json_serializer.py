import json
from datetime import date
from datetime import time


def serialize(obj):
    """
    通用python json序列化方法

    :param obj: 待序列化对象
    :return: 对象序列化字符串
    """
    # 处理日期格式
    if isinstance(obj, date):
        serial = obj.isoformat()
        return serial
    # 处理时间格式
    if isinstance(obj, time):
        serial = obj.isoformat()
        return serial
    # 其他类型
    return obj.__dict__


# 测试类
class TestClass:
    def __init__(self):
        self.value1 = "a"
        self.value2 = "b"
        self.date = date.today()
        self.time = time()


test = TestClass()
print(json.dumps(test, default=serialize))