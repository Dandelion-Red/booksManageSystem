from flask import render_template, flash, redirect, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from app import app
import copy


@app.route('/', methods=['GET', 'POST'])
def index():
    # info = {'RID': '1001', 'Rname': 'jacken', 'Rtel': '18817', 'Rem': 'f@13'}
    info = ''
    temp = ''
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    # from model.model import Administrator
    username = request.form.get('account')
    pwd = request.form.get('password')
    print("username:", username)
    print("pwd:", pwd)
    loginUser = {

        'rid': '2332',
        'account': 'jiangkun',
        'name': '江琨',
        'sex': 'nan'
    }
    res_data = {
        'loginUser': loginUser,
        'result': 'yes',
        'condi': 1
    }
    return jsonify(res_data)


@app.route('/__webpack_hmr')
def npm():
    return redirect('http://localhost:8080/__webpack_hmr')


@app.route('/reserveRrecord', methods=['GET', 'POST'])
def reserveRrecord():
    from dboperation.dboperation import queryreservationReconds, queryAccordingToID
    ans = []
    rec={}
    if request.method == 'POST':
        rid = request.form['rid']
        print('rid=',rid)
        if rid:
            result = queryreservationReconds(rid=rid)
            print(result)
            for record in result:
                print("进入result!:")
                # rec = dict(rec.items())
                temp1 = queryAccordingToID('book', record.BID)
                print('='*50)
                # print('rec[bid]=',rec['BID'])
                print('=' * 50)
                temp2 = queryAccordingToID('pbook', temp1.ISBN)
                rec['BID'] = record.BID
                rec['Bname'] = temp2.Bname
                rec['RID'] = rid
                if record.Status:
                    rec['Status'] = '预约满足，请自取'
                else:
                    rec['Status'] = '预约中'
                rec['Aptime1'] = record.Aptime1
                rec['Aptime2'] = record.Aptime2
                ans.append(copy.deepcopy(rec))
            print(ans)
            ans_data = {
                'reserveRrecord': ans,
                'status': 'ok'
            }
            return jsonify(ans_data)
    ans_data = {
        'reserveRrecord': '',
        'status': 'failed'
    }
    return jsonify(ans_data)


@app.route('/updateReserve', methods=['GET', 'POST'])
def updateReserve():
    from dboperation.dboperation import updaterlist
    import datetime
    ans = {}
    if request.method == 'POST':
        ans['rid'] = request.form['rid']
        ans['bid'] = request.form['bid']
        ans['newdate']=request.form['newdate']
        ans['starttime']=request.form['starttime']
        print(ans['starttime'])
        ans['starttime'] = datetime.datetime.strptime(ans['starttime'], '%Y-%m-%d')
        print(ans['starttime'])
        if updaterlist(ans):
            ans_data={
                'status': 'ok',
                'reserveRrecord':ans,
            }
            return jsonify(ans_data)
    ans_data = {
        'status': 'failed',
        'reserveRrecord': ans,
    }
    return jsonify(ans_data)

@app.route('/delReserve', methods=['GET', 'POST'])
def delReserve():
    from dboperation.dboperation import queryreservationReconds,delreservationReconds
    import datetime
    value = {}
    if request.method == 'POST':
        value['rid'] = request.form['rid']
        value['bid'] = request.form['bid']
        value['starttime']=request.form['starttime']
        value['starttime'] = datetime.datetime.strptime(value['starttime'], '%Y-%m-%d')
        print(type(value['starttime']))
        print(value['starttime'])
        # ans = queryreservationReconds(rid=value['rid'], bid=value['bid'], aptime1=value['starttime'])
        # for rec in ans:
        #     print(rec)
        if delreservationReconds(rid=value['rid'],bid=value['bid'],aptime1=value['starttime']):
            ans_data={
                'status':'ok',
            }
            return jsonify(ans_data)
    ans_data = {
        'status': 'failed',
    }
    return jsonify(ans_data)



@app.route('/readerNote/<rid>', methods=['GET', 'POST'])
def readerNote(rid):
    from dboperation.dboperation import queryAccordingToID, getNote
    import copy, datetime
    ans = borrowReconds(rid)
    hasPenalty = []
    hasDue = []
    borrowing = []
    for rec in ans:
        # 存在罚金
        if rec['Penalty'] != 0:
            hasPenalty.append(copy.deepcopy(rec))
        # 超期未还
        if rec['Rbtime1'] > datetime.datetime.now():
            hasDue.append(copy.deepcopy(rec))
        # 正在借阅
        if not rec['Rbtime2']:
            borrowing.append(copy.deepcopy(rec))
    return render_template('readerNote.html', borrowing=borrowing, hasDue=hasDue, hasPenalty=hasPenalty)


# ======================================================================================================

#
# # 获取读者信息展示
# @app.route('/render_readerQuery', methods=['GET', 'POST'])
# def render_readerQuery(rid=''):
#     if request.method == 'POST':
#         rid = request.form['rid']
#     reader = readerQuery(rid)
#     return render_template('readerManage.html', info=reader)


@app.route('/render_readerQuery', methods=['GET', 'POST'])
def render_readerQuery():
    if request.method == 'POST':
        rid = request.form['account']
        rname = request.form['name']
        print("rid=", rid)
        readers = readerQuery(rid=rid, rname=rname)
        ans_data = {
            'readers': readers
        }
        return jsonify(ans_data)


@app.route('/showBookInfo/<string:bid>', methods=['GET', 'POST'])
def showBookInfo(bid):
    from dboperation.dboperation import updateBookInfo, queryAccordingToID
    book = {}
    result = queryAccordingToID('book', bid)
    ans = queryAccordingToID('pbook', result.ISBN)
    print("result:", result)
    print("ans: ", ans)
    book['BID'] = result.BID
    book['ISBN'] = result.ISBN
    book['Loc'] = result.Loc
    book['Sta'] = result.Sta
    book['Bname'] = ans.Bname
    book['Author'] = ans.Author
    book['Pub'] = ans.Pub
    book['Pyear'] = ans.Pyear
    book['Per'] = ans.Per
    return render_template('bookupdate.html', record=book)


@app.route('/bookupdate', methods=['GET', 'POST'])
def bookupdate():
    from dboperation.dboperation import updateBookInfo, queryAccordingToID
    bookinfo = {}
    book = {}
    if request.method == 'POST':
        bookinfo['newbid'] = request.form['newbid']
        bookinfo['bid'] = request.form['bid']
        bookinfo['newisbn'] = request.form['newisbn']
        bookinfo['isbn'] = request.form['isbn']
        bookinfo['bname'] = request.form['bname']
        bookinfo['author'] = request.form['author']
        bookinfo['pub'] = request.form['pub']
        bookinfo['sta'] = request.form['sta']
        bookinfo['pyear'] = request.form['pyear']
        bookinfo['loc'] = request.form['loc']
        bookinfo['per'] = request.form['per']
        if updateBookInfo(info=bookinfo):
            result = queryAccordingToID('book', bookinfo['newbid'])
            ans = queryAccordingToID('pbook', result.ISBN)
            book['BID'] = result.BID
            book['ISBN'] = result.ISBN
            book['Loc'] = result.Loc
            book['Sta'] = result.Sta
            book['Bname'] = ans.Bname
            book['Author'] = ans.Author
            book['Pub'] = ans.Pub
            book['Pyear'] = ans.Pyear
            book['Per'] = ans.Per
            return render_template('bookupdate.html', result=book)
    return render_template('bookupdate.html', result=book)
    # result = queryAccordingToID('book', bid)
    # ans = queryAccordingToID('pbook', result.ISBN)
    # print("result:", result)
    # print("ans: ", ans)
    # book['BID'] = result.BID
    # book['ISBN'] = result.ISBN
    # book['Loc'] = result.Loc
    # book['Sta'] = result.Sta
    # book['Bname'] = ans.Bname
    # book['Author'] = ans.Author
    # book['Pub'] = ans.Pub
    # book['Pyear'] = ans.Pyear
    # book['Per'] = ans.Per
    # return render_template('bookupdate.html', record=book)
    # ans['BID'] = book['BID']
    # ans['ISBN'] = book['ISBN']
    # ans['Loc'] = book['Loc']
    # ans['Sta'] = book['Sta']
    # ans['Bname'] = book['Bname']
    # ans['Author'] = book['Author']
    # ans['Pub'] = book['Pub']
    # ans['Pyear'] = book['Pyear']
    # ans['Per'] = book['Per']


@app.route('/readeradd', methods=['POST'])
def readeradd():
    from model.model import Reader, R_sta
    from dboperation.dboperation import queryAccordingToID, add, addnum
    if request.method == 'POST':
        print("=====================in readeradd ======================================")
        print(request.form)
        rid = request.form['account']
        normal = request.form['normal']
        if normal == '1':
            normal = True
        else:
            normal = False
        rname = request.form['name']
        tel = request.form['tel']
        ema = request.form['ema']
        password = request.form['pwd']
        pwd = generate_password_hash(password)
        remark = request.form['remark']

        reader = Reader(RID=rid, Rname=rname, Rtel=tel, Rem=ema, Rpwd=pwd)
        reader_sta = R_sta(RID=rid, Normal=normal, Remark=remark)
        add(reader)
        add(reader_sta)

        print(reader)
        print(reader_sta)
        ans_data = {
            'rid': rid,
            'status': 'ok'
        }
        return jsonify(ans_data)
    ans_data = {
        'rid': '',
        'status': 'fail'
    }
    return jsonify(ans_data)


# 图书添加
@app.route('/bookadd', methods=['POST'])
def bookadd():
    from model.model import Book, PBook
    from dboperation.dboperation import queryAccordingToID, add, addnum

    if request.method == 'POST':
        print("=====================in bookadd ======================================")
        print(request.form)
        bid = request.form['bid']
        isbn = request.form['isbn']
        bname = request.form['bname']
        author = request.form['author']
        pub = request.form['pub']
        sta = request.form['sta']
        pyear = request.form['pyear']
        loc = request.form['loc']
        print("bookadd:bid:", bid)
        per = request.form['per']
        print("bookadd:isbn:", isbn)
        res = queryAccordingToID('pbook', isbn)
        book = Book(BID=bid, ISBN=isbn, Loc=loc, Sta=sta, Per=per)
        pbook = PBook(ISBN=isbn, Bname=bname, Author=author, Pub=pub, Pyear=pyear, num=1, Per=per)
        if not res:
            add(pbook)
            add(book)
        else:
            addnum(isbn)
            add(book)
        print("bookadd:bid:", bid)
        ans = bookQuery(detail='bid', bid=bid)
        print("在这里")
        print(ans)
        ans_data = {
            'isbn': isbn,
            'status': 'ok'
        }
        return jsonify(ans_data)


# @app.route('/bookaddcopy', methods=['GET','POST'])
@app.route('/bookaddcopy', methods=['GET', 'POST'])
def bookaddcopy():
    from model.model import Book, PBook
    from dboperation.dboperation import queryAccordingToID, add, addnum
    book = {}
    if request.method == 'POST':
        bid = request.form['bid']
        oldbid = request.form['oldbid']
        sta = request.form['sta']
        print(bid, sta)
        temp_ans = queryAccordingToID(detail='book', par=bid)
        if not temp_ans:
            ans = queryAccordingToID(detail='book', par=oldbid)
            loc = ans.Loc
            per = ans.Per
            isbn = ans.ISBN
            result = queryAccordingToID(detail='pbook', par=ans.ISBN)
            bname = result.Bname
            author = result.Author
            pub = result.Pub
            pyear = result.Pyear
            book = Book(BID=bid, ISBN=isbn, Loc=loc, Sta=sta, Per=per)
            pbook = PBook(ISBN=isbn, Bname=bname, Author=author, Pub=pub, Pyear=pyear, num=1, Per=per)
            addnum(isbn)
            add(book)
            ans_data = {
                'bid': bid,
                'status': 'ok'
            }
            return jsonify(ans_data)
    ans_data = {
        'bid': '',
        'status': 'fail'
    }
    return jsonify(ans_data)


#
# @app.route('/bookaddcopy', methods=['GET','POST'])
# def bookaddcopy():
#     if request.method == 'POST':
#         bid=request.form['bid']
#         print(bid)
#         ans_data = {
#             'book': {},
#             'status': 'fail'
#         }
#         return jsonify(ans_data)


@app.route('/delreader/<string:rid>', methods=['GET'])
def delreader(rid):
    from dboperation.dboperation import queryAccordingToID, accordingToISBN, delt, delnum
    if request.method == "GET":
        print("==============================in delreader===============================")
        print("rid", rid)
        res = queryAccordingToID(detail='reader', par=rid)
        ans = queryAccordingToID(detail='r_sta', par=res.RID)
        delt(ans)
        delt(res)
        ans_data = {
            'status': 'ok',
            'rid': rid,
        }
        return jsonify(ans_data)
    ans_data = {
        'status': 'fail',
        'rid': rid,
    }
    return jsonify(ans_data)


@app.route('/delbook/<string:bid>', methods=['GET'])
def delbook(bid):
    from dboperation.dboperation import queryAccordingToID, accordingToISBN, delt, delnum
    if request.method == "GET":
        print("==============================in delbook===============================")
        print("bid", bid)
        res = queryAccordingToID(detail='book', par=bid)
        isbn = res.ISBN
        ans = queryAccordingToID(detail='pbook', par=isbn)
        if ans.num == 0:
            delt(res)
            delt(ans)
        if ans.num != 0:
            delnum(isbn)
            delt(res)
            print("num!=0")
        ans_data = {
            'status': 'ok',
            'isbn': isbn,
        }
        return jsonify(ans_data)


# 图书查询
@app.route('/render_bookQuery', methods=['GET', 'POST'])
def render_bookQuery():
    from dboperation.dboperation import queryAccordingToID, accordingToISBN
    # book = {}
    books = []
    detail = ''
    # num = 0
    if request.method == 'POST':
        print("========in render_bookQuery======================")
        print(request.form)
        bid = request.form['bid']
        isbn = request.form['isbn']
        bname = request.form['title']
        if bid != '':
            detail = 'bid'
            books = bookQuery(detail=detail, bid=bid)
        elif isbn != '':
            detail = 'isbn'
            books = bookQuery(detail=detail, isbn=isbn)
        elif bname != '':
            detail = 'bname'
            books = bookQuery(detail=detail, bname=bname)
        print('detail ', detail)

    #     bid = request.form['bid']
    #     isbn = request.form['isbn']
    #     books = bookQuery(detail, bid, isbn)
    # print("renderQuerybooks:", books)
    print(books)
    res_data = {
        'books': books
    }
    return jsonify(res_data)


# 根据bid 或者 ISBN来查询图书结果
# 返回books
def bookQuery(detail, bid='', isbn='', bname=''):
    from dboperation.dboperation import queryAccordingToID, accordingToISBN, accordingTobname
    book = {}
    books = []
    if detail == 'bid':
        result = queryAccordingToID('book', bid)
        if not result:
            return books
        ans = queryAccordingToID('pbook', result.ISBN)
        book['BID'] = result.BID
        book['ISBN'] = result.ISBN
        book['Loc'] = result.Loc
        book['Sta'] = result.Sta
        book['Bname'] = ans.Bname
        book['Author'] = ans.Author
        book['Pub'] = ans.Pub
        book['Pyear'] = ans.Pyear
        # book['Num'] = num
        book['Per'] = ans.Per
        books.append(copy.deepcopy(book))
    elif detail == 'isbn':
        ans = queryAccordingToID('pbook', isbn)
        if ans:
            book['Bname'] = ans.Bname
            book['Author'] = ans.Author
            book['Pub'] = ans.Pub
            book['Pyear'] = ans.Pyear
            book['ISBN'] = ans.ISBN
            #           接下来是要写查询book的内容
            result = accordingToISBN(isbn)
            for rec in result:
                # num = num + 1
                print(rec)
                # print("num:",num)
                book['BID'] = rec.BID
                book['Loc'] = rec.Loc
                book['Sta'] = rec.Sta
                book['Per'] = rec.Per
                # book['Num'] = num
                print(book)
                books.append(copy.deepcopy(book))
            print('*' * 40)
            print(books)
    elif detail == 'bname':
        result = accordingTobname(bname)
        for rec in result:
            book['Bname'] = rec.Bname
            book['Author'] = rec.Author
            book['Pub'] = rec.Pub
            book['Pyear'] = rec.Pyear
            book['ISBN'] = rec.ISBN
            ans = accordingToISBN(rec.ISBN)
            for eve in ans:
                book['BID'] = eve.BID
                book['Loc'] = eve.Loc
                book['Sta'] = eve.Sta
                book['Per'] = eve.Per
                print(book)
                books.append(copy.deepcopy(book))
    return books


# 查询借阅历史
@app.route('/render_borrowHistory/<string:rid>', methods=['GET', 'POST'])
def render_borrowHistory(rid):
    import datetime
    # ans = []
    # if request.method == 'POST':
    #     rid = request.form['rid']
    print("rid=", rid)
    if rid != '':
        res = borrowReconds(rid)
        reader = readerQuery(rid=rid)
        if res and reader:
            ans_data = {
                'borrowrecords': res,
                'status': 'ok',
                'readername': reader[0]['Rname']
            }
            return jsonify(ans_data)
    ans_data = {
        'borrowrecords': '',
        'status': 'fail',
        'readername': '',
        'time': datetime.datetime.now()
    }
    return jsonify(ans_data)


# 查询正在借阅的图书
@app.route('/render_borrowReconds', methods=['GET', 'POST'])
def render_borrowReconds(rid=''):
    ans = []
    if request.method == 'POST':
        rid = request.form['rid']
    ans = borrowReconds(rid)
    return render_template('borrowing.html', rid=rid, info=ans)


@app.route('/readerupdate', methods=['GET', 'POST'])
def readerupdate():
    from dboperation.dboperation import updateReaderInfo
    reader = {}
    if request.method == 'POST':
        reader['RID'] = request.form['id']
        reader['Rname'] = request.form['rname']
        reader['Rtel'] = request.form['rtel']
        reader['Rem'] = request.form['rem']
        reader['Rpwd'] = request.form['rpwd']
        if updateReaderInfo(info=reader):
            result = readerQuery(reader['RID'])
            flash("修改成功,结果如下")
            return render_template('readerManage.html', info=result)
    flash("修改失败,请重新操作")
    return render_template('readerManage.html', info='')


# 输入rid  输出reader
def readerQuery(rid='', rname=''):
    from dboperation.dboperation import queryAccordingToID, getNote, accordingTorname
    readers = []
    reader = {}
    if rid != '':
        result = queryAccordingToID('reader', rid)
        ans = queryAccordingToID('r_sta', rid)
        note = ''
        if not result or not ans:
            print("这是在读者管理界面，没有找到对应RID")
            # reader = ''
        else:
            print("ans_remarik:", ans.Remark)
            note = getNote(ans.Remark)
            reader['RID'] = result.RID
            reader['Rname'] = result.Rname
            reader['Rtel'] = result.Rtel
            reader['Rem'] = result.Rem
            reader['condi'] = '学生'
            # reader['condi'] = '学生'
            if ans.Normal:
                reader['Normal'] = '正常'
            else:
                reader['Normal'] = '异常'
            reader['Remark'] = note
            readers.append(copy.deepcopy(reader))
        print("readers:", readers)
        return readers
    elif rname != '':
        res = accordingTorname(rname=rname)
        print("readers:", res)
        for rec in res:
            print("=" * 70)
            print(rec)
            result = queryAccordingToID('reader', rec.RID)
            ans = queryAccordingToID('r_sta', rec.RID)
            note = getNote(ans.Remark)
            reader['RID'] = result.RID
            reader['Rname'] = result.Rname
            reader['Rtel'] = result.Rtel
            reader['Rem'] = result.Rem
            reader['condi'] = '学生'
            if ans.Normal:
                reader['Normal'] = '正常'
            else:
                reader['Normal'] = '异常'
            reader['Remark'] = note
            readers.append(copy.deepcopy(reader))
        print("readers:", readers)
        return readers


def borrowReconds(rid='', bid='', botime='', rbtime1='', rbtime2=''):
    from dboperation.dboperation import queryborrowRecords, queryAccordingToID
    import datetime
    result = queryborrowRecords(rid=rid, bid=bid, botime=botime, rbtime1=rbtime1, rbtime2=rbtime2)
    print('borrowReconds函数下的result')
    print('rid:' + rid)
    ans = []
    # num = 0
    print("result:")
    # print(type(result))
    for rec in result:
        # print(type(rec))
        print("进入result!:")
        # num = num + 1
        # print("num:", num)
        rec = dict(rec.items())
        temp1 = queryAccordingToID('book', rec['BID'])
        temp2 = queryAccordingToID('pbook', temp1.ISBN)
        rec['ISBN'] = temp2.ISBN
        rec['Bname'] = temp2.Bname
        if not rec['Rbtime2']:
            rec['Condi'] = '未归还'
            if rec['Rbtime1'] > datetime.datetime.now():
                rec['Condi'] = '已超期'
            rec['Rbtime2'] = rec['Condi']
        else:
            if rec['Penalty']:
                rec['Condi'] = '罚金' + str(rec['Penalty'])
        ans.append(copy.deepcopy(rec))
        # print(type(rec))
    print("================================================================================")
    for rec in ans:
        print(rec)
    print("================================================================================")
    return ans
