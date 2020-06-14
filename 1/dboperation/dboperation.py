# from app import db
from model.model import *
from werkzeug.security import generate_password_hash, check_password_hash

def queryset():
    ans_data={}
    result = Setting_set.query.filter(Setting_set.SEname == '罚金单价').first()
    ans = Setting_set.query.filter(Setting_set.SEname == '预约天数').first()
    res = Setting_set.query.filter(Setting_set.SEname == '借阅天数').first()
    if result:
        ans_data['cost']=result.SEvalue
    if ans:
        ans_data['borrowdays']=ans.SEvalue
    if res:
        ans_data['reservedays']=res.SEvalue
    return ans_data

def upsetting(value={}):
    if value:
        result = Setting_set.query.filter(Setting_set.SEname == '罚金单价').first()
        result.SEvalue=value['cost']
        db.session.commit()
        ans = Setting_set.query.filter(Setting_set.SEname == '预约天数').first()
        ans.SEvalue=value['reservedays']
        db.session.commit()
        res = Setting_set.query.filter(Setting_set.SEname == '借阅天数').first()
        res.SEvalue=value['borrowdays']
        db.session.commit()
        return True
    return False



def delnum(isbn):
    res = queryAccordingToID('pbook', isbn)
    res.num = res.num - 1
    db.session.commit()
    print("删除成功")


def addnum(isbn):
    res = queryAccordingToID('pbook', isbn)
    res.num = res.num + 1
    db.session.commit()
    print("num增加成功")


def accordingToISBN(isbn=''):
    result = Book.query.filter(Book.ISBN == isbn)
    return result


def accordingTobname(bname=''):
    result = PBook.query.filter(PBook.Bname == bname)
    return result


def accordingTorname(rname=''):
    # rname='刘洋'
    result = Reader.query.filter(Reader.Rname == rname)
    print("accordingTorname:",rname)
    # print(result)
    print('*'*50)
    for rec in result:
        print(rec)
    return result


def test():
    res = accordingToISBN('1000000000')
    for rec in res:
        print(rec)


if __name__ == "__main__":
    accordingTorname()


# reader Remark的解码函数
def getNote(par):
    if par == 0:
        return ''
    par_bin = reversed(str(bin(par)))
    ans = ''
    temp = 0
    par_ten = ''
    for c in par_bin:
        temp = temp + 1
        if c == 'b':
            break
        if c == '1':
            par_ten = par_ten + str(temp)
    for c in par_ten:
        result = Remark_set.query.filter(Remark_set.REID == int(c)).first()
        ans = ans + ' ' + result.REname
    # for rec in result:
    # temp = list(result)
    print(ans)
    return ans


# 增加
# value 为 一个完整的对象
def add(value):
    db.session.add(value)
    db.session.commit()
    print("insert successfully")
    return True


# 查询
# detail是要查询的表，par是用来查询的参数
def queryAccordingToID(detail='None', par='None'):
    result = ''
    # 全部小写
    detail = detail.lower()
    # 去空格
    detail = detail.replace(" ", "")
    if detail == 'none' or par == 'none' or detail == '' or par == '':
        print("未传入查询目标")
    elif detail == 'administrator':
        result = Administrator.query.filter(Administrator.AID == par).first()
    elif detail == 'book':
        result = Book.query.filter(Book.BID == par).first()
    elif detail == 'reader':
        result = Reader.query.filter(Reader.RID == par).first()
    elif detail == 'pbook':
        result = PBook.query.filter(PBook.ISBN == par).first()
    elif detail == 'r_sta':
        result = R_sta.query.filter(R_sta.RID == par).first()
    print("queryAccordingToID:",par)
    print(result)
    return result


# 支持多个条件同时查询
def queryborrowRecords(rid='', bid='', botime='', rbtime1='', rbtime2=''):
    result = ''
    rid = rid.replace(" ", "")
    bid = bid.replace(" ", "")
    botime = botime.replace(" ", "")
    rbtime1 = rbtime1.replace(" ", "")
    rbtime2 = rbtime2.replace(" ", "")
    sql = 'select * from br_list where 1 = 1 '
    if rid == '' and bid == '' and botime == '' and rbtime1 == '' and rbtime2 == '':
        result = db.session.execute(sql)
        return result
    if rid != '' and rid != 'None':
        sql = sql + ' and rid= ' + rid
    if bid != '' and bid != 'None':
        sql = sql + ' and bid=' + bid
    if botime != '' and botime != 'None':
        sql = sql + ' and botime=' + botime
    if rbtime1 != '' and rbtime1 != 'None':
        sql = sql + ' and rbtime1=' + rbtime1
    if rbtime2 != '' and rbtime2 != 'None':
        sql = sql + ' and rbtime2=' + rbtime2
    result = db.session.execute(sql)
    return result

def delreservationReconds(rid='', bid='', aptime1=''):
    result = R_list.query.filter(R_list.RID == rid,R_list.BID==bid,R_list.Aptime1==aptime1).first()
    print(result)
    return  delt(result=result)


# 支持多个条件同时查询
def queryreservationReconds(rid='', bid='', aptime1='', aptime2=''):
    rid = rid.replace(" ", "")
    bid = bid.replace(" ", "")
    # aptime1 = aptime1.replace(" ", "")
    # aptime2 = aptime2.replace(" ", "")
    result = ''
    if rid != '' and bid != '' and aptime1 != '':
        result = R_list.query.filter(R_list.RID == rid, R_list.BID == bid, R_list.Aptime1 == aptime1)
    elif rid!='' and bid!='':
        result = R_list.query.filter(R_list.RID == rid, R_list.BID == bid)
    elif rid != '' :
        result = R_list.query.filter(R_list.RID == rid)
    return result


def delt(result=''):
    if result == '':
        print("delete unsuccessfully")
        return False
    db.session.delete(result)
    db.session.commit()
    return True


# 这是SB写法
# 依据传入的唯一主键id更新reader,book,pbook,administrator
# detail 为 reader,book,pbook,administrator的一种
# value 为修改的值，是一个完整的对象
def updateRecondsAccordingToID(detail='None', id='None', value='None'):
    result = False
    # 全部小写
    detail = detail.lower()
    # 去空格
    detail = detail.replace(" ", "")
    result = queryAccordingToID(detail, id)
    if not result:
        print("delete unsuccessfully!")
        return False
    db.session.delete(result)
    db.session.commit()
    print(result)
    if not add(value):
        print("update unsuccessfully")
    else:
        print("update successfully")


# 希望传入的对象value是字典
def updaterlist(value={}):
    if not value:
        print("value is null")
        return False
    result = queryreservationReconds(rid=value['rid'], bid=value['bid'], aptime1=value['starttime'])

    if not result:
        print("update unsuccessfully in updaterlist function")
        return False
    for rec in result:
        # rec = dict(rec.items())
        rec.Aptime2 = value['newdate']
        db.session.commit()
    return True


# 希望传入的对象value是字典
def updatebrlist(value={}):
    if not value:
        print("value is null")
        return False
    res = queryborrowRecords(rid=value['rid'], bid=value['bid'], botime=value['botime'])
    if not res:
        print("update unsuccessfully in updatebrlist function")
        return False
    res.RID = value['rid']
    res.BID = value['bid']
    res.Botime = value['botime']
    res.Rbtime1 = value['rbtime2']
    res.Rbtime2 = value['rbtime2']
    db.session.commit()
    return True


def updateBookInfo(info={}):
    if info:
        res = queryAccordingToID('pbook', info['isbn'])
        res.ISBN = info['newisbn']
        res.Bname = info['bname']
        res.Author = info['author']
        res.Pub = info['pub']
        res.Pyear = info['pyear']
        res.Per = info['per']
        db.session.commit()
        ans = queryAccordingToID('book', info['bid'])
        ans.BID = info['newbid']
        ans.Loc = info['loc']
        ans.Sta = info['sta']
        ans.Per = info['per']
        db.session.commit()
        return True
    else:
        print("修改失败")
        return False


def updateReaderInfo(info={}):
    if info:
        reader = queryAccordingToID(detail='reader', par=info['RID'])
        reader.Rname = info['Rname']
        reader.Rtel = info['Rtel']
        reader.Rem = info['Rem']
        pwd = info['Rpwd']
        if pwd != '':
            reader.Rpwd = generate_password_hash(pwd)
        db.session.commit()
        print("readerupdate 成功")
        return True
    return False
