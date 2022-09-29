# @Author : yan1079
# @Time : 2022/8/12 11:11

# class TestA:
#     def __init__(self,a, b):
#         self.a = a
#         self.b = b
#
#     def get_mes(self):
#         print("这是一个："+self.a+self.b)
#
#     def __new__(cls, a, b):
#         if a<10 and b>15:
#             object.__new__(cls)
#         else:
#             print("请传入正确的a、b的值")
#
#     def __str__(self):
#         return f'{self.__class__.__name__}({self.__dict__})'
#
# if __name__ == '__main__':
#     print(TestA(2, 31))
#     # aa.get_mes()


# import hashlib
#
# # m = hashlib.sha256()
# m = hashlib.md5()
# s = "YANP1017"+"q1w2e3r4"
# m.update(s.encode("utf-8"))
#
# print(m.digest())
# print(m.hexdigest())
# print(m.block_size)
# print(m.digest_size)


aa  = 'jksdjnkls'
print(aa[:-3])
