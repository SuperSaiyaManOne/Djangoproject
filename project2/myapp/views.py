from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime

def test1(request):
    return HttpResponse("Hello World")

def hello1(request,username):
    return HttpResponse("Hello "+username)

def hello2(request,username):
    now = datetime.now()
    # print(now)
    # print(username)
    # return HttpResponse("test...")
    return render(request, "hello2.html",locals())

from django.db import connections ##從django.db模組中導入connections物件，用於管理資料庫連接
def list(request): #定義一個函數list，接收一個參數request，表示網頁請求
    if 'cName' in request.GET: #如果請求中有cName這個參數，表示要查詢特定的學生姓名
        cName = request.GET["cName"] #從請求中獲取cName的值，賦給變數cName
        # print(cName)
        # print("test1...")
        # sql = "select * from myapp_student where cName=%s" #用這語法太嚴格
        sql = "select * from myapp_student where cName like %s" #定義一個sql語句，用於從myapp_student這個資料表中查詢符合cName條件的所有欄位
        # print(sql)
        cName = "%%"+cName+"%%" #這邊的 % 是特殊符號，所以要打兩個讓系統知道這是特殊符號
        #將cName的值加上兩個百分號，表示要模糊匹配，例如cName為"王"，則會查詢包含"王"的所有姓名
        val = [cName] #將cName的值放入一個列表中，賦給變數val，用於傳遞給sql語句的參數
    else: #如果請求中沒有cName這個參數，表示要查詢所有的學生資料
        sql = "select * from myapp_student" #定義一個sql語句，用於從myapp_student這個資料表中查詢所有的欄位
        # print("test2...")
        val = [] #定義一個空列表，賦給變數val，表示沒有參數要傳遞給sql語句

    cursor = connections["default"].cursor()
    #從connections物件中獲取名為"default"的資料庫連接，並創建一個游標物件，賦給變數cursor，用於執行sql語句和獲取結果
    cursor.execute(sql,val)
    #使用cursor物件的execute方法，執行sql語句，並將val作為參數傳遞
    result = cursor.fetchall()
    #使用cursor物件的fetchall方法，獲取所有的查詢結果，賦給變數result，它是一個二維的元組，每一個元素是一個一維的元組，表示一條資料
    # print(result)

    #取得資料庫的欄位名稱
    field_name = cursor.description
    #使用cursor物件的description屬性，獲取資料表的欄位名稱，賦給變數field_name，它是一個一維的元組，每一個元素是一個元組，表示一個欄位的資訊
    # print(fiel_name)
    cursor.close() #使用cursor物件的close方法，關閉游標，釋放資源

    #轉換格式
    resultList=[] #定義一個空列表，賦給變數resultList，用於存儲轉換後的查詢結果
    for data in result: #遍歷result中的每一條資料，賦給變數data
        # print(data)
        i=0 #定義一個變數i，賦值為0，用於記錄欄位的索引
        dict_data={} #定義一個空字典，賦給變數dict_data，用於存儲一條資料的鍵值對
        for d in data: #遍歷data中的每一個欄位值，賦給變數d
            # print(d)
            dict_data[field_name[i][0]]=d
            #將欄位名稱作為鍵，欄位值作為值，存入dict_data中，注意field_name[i][0]表示第i個欄位的第0個資訊，也就是欄位名稱
            # dict_data["id"]=1
            # dict_data["cName"]="簡鳳君"
            i=i+1 #將i的值加1，用於遍歷下一個欄位
        # print(dict_data)
        resultList.append(dict_data) #將dict_data加入到resultList中，表示一條資料的轉換完成
    print(resultList) #打印resultList，用於測試
    #以下判斷有沒有資料
    if not resultList: #如果resultList為空，表示沒有查詢到任何資料
        errormessage="無此資料" #定義一個變數errormessage，賦值為"無此資料"，用於顯示錯誤訊息
    else: #如果resultList不為空，表示查詢到了資料
        errormessage="" #定義一個變數errormessage，賦值為空字串，表示沒有錯誤訊息
    print(errormessage) #打印errormessage，用於測試

    # return HttpResponse("Hello World")
    return render(request, "list.html", locals())
    #使用django的render函數，將request、"list.html"和locals()作為參數傳遞，返回一個HttpResponse物件，表示網頁的回應，locals()是一個內建函數，它會返回一個字典，包含當前作用域中的所有變數，這樣就可以在list.html中使用這些變數

def search_name(request):
    return render(request, "search_name.html",locals())

def index(request): #顯示筆數、新增、搜尋、預設顯示所有資料
    if 'site_search' in request.GET:
        site_search = request.GET["site_search"]
        site_search = site_search.strip() #去掉輸入是空白的字元
        # print(sit_search)
        #sinagle keyword
        # site_search = "%%"+site_search+"%%" #關鍵是這邊，先把全部變成 %%
        # sql = "select * from myapp_student where "
        # sql += " cName like '%s'" %(site_search)
        # sql += " or cSex like '%s'" %(site_search)
        # sql += " or cBirthday like '%s'" %(site_search)
        # sql += " or cEmail like '%s'" %(site_search)
        # sql += " or cPhone like '%s'" %(site_search)
        # sql += " or cAddr like '%s'" %(site_search)
        # print(sql)

        #mutiple key words
        # select * from myapp_student where cName like 'abc' or cSex like 'abc' or cBirthday like 'abc'
        # or cBirthday like 'abc' or cEmail like 'abc' or cPhone like 'abc' or cAddr like 'abc'
        # or cName like 'def ' or cSex like 'def'
        # or cBirthday like 'def' or cEmail like 'def' or cPhone like 'def' or cAddr like 'def'
         
        sql = "select * from myapp_student "
        keywords = site_search.split(" ") #字元切割
        print(keywords)
        key_index=0
        for keyword in keywords:
            if keyword != "": #判斷是不是沒東西
                keyword = "%%"+keyword+"%%" #如果沒東西，用%%去判斷
                if key_index == 0:
                    sql += "where cName like '%s'" %(keyword)
                else:
                    sql += "or cName like '%s'" %(keyword)
                sql += "or cSex like '%s'" %(keyword)
                sql += "or cBirthday like '%s'" %(keyword)
                sql += "or cEmail like '%s'" %(keyword)
                sql += "or cPhone like '%s'" %(keyword)
                sql += "or cAddr like '%s'" %(keyword)
                key_index = key_index + 1
    else:
        sql = "select * from myapp_student"
    cursor = connections["default"].cursor() #連接資料庫
    cursor.execute(sql,[]) #執行sql語法
    result = cursor.fetchall() #取得資料
    # print(result)
    field_name = cursor.description #取得資料庫的欄位名稱
    # print(fiel_name)
    cursor.close()

    #-----------------
    #轉換格式 #固定寫法
    resultList=[]
    for data in result:
        # print(data)
        i=0
        dict_data={}
        for d in data:
            # print(d)
            dict_data[field_name[i][0]]=d
            # dict_data["id"]=1
            # dict_data["cName"]="簡鳳君"
            i=i+1
        # print(dict_data)
    #-----------------
        resultList.append(dict_data)
    # print(resultList)
    data_count = len(resultList) #用來偵測"資料長度"
    # print(data_count)

    #以下判斷有沒有資料，這邊有再新增true跟false
    if not resultList:
        errormessage="無此資料"
        status = False
    else:
        errormessage=""
        status = True

    # return HttpResponse("Hello World")
    return render(request, "index.html", locals())

from django.shortcuts import redirect
def post1(request):
    if request.method == "POST":
        cName = request.POST["cName"]
        cSex = request.POST["cSex"]
        cBirthday = request.POST["cBirthday"]
        cEmail = request.POST["cEmail"]
        cPhone = request.POST["cPhone"]
        cAddr = request.POST["cAddr"]
        print("{}:{}:{}:{}:{}".format(cName,cSex,cBirthday,cEmail,cPhone,cAddr))
        # insert into myapp_student (cName,cSex,cBirthday,cEmail,cPhone,cAddr)
        # values('abc','M`','2003-10-05','abc@yahoo.com.tw','0922','台北')
        sql ="insert into myapp_student (cName,cSex,cBirthday,cEmail,cPhone,cAddr)"
        sql += "values('%s','%s','%s','%s','%s','%s')"
        sql %= (cName,cSex,cBirthday,cEmail,cPhone,cAddr)
        print(sql)
        cursor = connections["default"].cursor() #連接資料庫
        cursor.execute(sql,[]) #執行sql語法
        cursor.close()
        return redirect("/index/")
        # return HttpResponse("Hello World")
    else:
        return render(request, "post1.html",locals())
    
def edit1(request, id=None, mode=None):
    if mode == "edit":
        # print(id)
        cName = request.GET["cName"]
        cSex = request.GET["cSex"]
        cBirthday = request.GET["cBirthday"]
        cEmail = request.GET["cEmail"]
        cPhone = request.GET["cPhone"]
        cAddr = request.GET["cAddr"]
        # print("{}:{}:{}:{}:{}".format(cName,cSex,cBirthday,cEmail,cPhone,cAddr))

        # update myapp_student set cName='aa', cSex='M', cBirthday='2023-10-11', cEmail='aa@yahoo.com.tw', cPhone='0922222222', cAddr='台北' where id=1

        sql = "update myapp_student set "
        sql += "cName='%s', cSex='%s', cBirthday='%s', cEmail='%s', cPhone='%s',cAddr='%s' where id=%s"
        sql %= (cName,cSex,cBirthday,cEmail,cPhone,cAddr,id)
        # print(sql)
        cursor = connections["default"].cursor() #連接資料庫
        cursor.execute(sql,[]) #執行sql語法
        cursor.close()
        return redirect("/index/")
        # return HttpResponse("test1")
    elif mode == "load":
        # print(id)
        # print(mode)
        # select * from myapp_student where id = 6
        sql = "select * from myapp_student where id = %s" %(id)
        print(sql)
        cursor = connections["default"].cursor() #連接資料庫
        cursor.execute(sql,[]) #執行sql語法
        result =cursor.fetchall() #取得資料
        # print(result)
        field_name = cursor.description #取得資料庫的欄位名稱
        # print(field_name)
        cursor.close()
        
        #-----------------
        #轉換格式 #固定寫法
        dict_data={}
        for data in result:
            # print(data)
            i=0
            for d in data:
                # print(d)
                dict_data[field_name[i][0]]=d
                i=i+1
        print(dict_data)
        #-----------------

        # return HttpResponse("test2")
        return render(request, "edit1.html",locals())

def edit2(request, id=None):
    print(id)
    if request.method == "POST":
        # print(id)
        cName = request.POST["cName"]
        cSex = request.POST["cSex"]
        cBirthday = request.POST["cBirthday"]
        cEmail = request.POST["cEmail"]
        cPhone = request.POST["cPhone"]
        cAddr = request.POST["cAddr"]
        # print("{}:{}:{}:{}:{}".format(cName,cSex,cBirthday,cEmail,cPhone,cAddr))

        sql = "update myapp_student set "
        sql += "cName='%s', cSex='%s', cBirthday='%s', cEmail='%s', cPhone='%s',cAddr='%s' where id=%s"
        sql %= (cName,cSex,cBirthday,cEmail,cPhone,cAddr,id)
        # print(sql)

        cursor = connections["default"].cursor() #連接資料庫
        cursor.execute(sql,[]) #執行sql語法
        cursor.close()
        return redirect("/index/")
        # return HttpResponse("test1")
    else:
        sql = "select * from myapp_student where id = %s" %(id)
        print(sql)
        cursor = connections["default"].cursor() #連接資料庫
        cursor.execute(sql,[]) #執行sql語法
        result =cursor.fetchall() #取得資料
        # print(result)
        field_name = cursor.description #取得資料庫的欄位名稱
        # print(field_name)
        cursor.close()
        
        #-----------------
        #轉換格式 #固定寫法
        dict_data={}
        for data in result:
            # print(data)
            i=0
            for d in data:
                # print(d)
                dict_data[field_name[i][0]]=d
                i=i+1
        print(dict_data)
        #-----------------

        # return HttpResponse("test2")
        return render(request, "edit2.html",locals())
    
def delete(request, id=None):
    print(id)
    if request.method == "POST":
        sql = "delete from myapp_student where id=%s"
        sql %= (id)
        # print(sql)
        cursor = connections["default"].cursor() #連接資料庫
        cursor.execute(sql,[]) #執行sql語法
        cursor.close()
        return redirect("/index/")
        # return HttpResponse("test1")
    else:
        sql = "select * from myapp_student where id = %s" %(id)
        print(sql)
        cursor = connections["default"].cursor() #連接資料庫
        cursor.execute(sql,[]) #執行sql語法
        result =cursor.fetchall() #取得資料
        # print(result)
        field_name = cursor.description #取得資料庫的欄位名稱
        # print(field_name)
        cursor.close()
        
        #-----------------
        #轉換格式 #固定寫法
        dict_data={}
        for data in result:
            # print(data)
            i=0
            for d in data:
                # print(d)
                dict_data[field_name[i][0]]=d
                i=i+1
        print(dict_data) #檢查碼在這裡
        #-----------------

        # return HttpResponse("test2")
        return render(request, "delete.html",locals())
    
#########################
# ★★ Web API ★★
from django.http import JsonResponse
def getAllItems(request):
    sql = "select * from myapp_student"
    cursor = connections["default"].cursor() #連接資料庫
    cursor.execute(sql,[]) #執行sql語法
    result = cursor.fetchall() #取得資料
    # print(result)
    # 取得資料庫的欄位名稱
    field_name = cursor.description
    # print(fiel_name)
    cursor.close()

    #轉換格式 #固定寫法 #↓↓↓↓↓↓↓
    resultList=[]
    for data in result:
        # print(data)
        i=0
        dict_data={}
        for d in data:
            # print(d)
            dict_data[field_name[i][0]]=d
            i=i+1
        # print(dict_data)
        resultList.append(dict_data)
    # print(resultList)
    #轉換格式 #固定寫法 #↑↑↑↑↑↑↑
    # return HttpResponse("test1")
    return JsonResponse(resultList,safe=False, json_dumps_params={'ensure_ascii':False})

def getItem(request, id=None):
    print(id)
    sql = "select * from myapp_student where id = %s" %(id)
    cursor = connections["default"].cursor() #連接資料庫
    cursor.execute(sql,[]) #執行sql語法
    result =cursor.fetchall() #取得資料
    # print(result)
    # 取得資料庫的欄位名稱
    field_name = cursor.description
    # print(field_name)
    cursor.close()

    #轉換格式 #固定寫法 #↓↓↓↓↓↓↓
    resultList=[]
    for data in result:
        # print(data)
        i=0
        dict_data={}
        for d in data:
            # print(d)
            dict_data[field_name[i][0]]=d
            i=i+1
        # print(dict_data)
        resultList.append(dict_data)
    print(resultList)
    #轉換格式 #固定寫法 #↑↑↑↑↑↑↑
    # return HttpResponse("test1")
    return JsonResponse(resultList,safe=False, json_dumps_params={'ensure_ascii':False})

from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def createItem(request):
    try:
        if request.method == "GET":
            cName = request.GET["cName"]
            cSex = request.GET["cSex"]
            cBirthday = request.GET["cBirthday"]
            cEmail = request.GET["cEmail"]
            cPhone = request.GET["cPhone"]
            cAddr = request.GET["cAddr"]
            print("...GET...")
            print("{}:{}:{}:{}:{}:{}".format(cName,cSex,cBirthday,cEmail,cPhone,cAddr))
            # return HttpResponse("createItem by GET")
        elif request.method == "POST":
            cName = request.POST["cName"]
            cSex = request.POST["cSex"]
            cBirthday = request.POST["cBirthday"]
            cEmail = request.POST["cEmail"]
            cPhone = request.POST["cPhone"]
            cAddr = request.POST["cAddr"]
            print("...POST...")
            print("{}:{}:{}:{}:{}:{}".format(cName,cSex,cBirthday,cEmail,cPhone,cAddr))
            # return HttpResponse("createItem by POST")
    except:
        return HttpResponse("createItem error")

    try:
        sql ="insert into myapp_student (cName,cSex,cBirthday,cEmail,cPhone,cAddr)"
        sql += "values('%s','%s','%s','%s','%s','%s')"
        sql %= (cName,cSex,cBirthday,cEmail,cPhone,cAddr)
        # print(sql)
        cursor = connections["default"].cursor() #連接資料庫
        cursor.execute(sql,[]) #執行sql語法
        affected_rows = cursor.rowcount
        print(affected_rows)
        cursor.close()
        if affected_rows == 0:
            return HttpResponse("false")
        else:
            return HttpResponse("true")
    except:
        return HttpResponse("sql execute error")
    

from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def updateItem(request, id=None):
    print(id)
    try:
        if request.method == "GET":
            cName = request.GET["cName"]
            cSex = request.GET["cSex"]
            cBirthday = request.GET["cBirthday"]
            cEmail = request.GET["cEmail"]
            cPhone = request.GET["cPhone"]
            cAddr = request.GET["cAddr"]
            print("...GET...")
            print("{}:{}:{}:{}:{}:{}".format(cName,cSex,cBirthday,cEmail,cPhone,cAddr))
            # return HttpResponse("updateItem by GET")
        elif request.method == "POST":
            cName = request.POST["cName"]
            cSex = request.POST["cSex"]
            cBirthday = request.POST["cBirthday"]
            cEmail = request.POST["cEmail"]
            cPhone = request.POST["cPhone"]
            cAddr = request.POST["cAddr"]
            print("...POST...")
            print("{}:{}:{}:{}:{}:{}".format(cName,cSex,cBirthday,cEmail,cPhone,cAddr))
            # return HttpResponse("updateItem by POST")
    except:
        return HttpResponse("updateItem error")
    try:
        sql = "update myapp_student set "
        sql += "cName='%s', cSex='%s', cBirthday='%s', cEmail='%s', cPhone='%s',cAddr='%s' where id=%s"
        sql %= (cName,cSex,cBirthday,cEmail,cPhone,cAddr,id)
        print(sql)
        cursor = connections["default"].cursor() #連接資料庫
        cursor.execute(sql,[]) #執行sql語法
        affected_rows = cursor.rowcount
        print(affected_rows)
        cursor.close()
        if affected_rows == 0:
            return HttpResponse("fasle")
        else:
            return HttpResponse("true")
    except:
        return HttpResponse("sql execute error")
        

from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def deleteItem(request, id=None):
    print(id)
    try:
        sql = "delete from myapp_student where id=%s "
        sql %= (id)
        # print(sql)
        cursor = connections["default"].cursor() #連接資料庫
        cursor.execute(sql,[]) #執行sql語法
        affected_rows = cursor.rowcount
        print(affected_rows)
        cursor.close()
        if affected_rows == 0:
            return HttpResponse("fasle")
        else:
            return HttpResponse("true")
    except:
        return HttpResponse("sql execute error")
