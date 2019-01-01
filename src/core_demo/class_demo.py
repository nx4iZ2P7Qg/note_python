class BookStore:
    number_of_object = 0

    # __init__()是每个类的唯一方法，创造对象时默认调用，用来初始化，相当于构造器
    # self是对象引用，同时也是__init__方法的第一个参数
    # 属性作为__init__的参数
    def __init__(self, title, author):
        self.title = title
        self.author = author
        BookStore.number_of_object += 1

    def book_info(self):
        print("Book title:", self.title)
        print("Book author:", self.author, "\n")


# Create a virtual book store
b1 = BookStore("Great Expectations", "Charles Dickens")
b2 = BookStore("War and Peace", "Leo Tolstoy")
b3 = BookStore("Middlemarch", "George Eliot")

# call member functions for each object
b1.book_info()
b2.book_info()
b3.book_info()

print("BookStore.noOfBooks:", BookStore.number_of_object)


# 继承
class Taxi:
    def __init__(self, model, capacity, variant):
        self.__model = model
        self.__capacity = capacity
        self.__variant = variant

    def get_model(self):
        return self.__model

    def get_capacity(self):
        return self.__capacity

    def set_capacity(self, capacity):
        self.__capacity = capacity

    def get_variant(self):
        return self.__variant

    def set_variant(self, variant):
        self.__variant = variant


class Vehicle(Taxi):
    def __init__(self, model, capacity, variant, color):
        super().__init__(model, capacity, variant)
        self.__color = color

    def vehicle_info(self):
        return self.get_model() + " " + self.get_variant() + " in " + self.__color \
               + " with " + self.get_capacity() + " seats"


v1 = Vehicle("i20 Active", "4", "SX", "Bronze")
print(v1.vehicle_info())
print(v1.get_model())

v2 = Vehicle("Fortuner", "7", "MT2755", "White")
print(v2.vehicle_info())
print(v2.get_model())
