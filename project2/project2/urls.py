from django.contrib import admin
from django.urls import path
from myapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('test1/',views.test1), #此test1只是測試用顯示"hello world"
    #path('', views.test1), #此行打了，就只要輸入到8080，之後不用打"/test"
    path('hello1/<str:username>/', views.hello1), #如果網址打「.../hello1/jason/」就會顯示「Hello jason」
    
    path('list/',views.list), #載入mysql的資料 #2023100303 18:25
    path('search_name/', views.search_name), #查詢裡面的內容
    path('index/', views.index), #初始頁面 #製作使用者可以編輯、刪除的表單
    path('post1/', views.post1), #新增 #按下去新增基本資料的
    path('edit1/<int:id>/<str:mode>/', views.edit1), #修改1 #使用GET #有兩個參數，所以views那邊也要設定兩個參數
    path('edit2/<int:id>/', views.edit2), #修改2 #使用POST
    path('delete/<int:id>/', views.delete), #使用POST
    
    #Web API
    path('getAllItems/', views.getAllItems), #開始使用web api
    path('getItem/<int:id>/', views.getItem),
    path('createItem/', views.createItem),
    path('updateItem/<int:id>/', views.updateItem),
    path('deleteItem/<int:id>/', views.deleteItem),

]
# ------------------------------------
# 定義自訂函式
