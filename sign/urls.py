#二级接口目录
from django.conf.urls import url
from sign import views_if
urlpatterns = [
    #sign system interface:
    #添加事件
    url(r'^add_event/',views_if.add_event,name='add_event'),
    #添加签到
    url(r'^add_guest/', views_if.add_guest, name='add_guest'),
    #获取事件列表get_event_list
    url(r'^get_event_list',views_if.get_event_list,name='get_event_list'),
    #获取嘉宾列表
    url(r'^get_guest_list',views_if.get_guest_list,name='get_guest_list'),
    #用户签到
    url(r'^user_sign/',views_if.user_sign,name='user_sign'),
]