from dboperation.dboperation import *
# 增加管理员
#AID为主键
# admin = Administrator(AID='2012', Aname='liukai', Apwd=generate_password_hash('2589635'))
# if add(admin):
#     print("管理员添加成功")
# else:
#     print("管理员添加失败")

# 添加书
# BID为主键，ISBN为外键，所以添加的数据ＩＳＢＮ必须存在
# B1 = Book(BID='1008',ISBN='1000000000',Loc='34-2-3-9',Sta='borrowed',Per='Peter Biship')
# # if add(B1):
# #     print("图书添加成功")
# # else:
# #     print("图书添加失败")

# 添加书目
# ISBN 为主键
# PB1 = PBook(ISBN='1000000008',Bname='你好',Author='是我',Pub='帅哥出版社',Pyear=datetime.date(2011,4,5),num=6,Per='you')
# if add(PB1):
#     print("图书添加成功")
# else:
#     print("图书添加失败")

# 添加借阅历史
# BID RID 为主键和外键
# BR1 = BR_list(RID='1000',BID='1008')
# if add(BR1):
#     print("借阅历史添加成功")
# else:
#     print("借阅历史添加失败")

# 添加读者
# R1 = Reader(RID='1003',Rname='刘庆',Rtel='18817292161',Rem='email@163.com',Rpwd=generate_password_hash('121121'))
# if add(R1):
#     print("读者添加成功")
# else:
#     print("读者添加失败")