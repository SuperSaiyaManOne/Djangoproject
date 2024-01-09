from django.db import models

class personal_information(models.Model):                                            # personal_information(個人資料) 資料表名稱
  cAcc = models.CharField(max_length=20, blank=True, null=False)                     # 帳號 CharField文字 長度20 不能不填寫
  cPwd = models.CharField(max_length=20, blank=True, null=False)                     # 密碼 CharField文字 長度20 不能不填寫
  cName = models.CharField(max_length=20, null=False)                                # 姓名 CharField文字 長度20 不能不填寫
  cSex = models.CharField(max_length=2, default='M', null=False)                     # 性別 CharField文字 長度2 預設M 不能不填寫
  cBirthday = models.DateField(null=False)                                           # 生日 DateField日期 不能不填寫
  cEmail = models.EmailField(max_length=100, blank=True, default='', null=False)     # email EmailField信箱 長度100 可以空白 預設空白 不能不填寫
  cPhone = models.CharField(max_length=50, blank=True, default='')                   # 電話 CharField文字 長度50 可以空白 預設空白
  cAddr = models.CharField(max_length=255,blank=True, default='')                    # 地址 CharField文字 長度255 可以空白 預設空白

class yellow_pages(models.Model):                                                    # yellow_pages(店家資料) 資料表名稱
  cStore_Name = models.CharField(max_length=30, null=False)                          # 店名 CharField文字 長度30 不能不填寫
  cStore_Phone = models.CharField(max_length=50, null=False)                         # 電話 CharField文字 長度50 不能不填寫
  cStore_Addr = models.CharField(max_length=255,blank=True, default='')              # 地址 CharField文字 長度255 可以空白 預設空白
  cBusiness_Hours = models.CharField(max_length=100, blank=True, default='')         # 營業時間 CharField文字 長度100 可以空白 預設空白
  cSort_project = models.CharField(max_length=30, blank=True, default='')            # 類別 CharField文字 長度30 可以空白 預設空白

class menu_all(models.Model):                                                        # menu_all(菜單_全) 資料表名稱
  cStore_Name = models.CharField(max_length=30, null=False)                          # 店名 CharField文字 長度30 不能不填寫
  cProduct_name = models.CharField(max_length=100, null=False)                       # 品名 CharField文字 長度100 不能不填寫
  cUnit_price = models.CharField(max_length=20, null=False)                          # 單價 CharField文字 長度20 不能不填寫
  cSort_project = models.CharField(max_length=30, blank=True, default='')            # 類別 CharField文字 長度30 可以空白 預設空白






from django.db import models
from django import forms

# 會員資料
class Member(models.Model):
    GENDER_CHOICES = [                                                                # 性別，使用 GENDER_CHOICES 定義了性别選項
        ('M', '男性'),
        ('F', '女性'),
        ('O', '其他'),
    ]
    
    username = models.CharField(max_length=50)                                        # 姓名，CharField 文字
    email = models.EmailField()                                                       # 信箱
    password = models.CharField(max_length=100)                                       # 密碼
    balance = models.DecimalField(max_digits=10, decimal_places=2)                    # 餘額
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)                   # 性別，對應上面的語法
    phone = models.CharField(max_length=15)  # 可根据需求设置最大长度                   # 電話
    address = models.TextField()                                                      # 地址，使用 TextField 保存較長文字
    birthday = models.DateField()                                                     # 生日，DateField 日期

    def __str__(self):                                                                # 會員資料使用外部關聯
        return self.username

# 創建表單與會員資料關聯 名稱需與關連名稱相同
class MemberRegistrationForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['username', 'email', 'password', 'balance', 'gender', 'phone', 'address', 'birthday']



# 店家資料
class Store(models.Model):
    CATEGORY_CHOICES = [                                                              # 類別，使用 CATEGORY_CHOICES 定義了類別選項
        ('Chinese_Food', '中式'),
        ('Western_Food', '西式'),
        ('Feature', '特色'),
        # 可根据需求扩展更多类别选项
    ]

    name = models.CharField(max_length=100)                                           # 店名
    address = models.CharField(max_length=200)                                        # 地址
    contact = models.CharField(max_length=25)                                         # 營業時間
    phone = models.CharField(max_length=15)  # 可根据需求设置最大长度                   # 電話
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)              # 類別，對應上面的語法

    def __str__(self):                                                                # 會員資料使用外部關聯
        return self.name
    
# 菜單資料
class MenuItem(models.Model):
    name = models.CharField(max_length=100)                                           # 品名
    description = models.TextField()                                                  # 描述
    price = models.DecimalField(max_digits=10, decimal_places=2)                      # 價格
    num = models.IntegerField(default=0)                                              # 数量字段并设置默认值为0
    store = models.ForeignKey(Store, on_delete=models.CASCADE)                        # 菜單與店家關聯

    def __str__(self):                                                                # 會員資料使用外部關聯
        return self.name





# 書本11章資料
from django.db import models                                                          # 書本11章

class ProductModel(models.Model):                                                     # 商品內容
    pname =  models.CharField(max_length=100, default='')                             # 商品名稱
    pprice = models.IntegerField(default=0)                                           # 單價
    pimages = models.CharField(max_length=100, default='')                            # 照片
    pdescription = models.TextField(blank=True, default='')                           # 說明
    def __str__(self):                                                                # 商品資料使用外部關聯
        return self.pname
        
class OrdersModel(models.Model):                                                      # 訂單資料
    subtotal = models.IntegerField(default=0)                                         # 購物金額(未含運費)
    shipping = models.IntegerField(default=0)                                         # 運費
    grandtotal = models.IntegerField(default=0)                                       # 購物金額(含運費)
    customname =  models.CharField(max_length=100, default='')                        # 購買者姓名
    customemail =  models.CharField(max_length=100, default='')                       # 購買者信箱
    customaddress =  models.CharField(max_length=100, default='')                     # 購買者地址
    customphone =  models.CharField(max_length=100, default='')                       # 購買者電話
    paytype =  models.CharField(max_length=50, default='')                            # 購買者付款方式
    def __str__(self):                                                                # 訂單資料使用外部關聯
        return self.customname
     
class DetailModel(models.Model):                                                      # 詳細訂單內容
    dorder = models.ForeignKey('OrdersModel', on_delete=models.CASCADE)               # 儲存訂單 (關聯欄位) on_delete 移除整筆訂單
    pname = models.CharField(max_length=100, default='')                              # 商品名稱
    unitprice = models.IntegerField(default=0)                                        # 單價
    quantity = models.IntegerField(default=0)                                         # 數量
    dtotal = models.IntegerField(default=0)                                           # 總價
    def __str__(self):                                                                # 詳細訂單內容資料使用外部關聯
        return self.pname
    
    
    
    
    
    
    
    
# chat.openai.com 回答

from django.db import models
from django.contrib.auth.models import User
from myapp.models import MenuItem

# 跟蹤購物車商品
class CartItem(models.Model):
    product = models.ForeignKey(MenuItem, on_delete=models.CASCADE)             # 資料使用外部關聯 MenuItem
    quantity = models.PositiveIntegerField(default=1)                           # 商品數量
    user = models.ForeignKey(User, on_delete=models.CASCADE)                    # 與購物車的所有者相關聯
    def subtotal(self):                                                         # 計算每個購物車項目的小計
        return self.product.price * self.quantity
