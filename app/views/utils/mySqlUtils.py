# coding=utf-8
import MySQLdb
import sys
reload(sys)
sys.setdefaultencoding('utf8')

class MySQL(object):
	def __init__(self):
		self.host = '127.0.0.1'
		self.user = 'root'
		self.password = '5868629'
		# self.database = 'jssf'
		self.db = None
		self.cursor = None

	def connectDB(self, dbname):
		self.db = MySQLdb.connect(self.host, self.user, self.password, dbname, charset="utf8")
		self.cursor = self.db.cursor()
		return self.cursor

	def get_query(self, table_name,  data = None, no = None, order_key=None):
		query_str = "select * from " + table_name
		if data is not None:
			query_str += " where "
			for k in data.keys():
				query_str += k + data[k]["conn"] + '"' + data[k]["val"] + '"' + " and "
		# if query_key is not None and query_conn is not None and query_val is not None:
		# 	query_str += " where " + query_key + query_conn + '"' + query_val + '"'
			query_str = query_str[:-5]
		if order_key is not None:
			query_str += " order by " + order_key
		# 获取列名
		self.cursor.execute('DESC ' + table_name)
		columns = self.cursor.fetchall()
		# print columns
		columns_list = []
		for c in columns:
			columns_list.append(c[0])
		columns_list.append("id")
		# 获取要查询的数据
		print query_str
		self.cursor.execute(query_str)
		results = self.cursor.fetchall()
		query_result = []
		if no is not None:
			add = 0
			for row in results:
				dic_tmp = {}
				for idx in range(len(row)):
					key = columns_list[idx]
					val = row[idx]
					dic_tmp[key] = val
				query_result.append(dic_tmp)
				add += 1
				if add == no:
					break
		else:
			for row in results:
				print row
				dic_tmp = {}
				for idx in range(len(row)):
					key = columns_list[idx]
					val = row[idx]
					dic_tmp[key] = val
				query_result.append(dic_tmp)
		return query_result

	def insert_data(self, table_name, data = None):
		try:
			insert_name = []
			insert_val = []
			for key in data.keys():
				insert_name.append(key)
				insert_val.append(data[key])
			insert_str = "INSERT INTO " + table_name
			left_str = " ("
			for name in insert_name:
				left_str += (name + ',')
			left_str = left_str[:-1]
			left_str += ') VALUES ('
			for val in insert_val:
				left_str += ('"' + str(val) + '",')
			left_str = left_str[:-1]
			left_str += ')'
			insert_str += left_str
			print insert_str
			try:
				# 执行sql语句
				self.cursor.execute(insert_str)
				# 提交到数据库执行
				self.db.commit()
			except:
				# Rollback in case there is any error
				self.db.rollback()
			return "success"
		except Exception, e:
			print(str(e))
			return "error"

	def update_data(self, table_name, data, kvs):
		try:
			key_name = []
			key_val = []
			for k in kvs.keys():
				key_name.append(k)
				key_val.append(kvs[k])
			update_name = []
			update_val = []
			for key in data.keys():
				update_name.append(key)
				update_val.append(data[key])
			update_str = "UPDATE " + table_name +" SET "
			left_str = ""
			for idx in range(len(update_name)):
				left_str += (update_name[idx] + '="' + update_val[idx] + '",')
			left_str = left_str[:-1]
			if len(key_name) > 0:
				left_str += " WHERE "
				for k in key_name:
					left_str += k + '="' + kvs[k] + '" and '
				left_str = left_str[:-5]
			update_str += left_str
			print update_str
			try:
				# 执行sql语句
				self.cursor.execute(update_str)
				# 提交到数据库执行
				self.db.commit()
			except:
				# Rollback in case there is any error
				self.db.rollback()
			return "success"
		except Exception, e:
			print(str(e))
			return "error"

	def delete_data(self, table_name, kvs):
		try:
			delete_str = "DELETE FROM " + table_name
			if len(kvs) > 0:
				delete_str += " WHERE "
				for k in kvs.keys():
					delete_str += k + '="' + kvs[k] + '" and '
				delete_str = delete_str[:-5]
			try:
				print delete_str
				# 执行sql语句
				self.cursor.execute(delete_str)
				# 提交到数据库执行
				self.db.commit()
				return "success"
			except:
				# Rollback in case there is any error
				self.db.rollback()
				return "error"
		except Exception, e:
			print str(e)
			return "error"

	def get_query_s_e_time(self, table_name, device_id = None, key = None, start_time = None, end_time = None, no=None, order_key=None):
		query_str = "select * from " + table_name
		if key is not None and start_time is not None and end_time is not None:
			query_str += " where "
			query_str += key + '>= "' + start_time + '" and ' + key + '<= "' + end_time + '" ' + ' and ' + ' 项目内节点编号 = "' + device_id + '"'
		if order_key is not None:
			query_str += " order by " + order_key
		# 获取列名
		self.cursor.execute('DESC ' + table_name)
		columns = self.cursor.fetchall()
		# print columns
		columns_list = []
		for c in columns:
			columns_list.append(c[0])
		columns_list.append("id")
		# 获取要查询的数据
		print query_str
		self.cursor.execute(query_str)
		results = self.cursor.fetchall()
		query_result = []
		if no is not None:
			add = 0
			for row in results:
				dic_tmp = {}
				for idx in range(len(row)):
					key = columns_list[idx]
					val = row[idx]
					dic_tmp[key] = val
				query_result.append(dic_tmp)
				add += 1
				if add == no:
					break
		else:
			for row in results:
				# print row
				dic_tmp = {}
				for idx in range(len(row)):
					key = columns_list[idx]
					val = row[idx]
					dic_tmp[key] = val
				query_result.append(dic_tmp)
		return query_result

	def close_connect(self):
		self.db.close()


if __name__ == '__main__':
	pass
	sql = MySQL()
	sql.connectDB("python_test")
	data = {}
	data["number"] = "1111111"
	data["name"] = "testupdate"
	data["birthday"] = "2000-01-01 01:01:01"
	kvs = {}
	kvs["number"] = "1111111"
	kvs["name"] = "testupdate"
	sql.delete_data("person", kvs)
	sql.close_connect()
	# from datetime import datetime
	# NOW = datetime.today()
	# start = datetime(NOW.year, NOW.month, NOW.day, 0, 0, 0)
	# datas = sql.get_query(u"大气六参数", u"紧缩性时间传感器_实时时间", ">", start.strftime("%Y-%m-%d %H:%M:%S"), None, u"紧缩性时间传感器_实时时间")
	# print datas
	# sql.close_connect()
	# sql.connectDB()
	# data = {}
	# data["number"] = "20150030"
	# data["name"] = "AP"
	# data["birthday"] = "1994-10-23"
	# print sql.insert_data("person", data)
	# print sql.get_query(u"大气六参数")
	# print sql.get_query("person", "birthday", None, None, None, "birthday")
	# print sql.update_data("person", data, "1")
	# print sql.delete_data("person", 2)
	# from datetime import datetime, timedelta
	# import random
	# today = datetime.today()
	# hour1 = timedelta(hours=1)
	# data_list = []
	# for i in range(9):
	# 	sql.delete_data("data", i+101)
	# 	data = {}
	# 	data["device_id"] = 1
	# 	data["pm25"] = random.randint(0,500)
	# 	data["so2"] = random.randint(0,200)
	# 	data["co"] = random.randint(0,200)
	# 	data["no2"] = random.randint(0,200)
	# 	data["o3"] = random.randint(0,200)
	# 	data["pm10"] = random.randint(0,200)
	# 	data["time"] = today
	# 	today -= hour1
	# 	sql.insert_data("data", data)
	# longitude_s = 117.2944
	# latitude_s = 30.4127
	# for i in range(10):
		# sql.delete_data("device", 41)
		# data = {}
		# data["name"] = u"观测点" + str(i)
		# data["address"] = u"池州"
		# data["longitude"] = longitude_s
		# data["latitude"] = latitude_s
		# longitude_s += 0.001
		# latitude_s += 0.001
		# data["install_time"] = today
		# sql.insert_data("device", data)
	# sql.close_connect()