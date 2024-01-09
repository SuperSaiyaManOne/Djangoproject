"""
URL configuration for eat project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from myapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.front_page_1),                                       # 沒輸入也進檢視首頁
    path("front_page_1/",views.front_page_1),                           # 未登入 首頁檢視
    path("front_page/",views.front_page),                               # 未登入 店家檢視
    path('menu/<int:id>/', views.menu),                                 # 未登入 菜單檢視
    
    path("home/",views.home),                                           # 已登入 首頁
    path("home_front_page/",views.home_front_page),                     # 已登入 檢視店家
    path('check_index/', views.check_index),                            # 書本 檢視店家
    path("home_menu/<int:id>/",views.home_menu),                        # 已登入 送出菜單
    path('check_index_menu/<int:store_id>/', views.check_index_menu),   # 書本 檢視店家菜單
    path('updateuser/<int:id>/', views.update_user, name='update_user'),# 已登入 修改會員

    path('food_map_no/', views.food_map_no),                            # 未登入 檢視美食地圖卡片
    path('food_map/', views.food_map),                                  # 已登入 檢視美食地圖卡片
    
    
    path('login/', views.login),                                        # 會員登入
    path('logout/', views.logout),	                                    # 會員登出
    path('adduser_1/', views.adduser_1),                                # 加入會員
    
    
    ###########################################################################################################
    # chat.openai.com 回答 購物車
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('view_cart/', views.view_cart, name='view_cart'),
    path('update_cart/<int:item_id>/', views.update_cart, name='update_cart'),
    path('remove_from_cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),



    ###########################################################################################################
    # 書本 下面還是有問題
    
    
    
    
    path('check_detail/<int:storeid>/', views.check_detail),
    path('check_addtocart/<str:ctype>/', views.check_addtocart),
    path('check_addtocart/<str:ctype>/<int:productid>/', views.check_addtocart),
    path('check_cart/', views.check_cart),
    path('check_cartorder/', views.check_cartorder),
    path('check_cartok/', views.check_cartok),
    path('check_cartordercheck/', views.check_cartordercheck),
    

    

    # path('list/', views.list),                                        # 抓取資料庫(店家資料)
    # path('list_menu/', views.list_menu),                              # 抓取資料庫(各家菜單)
    # path('list_information/', views.list_information),                # 抓取資料庫(基本資料)
    
    # path("costco_purchasing_agent/",views.costco_purchasing_agent),   # 好事多代購系統 未來期許
    

    # # path('menu1/<int:id>/', views.menu1),                           # 訂餐
    

    # path('checkout/', views.checkout),                                # 結帳

    
    
    # # path('join_member/', views.join_member),                    # 加入會員

    
    # path('member_material/', views.member_material),            # 會員資料
	
		
    

    
]
