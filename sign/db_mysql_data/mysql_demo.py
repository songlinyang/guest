# from pymysql import cursors,connect
# import json
# #连接数据库
# conn = connect(
# 	host='47.104.74.144', #数据库地址
# 	user='root',        	#数据库名称
# 	password='yang@123',  	#数据库密码
# 	db='guest',         	#数据库
# 	charset='utf8',
# 	cursorclass=cursors.DictCursor
# 	)
# try:
# 	with conn.cursor() as cursor:
# 		#创建嘉宾数据
# 		sql = 'INSERT INTO sign_guest (realname,phone,email,sign,event_id,create_time) VALUES ("杨松霖","13715384224","376681881@qq.com",0,1,NOW());'
# 		cursor.execute(sql)
# 		#提交事物
# 		conn.commit()
#
# 	with conn.cursor() as cursor:
# 		#sql = "SELECT id,name,status,address,start_time FROM sign_event WHERE name=%s;"
#
# 		#cursor.execute(sql, ('小米5发布会',))
# 		sql = "SELECT guest.id,guest.realname,guest.phone,guest.email,guest.sign,event.name FROM sign_guest guest LEFT JOIN sign_event event ON guest.event_id=event.id;"
# 		cursor.execute(sql)
# 		result = cursor.fetchone()
# 		print(result)
# except:
# 	conn = connect(
# 	host='192.168.247.128', #数据库地址
# 	user='root',        	#数据库名称
# 	password='123456',  	#数据库密码
# 	db='guest',         	#数据库
# 	charset='utf8',
# 	cursorclass=cursors.DictCursor
# 	)
# finally:
# 	conn.close()
#
