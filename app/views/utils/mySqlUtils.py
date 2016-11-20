# coding=utf-8
import MySQLdb


class MySQL(object):
	def __init__(self):
		self.host = '127.0.0.1'
		self.user = 'root'
		self.password = '123456'
		self.database = 'python_test'
		self.db = None
		self.cursor = None

	def connectDB(self):
		self.db = MySQLdb.connect(self.host, self.user, self.password, self.database)
		self.cursor = self.db.cursor()
		return self.cursor

	def get_query(self, table_name, query_key = None, query_conn = None, query_val = None, no = None, order_key=None):
		query_str = "select * from " + table_name
		if query_key is None and query_val is not None and query_val is not None:
			query_str += " where " + query_key + query_conn + '"' + query_val + '"'
		if order_key is not None:
			query_str += " order by " + order_key
		# 获取列名
		self.cursor.execute('DESC ' + table_name)
		columns = self.cursor.fetchall()
		print columns
		columns_list = []
		for c in columns:
			columns_list.append(c[0])
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
				left_str += ('"' + val + '",')
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

	def update_data(self, table_name, data, id):
		try:
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
			left_str += " WHERE id = "
			left_str += str(id)
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

	def delete_data(self, table_name, id):
		try:
			delete_str = "DELETE FROM " + table_name + " WHERE id = " + str(id)
			try:
				# 执行sql语句
				self.cursor.execute(delete_str)
				# 提交到数据库执行
				self.db.commit()
			except:
				# Rollback in case there is any error
				self.db.rollback()
			return "success"
		except Exception, e:
			print str(e)
			return "error"

	def close_connect(self):
		self.db.close()


if __name__ == '__main__':
	sql = MySQL()
	sql.connectDB()
	data = {}
	data["number"] = "20150030"
	data["name"] = "AP"
	data["birthday"] = "1994-10-23"
	# print sql.insert_data("person", data)
	# print sql.get_query("person", "birthday", None, None, None, "birthday")
	# print sql.update_data("person", data, "1")
	# print sql.delete_data("person", 2)
	sql.close_connect()