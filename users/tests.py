# class Person:
#     def __init__(self, name, age):
#         self.name = name
#         self.age = age
#
# person = Person("Alice", 25)
# setattr(person, "age", 30)
# def fun2(a):
#     return a * 2
#
#
# class MyClass:
#     instances = 0
#
#     def __init__(self, fun1):
#         self.a = fun1
#
#     def __call__(self, son, *args, **kwargs):
#         return self.a(son * 3)
#
#
# obj = MyClass(fun2)(2)
# print(obj)
import requests

from bs4 import BeautifulSoup

# url = "https://www.mediapark.uz/products/view/15591"
# page = requests.get(url)
# soup = BeautifulSoup(page.content, 'html.parser')
# title = soup.find_all("title", limit=1)[0].getText()
# string = ""
# for i in title[-4::-1]:
#     if i == " ":
#         continue
#     elif i.isnumeric():
#         string += i
#     else:
#         break
# print(string[::-1])
for i in range(15000):
    response = requests.get(url=f"http://31.42.191.53:4812/radiusut/hs/radius_bot/products/all?list=s23",
                            auth=("django_admin", "DJango_96547456")).json()
    print(i, response)