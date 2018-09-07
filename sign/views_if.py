from django.http import JsonResponse
from sign.models import Event,Guest
import time
from django.core.exceptions import ValidationError,ObjectDoesNotExist
from django.db.utils import IntegrityError
import traceback
#添加发布会接口
def add_event(request):
    eid = request.POST.get('eid','') #发布会id
    name = request.POST.get('name','') #发布会标题
    limit = request.POST.get('limit','') #限制人数
    status = request.POST.get('status','') #状态
    address = request.POST.get('address','') #地址
    start_time = request.POST.get('start_time','') #发布会时间

    if eid == '' or name == '' or limit == '' or status =='' or address == '' or start_time =='':
        return JsonResponse({'starus':10021,'message':'参数错误'})
    result = Event.objects.filter(id=eid)
    if result:
        return JsonResponse({'starus':10022,'message':'发布会编号已存在'})
    result = Event.objects.filter(name=name)
    if result:
        return JsonResponse({'starus':10023,'message':'发布会名称已存在'})
    if status == '':
        status = 1
    try:
        #写入Event表
        Event.objects.create(id=eid,name=name,limit=limit,address=address,status=int(status),start_time=start_time)
    except ValidationError as e:
        error = str(e)
        return JsonResponse({'starus':10024,'message':error})

    return JsonResponse({'starus':200,'message':'添加时间成功'})

#查询发布会接口
def get_event_list(request):
    eid = request.GET.get("eid","") #发布会id
    name = request.GET.get("name","") #发布会名称

    if eid == '' and name == '':
        return JsonResponse({'status':10021,'message':'参数错误'})

    if eid != '':
        event = {}
        try:
            result = Event.objects.get(id=eid)
        except ObjectDoesNotExist:
            return JsonResponse({'status':10022,'message':'查询结果为空'})
        else:
            event['name'] = result.name
            event['limit'] = result.limit
            event['status'] = result.status
            event['address'] = result.address
            event['start_time'] = result.start_time
            return JsonResponse({'status':200,'message':'success','data':event})
    if name != '':
        datas = []
        results = Event.objects.filter(name__contains=name)
        if results:
            for r in results:
                event = {}
                event['name'] = r.name
                event['limit'] = r.limit
                event['status'] = r.status
                event['address'] = r.address
                event['start_time'] = r.start_time
                datas.append(event)
                return JsonResponse({'status':200,'message':'success','data':datas})
        else:
            return JsonResponse({'status':10022,'message':'查询结果为空'})
#添加嘉宾接口
def add_guest(request):
    try:
        eid = request.POST.get("eid","")
        realname = request.POST.get("realname","")
        phone = request.POST.get("phone","")
        email = request.POST.get("email","")

        if eid == "" or realname == "" or phone == "":
            return JsonResponse({'stauts':10021,'message':'参数错误'})
        event_result = Event.objects.get(id=eid)
        if not event_result:
            return JsonResponse({'status':10022,'message':'发布会不存在，请重新添加'})
        result = Event.objects.get(id=eid).status
        if result == 1:
            return JsonResponse({'status':10023,'message':'发布会已关闭，无法添加嘉宾'})

        event_limit = Event.objects.get(id=eid).limit #发布会限制人数
        guest_limit = Guest.objects.filter(event_id=eid) #发布会已添加的嘉宾数

        if len(guest_limit) >= event_limit:
            return JsonResponse({'status':10024,'message':'发布会人数已超出上限'})
        event_time = Event.objects.get(id=eid).start_time #发布会限制人数
        timeArray = time.strptime(str(event_time),"%Y-%m-%d %H:%M:%S")
        e_time = int(time.mktime(timeArray))

        now_time = str(time.time())
        ntime = now_time.split(".")[0]
        n_time = int(ntime)

        if n_time >= e_time:
            return JsonResponse({'status':10025,'message':'发布会事件已经开始'})
        try:
            Guest.objects.create(realname=realname,phone=int(phone),email=email,sign=0,event_id=int(eid))
        except IntegrityError as error:
            return JsonResponse({'status':500,'message':error})
        return JsonResponse({'status':200,'message':'添加嘉宾成功'})
    except Exception as e:
        print(e,traceback.print_exc())

"""
查询嘉宾接口
"""
def get_guest_list(request):
    #根据发布会eid和嘉宾phone，获取指定嘉宾信息及参加的发布会
    print("fuck=====>",request.GET)
    eid = request.GET.get("eid","")
    phone = request.GET.get("phone","")
    if eid != "":
        try:
            Guest.objects.get(event_id=eid)
        except ValueError:
            return JsonResponse({'status':10021,'message':"参数错误"})

    if eid == "" and phone == "":
        return JsonResponse({'status':10021,'message':"参数错误"})
    #根据phone获取嘉宾
    if eid != "" and phone == "":
        data = []
        results = Guest.objects.filter(event_id=eid)
        if results:
            for guest_result in results:
                guest = {}
                guest["realname"] = guest_result.realname
                guest["phone"] = guest_result.phone
                guest["email"] = guest_result.email
                guest["sign"] = guest_result.sign
                data.append(guest)
            return JsonResponse({'status':200,'message':'success','data':data})
        else:
            return JsonResponse({'status':10022,'message':'查询结果为空'})
    if eid != "" or phone != "":
        guest = {}
        try:
            result = Guest.objects.get(event_id=eid, phone=phone)
        except ObjectDoesNotExist:
            return JsonResponse({'status':10022,'message':'查询结果为空'})
        else:
            guest['realname']=result.realname
            guest['phone']=result.phone
            guest['email']=result.email
            guest['sign']=result.sign
            return JsonResponse({'status':200,'message':'success','data':guest})

#发布会签到接口
def user_sign(request):
    eid = request.POST.get('eid','') #发布会id
    phone = request.POST.get('phone','')

    if eid == '' or phone == '':
        return JsonResponse({'status':10021,'message':'参数错误'})
    result = Event.objects.filter(id=eid)
    if not result:
        return JsonResponse({'status':10022,'message':'发布会不存在'})
    result = Event.objects.get(id=eid).status
    if not result:
        return JsonResponse({'status': 10023, 'message': '发布会状态不可用'})
    event_time = Event.objects.get(id=eid).start_time #发布会时间
    etime = str(event_time).split(".")[0]
    timeArray = time.strptime(etime,"%Y-%m-%d %H:%M:%S")
    print("时间时间：",timeArray)
    e_time = int(time.mktime(timeArray))

    now_time = str(time.time())
    ntime = now_time.split(".")[0]
    n_time = int(ntime)

    if n_time >= e_time:
        return JsonResponse({'status': 10024, 'message': '发布会已经开始，不能进行签到'})
    result = Guest.objects.filter(phone=phone)
    if not result:
        return JsonResponse({'status': 10025, 'message': '用户不存在'})
    result = Guest.objects.filter(event_id=eid,phone=phone)
    if not result:
        return JsonResponse({'status':10026,'message':'用户不在该场次发布会名单内'})
    #sign 为0表示未签到，为1表示已签到成功，用户已入场
    result = Guest.objects.get(event_id=eid,phone=phone).sign
    if result:
        return JsonResponse({'status':10027,'message':'用户已签到成功，已入场'})
    else:
        Guest.objects.filter(event_id=eid,phone=phone).update(sign='1')
        return JsonResponse({'status':200,'message':'用户签到成功'})

