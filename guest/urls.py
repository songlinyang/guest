"""guest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from sign import views
urlpatterns = [
    url(r'^admin/', admin.site.urls),           #admin管理页
    url(r'^index/$',views.index),               #登录页
    url(r'^login_action/$',views.login_action), #登录页跳转
    url(r'^event_manage/$',views.event_manage), #发布会列表
    url(r'^accounts/login/$',views.index),      #登录页
    url(r'^$',views.index),                     #登录页
    url(r'^search_name/$',views.search_name),   #发布会搜索页面
    url(r'^guest_manage/$',views.guest_manage), #嘉宾列表
    url(r'^search_name_1/$',views.search_name_1),#嘉宾搜索页面
    url(r'^sign_index/(?P<eid>[0-9]+)/$',views.sign_index), #签到页面
    url(r'^sign_index_action/(?P<eid>[0-9]+)/$',views.sign_index_action),
    url(r'^logout/$',views.logout),
    #添加接口根路劲
    url(r'^api/',include('sign.urls',namespace="sign")),
]
