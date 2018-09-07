#encoding=utf-8
from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from pymysql import cursors,connect
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
# Create your views here.
def index(request):
	return render(request,"index.html")

# 登陆动作
def login_action(request):
	if request.method == 'POST':
		username = request.POST.get('username','')
		password = request.POST.get('password','')
		#if username == 'admin' and password == 'admin123':
			#response = HttpResponseRedirect('/event_manage/')
			#使用cookies存放用户登录信息
			#response.set_cookie('user',username,3600)
			#request.session['user'] = username
			#return response
		#else:
			#return render(request,'index.html',{'error':'username or password error!'})
		user = auth.authenticate(username=username,password=password)
		if user is not None:
			auth.login(request,user) #登录
			request.session['user'] = username
			response = HttpResponseRedirect('/event_manage/')
			return response
		else:
			return render(request,'index.html',{"error":'username or password error!'})

#连接数据库
con = connect(
	host='47.104.74.144',
	user='root',
	password='yang@123',
	db='guest',
	charset='utf8',
	cursorclass=cursors.DictCursor
	)


# 发布会管理
@login_required
def event_manage(request):
	#username = request.COOKIES.get('user','') #读取浏览器cookie
	username = request.session.get('user','') #读取浏览器session
	#获取Event对象
	#event_list = Event.objects.all()
	#使用Mysql语句
	event_list = []
	try:
		with con.cursor() as cursor:
			sql="SELECT id,name,status,address,start_time FROM sign_event;"
			cursor.execute(sql)
			event_list = cursor.fetchall()
	except Exception as e:
		print(e)
		return
	finally:
		pass
	#创建每页5条数据的分页器
	paginator = Paginator(event_list,5)
	#通过GET请求获取当前要显示的第几页
	page = request.GET.get('page','')
	try:
		contacts = paginator.page(page)
	except PageNotAnInteger:
		contacts = paginator.page(1)
	except EmptyPage:
		contacts = paginator.page(paginator.num_pages)

	#warning 需要关闭数据库
	return render(request,"event_manage.html",{"user":username,"events":contacts})

#搜索框	
@login_required
def search_name(request):
	username = request.session.get('user','')
	search_name = request.GET.get("name","")
	search_list = search(search_name)
	return render(request,"event_manage.html",{"user":username,"events":search_list})
	


#发布会列表页面模糊搜索功能	
def search(search_name):
	#生成游标
	search_result = []
	if search_result:
		try:
			with con.cursor() as cursor:
				sql = "SELECT id,name,status,address,start_time FROM sign_event WHERE name like %s;"
				cursor.execute(sql,'%%%%'+search_name+'%%%%')
				search_result = cursor.fetchall()
			
		finally:
			#warning 需要关闭数据库
			return search_result
	else:
		return search_result


#嘉宾列表
@login_required
def guest_manage(request):
	username = request.session.get('user','')
	guest_list = get_guest_list()
	#创建每页5条数据的分页器
	paginator = Paginator(guest_list,5)
	page = request.GET.get('page','')
	try:
		contacts = paginator.page(page)
	except PageNotAnInteger:
		#如果page不是整数，取第一页面数据
		contacts = paginator.page(1)
	except EmptyPage:
		#如果page不在范围，取最后一页面
		contacts = paginator.page(paginator.num_pages)
	return render(request,"guest_manage.html",{"user":username,"guests":contacts})

#获取所有的嘉宾
def get_guest_list(conn=con):

	guest_list = []
	#生成游标
	try:
		with conn.cursor() as cursor:
			sql = "SELECT guest.id,guest.realname,guest.phone,guest.email,guest.sign,event.name FROM sign_guest guest LEFT JOIN sign_event event ON guest.event_id=event.id;"
			cursor.execute(sql)
			guest_list = cursor.fetchall()
	finally:
		#warning 需要关闭数据库
		return guest_list

#嘉宾列表搜索框	
@login_required
def search_name_1(request):
	username = request.session.get('user','')
	search_name = request.GET.get("name","")
	guest_list = search_for_guest(search_name)
	return render(request,"guest_manage.html",{"user":username,"guests":guest_list})
	
#嘉宾列表模糊搜索功能
def search_for_guest(search_name):
	
	search_result = []
	if search_name:
		try:
			#生成游标
			with con.cursor() as cursor:
				sql = "SELECT guest.id,guest.realname,guest.phone,guest.email,guest.sign,event.name FROM sign_guest guest LEFT JOIN sign_event event ON guest.event_id=event.id WHERE realname like %s;"
				cursor.execute(sql,'%%%%'+search_name+'%%%%')
				search_result = cursor.fetchall()
		finally:
			#warning 需要关闭数据库
			return search_result
	else:
		return search_result

#签到页面
@login_required
def sign_index(request,eid):
	try:
		with con.cursor() as cursor:
			sql = "SELECT id,name,status,address,start_time FROM sign_event WHERE id=%s;"
			cursor.execute(sql,(eid,))
			event = cursor.fetchone()
	except:
		return render(request,'404.html')
	return render(request,'sign_index.html',{'event':event})

#签到Action
@login_required
def sign_index_action(request,eid):
	sign_phone = request.POST.get('phone','')
	try:
		#创建游标，获取Event数据
		with con.cursor() as cursor:
			sql = "SELECT id,name,status,address,start_time FROM sign_event WHERE id=%s;"
			cursor.execute(sql,(eid,))
			event = cursor.fetchone()
	except:
		return render(request,'404.html')
	try:
		#创建游标，获取Guest数据
		with con.cursor() as cursor:
			sql = "SELECT id,realname,phone,email,sign FROM sign_guest WHERE phone=%s;"
			cursor.execute(sql,(sign_phone,))
			result_sign_phone = cursor.fetchone()
	except Exception as e:
		print (e)
		return render(request,'404.html')
	try:
		#创建游标，获取Guest，Event数据
		with con.cursor() as cursor:
			sql = "SELECT guest.id,guest.realname,guest.phone,guest.email,guest.sign,event.name FROM sign_guest guest JOIN sign_event event ON guest.event_id=event.id WHERE guest.phone=%s and event.id=%s;"
			cursor.execute(sql,(sign_phone,eid,))
			result_sign_phone_event = cursor.fetchone()
	except Exception as e:
		print (e)
		return render(request,'404.html')

	if not result_sign_phone:
		return render(request,'sign_index.html',{'event':event,'hint':'手机号错误，签到失败！'})
	if not result_sign_phone_event:
		return render(request,'sign_index.html',{'event':event,'hint':'手机号或发布会不存在，签到失败！'})
	if result_sign_phone_event['sign']:
		return render(request,'sign_index.html',{'event':event,'hint':"该用户已签到成功！"})
	else:
		#对该用户进行签到，并更新Guest数据
		with con.cursor() as cursor:
			sql = "UPDATE sign_guest guest JOIN sign_event event ON guest.event_id=event.id SET sign=1 where guest.phone=%s;"
			cursor.execute(sql,(sign_phone,))
			con.commit()
		return render(request,'sign_index.html',{'event':event,'hint':"签到成功！",'guest':result_sign_phone_event})


#登出
@login_required
def logout(request):
	auth.logout(request) #退出系统 可以清空缓存的作用
	#重定向
	response = HttpResponseRedirect('/index/') #重定向
	return response