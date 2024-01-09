from django.shortcuts import render, redirect
from myapp import models

from django.http import HttpResponse                    # HttpResponse 網頁顯示
from datetime import datetime                           # datetime 顯示時間
import random                                           # random 隨機數字 0-255
from django.contrib.auth import authenticate
from django.contrib import auth
from myapp.models import personal_information as User


message = ''            # 錯誤訊息
commoditylist = []      # 購買商品串列
customname = ''         # 購買者姓名
customphone = ''        # 購買者電話
customaddress = ''      # 購買者地址
customemail = ''        # 購買者電子郵件



# 未登入 首頁檢視
def front_page_1(request):

    return render(request,"front_page_1.html",locals())


# 未登入 店家檢視
from django.db import connections
from myapp.models import yellow_pages        # ORM 抓取 SQL 資料庫 yellow_pages 資料表
from django.views.decorators.csrf import csrf_exempt    # 允許這個方法沒有安全機制
@csrf_exempt
def front_page(request):
    resultList = yellow_pages.objects.all().order_by("id")   # 顯示所有資料
    if not resultList:              # 錯誤訊息 查無資料的話
        errormessage="查無此資料"
        status = False
    else:
        errormessage=""
        status = True
    # return HttpResponse("這是測試頁")
    return render(request,"front_page.html",locals())


# 未登入 菜單檢視
from myapp.models import yellow_pages, menu_all  # 抓資料庫 店家資訊 和 菜單資訊
from django.views.decorators.csrf import csrf_exempt    # 允許這個方法沒有安全機制
@csrf_exempt
def menu(request, id=None):
    if request.method == "POST":
        
        return render(request, "checkout.html", locals())
    else:
        # sql = "select * from myapp_menu_all where (cSort_project = '中式' && cStore_Name = '無名早午餐')"       # 抓取資料庫中的 中式早餐
        if(id==2):
            sql = "select * from myapp_menu_all where (cSort_project = '中式' && cStore_Name = '無名早午餐')"
        elif(id==3):
            sql = "select * from myapp_menu_all where (cSort_project = '中式' && cStore_Name = '永和傳統豆漿')"
        elif(id==4):
            sql = "select * from myapp_menu_all where (cSort_project = '西式' && cStore_Name = '斜坡粉漿蛋餅')"
        elif(id==5):
            sql = "select * from myapp_menu_all where (cSort_project = '西式' && cStore_Name = '老八早點鋪')"
        elif(id==6):
            sql = "select * from myapp_menu_all where (cSort_project = '西式' && cStore_Name = '天天有氧')"
        elif(id==1):
            sql = "select * from myapp_menu_all where (cSort_project = '特色' && cStore_Name = '黃媽媽早點客家菜包')"
        
        cursor = connections["default"].cursor()# 連接資料庫
        cursor.execute(sql,[])# 執行 sql 語法
        result = cursor.fetchall()# 取得資料
        # print(result)
        # 取得欄位名稱
        field_name = cursor.description
        # print(field_name)
        cursor.close()# 關閉 資料庫

        resultList =[]# 轉換格式
        for data in result:
            # print(data)
            i = 0
            dict_data = {}
            for d in data:
                # print(d)
                dict_data[field_name[i][0]] = d
                # dict_data["id"] = 1               # 顯示方式
                # dict_data["cName"] = "簡奉君"
                i += 1
            # print(dict_data)
            resultList.append(dict_data)
        # print(resultList)
        data_count = len(resultList)# 長度偵測 計算資料庫總筆數
        # print(data_count)
        
        if not resultList:              # 錯誤訊息 查無資料的話
            errormessage="查無此資料"
            status = False
        else:
            errormessage=""
            status = True
        # return HttpResponse("進入菜單")
        return render(request, "menu.html", locals())


# 加入會員
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate
from django.contrib import auth
from django.http import HttpResponse
from django.contrib.auth.models import User
from myapp.models import personal_information,Member        # ORM 抓取 SQL 資料庫 personal_information(會員) 資料表
from django.views.decorators.csrf import csrf_exempt    # 允許這個方法沒有安全機制
@csrf_exempt
def adduser_1(request):
    if request.method =="POST":
        username = request.POST["username"]           # 抓取資料
        password = request.POST["password"]
        repassword = request.POST["repassword"]
        gender = request.POST["gender"]
        phone = request.POST["phone"]
        email = request.POST["email"]
        birthday = request.POST["birthday"]
        address = request.POST["address"]
        print("{}:{}:{}:{}:{}:{}:{}:{}".format(username, password, repassword, gender, phone, email, birthday, address))
        
        try:        # 帳號是否重複
            user = User.objects.get(username=username)
        except:
            user = None
        if user!=None:
            print("帳號已建立")
            message = user.username + "帳號已建立!"
        else:   # 建立帳號
            if password != repassword:
                message = user.username +"密碼不一致"
            else:
                print("可註冊")
                # print(username)
                # print(email)
                # print(password)
                user = User.objects.create_user(username,email,password)
                add = Member(username=username, password=password, balance=0, gender=gender, phone=phone, email=email, birthday=birthday, address=address)
                add.save()
                # user.is_staff =True
                user.tel = email
                user.cBirthday = birthday
                user.save()
                # useradd_sucess_status = True
                return redirect('/front_page_1/')                   
    else:
        return render(request,"adduser_1.html",locals())


# 會員登入
def login(request):
	if request.method == 'POST':
		name = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=name, password=password)
		if user is not None:
			if user.is_active:
				auth.login(request,user)
				return redirect('/home/')
				message = '登入成功！'
			else:
				message = '帳號尚未啟用！'
		else:
			message = '登入失敗！'
	return render(request, "login.html", locals())


# 會員登入顯示
def index(request):
    if request.user.is_authenticated:
        name=request.user.username
    return render(request, "home.html", locals())


# 會員登出
def logout(request):
	auth.logout(request)
	return redirect('/front_page_1/')	


# 會員修改
from myapp.models import Member
from django.views.decorators.csrf import csrf_exempt    # 允許這個方法沒有安全機制
@csrf_exempt
def update_user(request, id):
    # 根據會員ID獲取會員資料
    member = Member.objects.get(id=id)

    if request.method == "POST":
        # 處理表單提交
        member.username = request.POST.get('username')
        member.password = request.POST.get('password')
        member.gender = request.POST.get('gender')
        member.phone = request.POST.get('phone')
        member.email = request.POST.get('email')
        member.birthday = request.POST.get('birthday')
        member.address = request.POST.get('address')
        member.save()
        return redirect('/home/')  # 回會員登入後的首頁

    return render(request, 'update_user.html', {'member': member})

# 已登入 首頁檢視
def home(request):
    return render(request,"home.html",locals())


# 已登入 檢視店家
from django.db import connections
from myapp.models import Store        # ORM 抓取 SQL 資料庫 yellow_pages 資料表
from django.views.decorators.csrf import csrf_exempt    # 允許這個方法沒有安全機制
@csrf_exempt
def home_front_page(request):
    resultList = Store.objects.all().order_by("id")   # 顯示所有資料
    if not resultList:              # 錯誤訊息 查無資料的話
        errormessage="查無此資料"
        status = False
    else:
        errormessage=""
        status = True
    # return HttpResponse("這是測試頁")
    return render(request,"home_front_page.html",locals())


# 已登入 送出菜單
from myapp.models import yellow_pages, menu_all  # 抓資料庫 店家資訊 和 菜單資訊
from django.views.decorators.csrf import csrf_exempt    # 允許這個方法沒有安全機制
@csrf_exempt
def home_menu(request, id=None):
    if request.method == "POST":
        print(id)
        # user_data = request.POST.get('user_data')  # 從 POST 請求中取得使用者提交的資料
        # # 在這裡進行處理，比如存入資料庫、進行其他操作等
        # # 這邊先做一個簡單的回應
        # return HttpResponse(f"已收到資料: {user_data}")
        # return render(request, "checkout.html", locals())
    else:
        # sql = "select * from myapp_menu_all where (cSort_project = '中式' && cStore_Name = '無名早午餐')"       # 抓取資料庫中的 中式早餐
        if(id==2):
            sql = "select * from myapp_menu_all where (cSort_project = '中式' && cStore_Name = '無名早午餐')"
        elif(id==3):
            sql = "select * from myapp_menu_all where (cSort_project = '中式' && cStore_Name = '永和傳統豆漿')"
        elif(id==4):
            sql = "select * from myapp_menu_all where (cSort_project = '西式' && cStore_Name = '斜坡粉漿蛋餅')"
        elif(id==5):
            sql = "select * from myapp_menu_all where (cSort_project = '西式' && cStore_Name = '老八早點鋪')"
        elif(id==6):
            sql = "select * from myapp_menu_all where (cSort_project = '西式' && cStore_Name = '天天有氧')"
        elif(id==1):
            sql = "select * from myapp_menu_all where (cSort_project = '特色' && cStore_Name = '黃媽媽早點客家菜包')"
        
        cursor = connections["default"].cursor()# 連接資料庫
        cursor.execute(sql,[])# 執行 sql 語法
        result = cursor.fetchall()# 取得資料
        # print(result)
        # 取得欄位名稱
        field_name = cursor.description
        # print(field_name)
        cursor.close()# 關閉 資料庫

        resultList =[]# 轉換格式
        for data in result:
            # print(data)
            i = 0
            dict_data = {}
            for d in data:
                # print(d)
                dict_data[field_name[i][0]] = d
                # dict_data["id"] = 1               # 顯示方式
                # dict_data["cName"] = "簡奉君"
                i += 1
            # print(dict_data)
            resultList.append(dict_data)
        # print(resultList)
        data_count = len(resultList)# 長度偵測 計算資料庫總筆數
        # print(data_count)
        
        if not resultList:              # 錯誤訊息 查無資料的話
            errormessage="查無此資料"
            status = False
        else:
            errormessage=""
            status = True
        # return HttpResponse("進入菜單")
        return render(request, "home_menu.html", locals())


# 未登入 檢視美食地圖卡片
def food_map_no(request):
    resultList = Store.objects.all().order_by("id")   # 顯示所有資料
    if not resultList:              # 錯誤訊息 查無資料的話
        errormessage="查無此資料"
        status = False
    else:
        errormessage=""
        status = True
    # return HttpResponse("這是測試頁")
    return render(request,"food_map_no.html",locals())


# 已登入 檢視美食地圖卡片
def food_map(request):
    resultList = Store.objects.all().order_by("id")   # 顯示所有資料
    if not resultList:              # 錯誤訊息 查無資料的話
        errormessage="查無此資料"
        status = False
    else:
        errormessage=""
        status = True
    # return HttpResponse("這是測試頁")
    return render(request,"food_map.html",locals())



#####################################################################################################################################





#####################################################################################################################################
# chat.openai.com 回答 購物車

from django.shortcuts import render, redirect
from myapp.models import CartItem, MenuItem

# 添加商品到购物车
def add_to_cart(request, product_id):
    product = MenuItem.objects.get(pk=product_id)
    user = request.user

    try:
        cart_item = CartItem.objects.get(product=product, user=user)
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        CartItem.objects.create(product=product, quantity=1, user=user)

    return redirect('view_cart')

# 查看购物车
def view_cart(request):
    user = request.user
    cart_items = CartItem.objects.filter(user=user)

    total = sum(item.subtotal() for item in cart_items)

    return render(request, 'view_cart.html', {'cart_items': cart_items, 'total': total})

# 更新购物车
def update_cart(request, item_id):
    item = CartItem.objects.get(pk=item_id)

    if request.method == 'POST':
        new_quantity = int(request.POST['quantity'])
        if new_quantity > 0:
            item.quantity = new_quantity
            item.save()
        else:
            item.delete()

    return redirect('view_cart')

# 从购物车中删除商品
def remove_from_cart(request, item_id):
    item = CartItem.objects.get(pk=item_id)
    item.delete()
    return redirect('view_cart')
#####################################################################################################################################





#####################################################################################################################################
# 書本 購物頁面
from django.shortcuts import render, redirect, get_object_or_404
from myapp import models
from smtplib import SMTP, SMTPAuthenticationError, SMTPException
from email.mime.text import MIMEText

# 宣告資料
message = ''            # 錯誤訊息顯示
cartlist = []           # 購買商品串列
customname = ''         # 購買者姓名
customphone = ''        # 購買者電話
customaddress = ''      # 購買者地址
customemail = ''        # 購買者電子郵件

# 書本 店家頁面OK
from myapp.models import MenuItem, Store
def check_index(request):
	global cartlist
	if 'cartlist' in request.session:                   # 若session中存在cartlist就讀出
		cartlist = request.session['cartlist']
	else:                                               # 重新購物
		cartlist = []                                   # 購買商品串列
	cartnum = len(cartlist)                             # 購買商品筆數
	productall = models.Store.objects.all()             # 取得資料庫所有商品
    # print(productall)
	return render(request, "check_index.html", locals())

    # store = get_object_or_404(Store, pk=store_id)
    # productall = MenuItem.objects.filter(store=store)
    # return render(request, "check_index.html", {'menu_item': store, 'store': productall})

# 書本 店家菜單頁面OK
def check_index_menu(request,store_id):
	global cartlist
	if 'cartlist' in request.session:                   # 若session中存在cartlist就讀出
		cartlist = request.session['cartlist']
	else:                                               # 重新購物
		cartlist = []                                   # 購買商品串列
	cartnum = len(cartlist)                             # 購買商品筆數
	productall = models.MenuItem.objects.filter(store=store_id)             # 取得資料庫所有商品
    # print(productall)
	return render(request, "check_index_menu.html", locals())


# 店家詳細頁面
def check_detail(request, productid=None):
	product = models.MenuItem.objects.get(id=productid)  # 取得店家資料
	return render(request, "check_detail.html", locals())


# 顯示購物車
def check_cart(request):
    global cartlist                 # 全域變數
    cartlist1 = cartlist            # 以區域變數傳給模版
    total = 0                       # 總金額
    for unit in cartlist:           # 計算商品總金額
        total += int(unit[3])
        grandtotal = total + 100    # 加入運費總額
        return render(request, "check_cart.html", locals())


def check_addtocart(request, ctype=None, store_id=None):
	global cartlist
	if ctype == 'add':  #加入購物車
		product = models.MenuItem.objects.get(store=store_id)
		flag = True  #設檢查旗標為True
		for unit in cartlist:  #逐筆檢查商品是否已存在
			if product.name == unit[0]:  #商品已存在
				unit[2] = str(int(unit[2])+ 1)  #數量加1
				unit[3] = str(int(unit[3]) + product.price)  #計算價錢
				flag = False  #設檢查旗標為False
				break
		if flag:  #商品不存在
			temlist = []  #暫時串列
			temlist.append(product.name)  #將商品資料加入暫時串列
			temlist.append(str(product.price))  #商品價格
			temlist.append('1')  #先暫訂數量為1
			temlist.append(str(product.price))  #總價
			cartlist.append(temlist)  #將暫時串列加入購物車
		request.session['cartlist'] = cartlist  #購物車寫入session
		return redirect('/check_cart/')
	elif ctype == 'update':  #更新購物車
		n = 0
		for unit in cartlist:
			unit[2] = request.POST.get('qty' + str(n), '1')  #取得數量
			unit[3] = str(int(unit[1]) * int(unit[2]))  #取得總價
			n += 1
		request.session['cartlist'] = cartlist
		return redirect('/check_cart/')
	elif ctype == 'empty':  #清空購物車
		cartlist = []  #設購物車為空串列
		request.session['cartlist'] = cartlist
		return redirect('/check_index/')
	elif ctype == 'remove':  #刪除購物車中商品
		del cartlist[int(productid)]  #從購物車串列中移除商品
		request.session['cartlist'] = cartlist
		return redirect('/check_cart/')


def check_cartorder(request):  #按我要結帳鈕
	global cartlist, message, customname, customphone, customaddress, customemail
	cartlist1 = cartlist
	total = 0
	for unit in cartlist:  #計算商品總金額
		total += int(unit[3])
	grandtotal = total + 100
	customname1 = customname  ##以區域變數傳給模版
	customphone1 = customphone
	customaddress1 = customaddress
	customemail1 = customemail
	message1 = message
	return render(request, "check_cartorder.html", locals())


def check_cartok(request):  #按確認購買鈕
	global cartlist, message, customname, customphone, customaddress, customemail
	total = 0
	for unit in cartlist:
		total += int(unit[3])
	grandtotal = total + 100
	message = ''
	customname = request.POST.get('CustomerName', '')
	customphone = request.POST.get('CustomerPhone', '')
	customaddress = request.POST.get('CustomerAddress', '')
	customemail = request.POST.get('CustomerEmail', '')
	paytype = request.POST.get('paytype', '')
	customname1 = customname
	if customname=='' or customphone=='' or customaddress=='' or customemail=='':
		message = '姓名、電話、住址及電子郵件皆需輸入'
		return redirect('/check_cartorder/')
	else:
		unitorder = models.OrdersModel.objects.create(subtotal=total, shipping=100, grandtotal=grandtotal, customname=customname, customphone=customphone, customaddress=customaddress, customemail=customemail, paytype=paytype) #建立訂單
		for unit in cartlist:  #將購買商品寫入資料庫
			total = int(unit[1]) * int(unit[2])
			unitdetail = models.DetailModel.objects.create(dorder=unitorder, pname=unit[0], unitprice=unit[1], quantity=unit[2], dtotal=total)
		orderid = unitorder.id  #取得訂單id
		mailfrom="你的gmail帳號"  #帳號
		mailpw="你的gmail密碼"  #密碼
		mailto=customemail  #收件者
		mailsubject="織夢數位購物網-訂單通知";  #郵件標題
		mailcontent = "感謝您的光臨，您已經成功的完成訂購程序。\n我們將儘快把您選購的商品郵寄給您！ 再次感謝您支持\n您的訂單編號為：" + str(orderid) + "，您可以使用這個編號回到網站中查詢訂單的詳細內容。\n織夢數位購物網" #郵件內容
		# send_simple_message(mailfrom, mailpw, mailto, mailsubject, mailcontent)  #寄信
		cartlist = []
		request.session['cartlist'] = cartlist
		return render(request, "check_cartok.html", locals())


def check_cartordercheck(request):  #查詢訂單
	orderid = request.GET.get('orderid', '')  #取得輸入id
	customemail = request.GET.get('customemail', '')  #取得輸email
	if orderid == '' and customemail == '':  #按查詢訂單鈕
		firstsearch = 1
	else:
		order = models.OrdersModel.objects.filter(id=orderid).first()
		if order == None or order.customemail != customemail:  #查不到資料
			notfound = 1
		else:  #找到符合的資料
			details = models.DetailModel.objects.filter(dorder=order)
	return render(request, "check_cartordercheck.html", locals())















#####################################################################################################################################
# # 抓取 sql 資料(店家資料)，並顯示
# from django.db import connections
# def list(request):
#     if 'cStore_Name' in request.GET:
#         cStore_Name = request.GET["cStore_Name"]
#         # print(cName)
#         # print("有輸入 /?cName=XXX 顯示此頁，恭喜成功進入")
#         # sql = "select * from myapp_yellow_pages where cName = '%s'"                      # 差別在這
#         sql = "select * from myapp_yellow_pages where cName like %s"
#         # print(sql)
#         cName = "%%"+ cStore_Name +"%%"
#         val = [cStore_Name]                                                               # (新增) 有輸入資料則顯示
#     else:
#         sql = "select * from myapp_yellow_pages"
#         # print("沒輸入 /?cName=XXX 顯示此頁，請輸入完整")
#         val = []                                                                    # (新增) 沒輸入資料給空的[]
    
#     # 不管是否輸入，皆要執行 sql 語法
#     cursor = connections["default"].cursor()
#     cursor.execute(sql,val)                                                          # 原始寫法結束

#     result = cursor.fetchall()                                                      # 取得資料  固定寫法
#     # print(result)
    
#     # 取得欄位名稱
#     field_name = cursor.description
#     # print(field_name)
#     cursor.close()                                                                  # 關閉 資料庫

#     # 轉換格式 2層 固定寫法
#     resultList =[]
#     for data in result:
#         # print(data)
#         i = 0
#         dict_data = {}
#         for d in data:
#             # print(d)
#             dict_data[field_name[i][0]] = d
#             i += 1
#         # print(dict_data)
#         resultList.append(dict_data)
#     print(resultList)
#     if not resultList:              # 錯誤訊息 查無資料的話
#         errormessage="查無此資料"
#     else:
#         errormessage=""
#     print(errormessage)

#     return render(request,"list.html",locals())
#     # return HttpResponse("這是測試頁")



# # 抓取 sql 資料(菜單資料)，並顯示
# from django.db import connections
# def list_menu(request):
#     if 'cStore_Name' in request.GET:
#         cStore_Name = request.GET["cStore_Name"]
#         sql = "select * from myapp_menu_all where cName like %s"
#         cName = "%%"+ cStore_Name +"%%"
#         val = [cStore_Name]                                                               # (新增) 有輸入資料則顯示
#     else:
#         sql = "select * from myapp_menu_all"
#         val = []                                                                    # (新增) 沒輸入資料給空的[]
    
#     # 不管是否輸入，皆要執行 sql 語法
#     cursor = connections["default"].cursor()
#     cursor.execute(sql,val)
#     result = cursor.fetchall()                                                      # 取得資料  固定寫法
#     # 取得欄位名稱
#     field_name = cursor.description
#     cursor.close()                                                                  # 關閉 資料庫

#     # 轉換格式 2層 固定寫法
#     resultList =[]
#     for data in result:
#         i = 0
#         dict_data = {}
#         for d in data:
#             dict_data[field_name[i][0]] = d
#             i += 1
#         resultList.append(dict_data)
#     print(resultList)
#     if not resultList:              # 錯誤訊息 查無資料的話
#         errormessage="查無此資料"
#     else:
#         errormessage=""
#     print(errormessage)
#     return render(request,"list_menu.html",locals())



# # 抓取 sql 資料(菜單資料)，並顯示
# from django.db import connections
# def list_information(request):
#     if 'cName' in request.GET:
#         cName = request.GET["cName"]
#         sql = "select * from myapp_personal_information where cName like %s"
#         cName = "%%"+ cName +"%%"
#         val = [cName]                                                               # (新增) 有輸入資料則顯示
#     else:
#         sql = "select * from myapp_personal_information"
#         val = []                                                                    # (新增) 沒輸入資料給空的[]
    
#     # 不管是否輸入，皆要執行 sql 語法
#     cursor = connections["default"].cursor()
#     cursor.execute(sql,val)
#     result = cursor.fetchall()                                                      # 取得資料  固定寫法
#     # 取得欄位名稱
#     field_name = cursor.description
#     cursor.close()                                                                  # 關閉 資料庫

#     # 轉換格式 2層 固定寫法
#     resultList =[]
#     for data in result:
#         i = 0
#         dict_data = {}
#         for d in data:
#             dict_data[field_name[i][0]] = d
#             i += 1
#         resultList.append(dict_data)
#     print(resultList)
#     if not resultList:              # 錯誤訊息 查無資料的話
#         errormessage="查無此資料"
#     else:
#         errormessage=""
#     print(errormessage)

#     return render(request,"list_information.html",locals())











# # 結帳
# def checkout(request, id=None):

#     return render(request,"checkout.html",locals())



# # 會員資料
# def member_material(request):

#     return render(request, "member_material.html",locals())


# # 好事多代購系統
# def costco_purchasing_agent(request):

#     return render(request, "costco_purchasing_agent.html",locals())



        
        
        
#         try:        # 帳號是否重複
#             user = User.objects.get(username=username)
#         except:
#             user = None
#         if user!=None:
#             print("帳號已建立")
#             message = user.username + "帳號已建立!"
#             return render(request, "login.html",locals())
#         else:   # 建立帳號
#             if password != repassword:
#                 message = user.username +"密碼不一致"
#                 return render(request, "adduser.html",locals())
#             else:
#                 print("可註冊")
#                 print(username)
#                 print(email)
#                 print(password)
#                 user = User.objects.create_user("testxx","testx@xx.com.tw","123456")
#                 user.is_staff =True
#                 user.tel = email
#                 user.cBirthday = birthday
#                 user.save()
#                 # useradd_sucess_status = True
#                 return render(request,"login.html",locals())                      
#     else:
#         return render(request,"adduser.html",locals())




# 
# def adduser(request):	
# 	try:
# 		user=User.objects.get(username="test")
# 	except:
# 		user=None
# 	if user!=None:
# 		message = user.username + " 帳號已建立!"
# 		return HttpResponse(message)
# 	else:	# 建立 test 帳號			
# 		user=User.objects.create_user("test","test@test.com.tw","a123456!")
# 		user.first_name="wen" # 姓名
# 		user.last_name="lin"  # 姓氏
# 		user.is_staff=True	# 工作人員狀態
# 		user.save()
# 		return redirect('/admin/')

