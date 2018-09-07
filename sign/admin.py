from django.contrib import admin
from sign.models import Event,Guest
# Register your models here.
#修改后台，显示更多的表
class EventAdmin(admin.ModelAdmin):
	list_display = ['id','name','status','adress','start_time']
class GuestAdmin(admin.ModelAdmin):
	list_display = ['realname','phone','email','sign','create_time','event']
admin.site.register(Event)
admin.site.register(Guest)