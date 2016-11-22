#coding=utf-8
import math
class AqiParameter(object):
	def __init__(self):
		self.IAQI_24 = []
		self.IAQI_1 = []
		self.AQI_24 = 0
		self.AQI_1 = 0
		self.Main_Pollute_24 = ''
		self.Main_Pollute_1 = ''
		self.fix_value_24 = [{"so2": [{"level":0, "value": 1}, {"level":50, "value": 1.0/2},{"level":150, "value": 2.0/13},{"level":475, "value": 2.0/13},{"level":800, "value": 1.0/8},{"level":1600, "value": 1.0/5},{"level":2100, "value": 5.0/26}] },
							 {"no2": [{"level":0, "value": 5.0/4}, {"level":40, "value": 5.0/4}, {"level":80, "value": 1.0/2}, {"level":180, "value": 1.0/2}, {"level":280, "value": 10.0/57}, {"level":565, "value": 20.0/37}, {"level":750, "value": 10.0/19}]},
							 {"pm10":[{"level":0, "value":1}, {"level":50, "value":1.0/2}, {"level":150, "value":1.0/2}, {"level":250, "value":1.0/2}, {"level":350, "value":10.0/7}, {"level":420, "value":5.0/4}, {"level":500, "value":1} ]},
							 {"co":[{"level":0, "value": 25}, {"level":2, "value": 25}, {"level":4, "value": 5}, {"level":14, "value": 5}, {"level":24, "value": 25.0/3}, {"level":36, "value": 25.0/3}, {"level":48, "value": 25.0/3}]},
							 {"o3":[{"level":0, "value": 1.0/2}, {"level":100, "value": 5.0/6}, {"level":160, "value": 10.0/11}, {"level":215, "value": 1}, {"level":265, "value": 20.0/107}, {"level":800, "value": 1.0/2}, {"level":1000, "value": 1.0/2}]},
							 {"pm25": [{"level":0,"value":10.0/7} ,{"level":35,"value":5.0/4} ,{"level":75,"value":5.0/4} ,{"level":115,"value":10.0/7} ,{"level":150,"value":1} ,{"level":250,"value":1} ,{"level":350,"value":2.0/3}]}
							 ]
		self.fix_value_1 = [{"so2": [{"level":0, "value": 1.0/3}, {"level":150, "value": 1.0/7},{"level":500, "value": 1.0/3},{"level":650, "value": 1.0/3},{"level":800, "value": 1.0/8},{"level":1600, "value": 1.0/5},{"level":2100, "value": 5.0/26}] },
							 {"no2": [{"level":0, "value": 1.0/2}, {"level":100, "value": 1.0/2}, {"level":200, "value": 1.0/10}, {"level":700, "value": 1.0/10}, {"level":1200, "value": 5.0/57}, {"level":2340, "value": 2.0/15}, {"level":3090, "value": 2.0/15}]},
							 {"pm10":[{"level":0, "value":1}, {"level":50, "value":1.0/2}, {"level":150, "value":1.0/2}, {"level":250, "value":1.0/2}, {"level":350, "value":10.0/7}, {"level":420, "value":5.0/4}, {"level":500, "value":1} ]},
							 {"co":[{"level":0, "value": 10}, {"level":5, "value": 10}, {"level":10, "value": 2}, {"level":35, "value": 2}, {"level":60, "value": 10.0/3}, {"level":90, "value": 10.0/3}, {"level":120, "value": 10.0/3}]},
							 {"o3":[{"level":0, "value": 5.0/16}, {"level":160, "value": 5.0/4}, {"level":200, "value": 1.0/2}, {"level":300, "value": 1.0/2}, {"level":400, "value": 1.0/4}, {"level":800, "value": 1.0/2}, {"level":1000, "value": 1.0/2}]},
							 {"pm25": [{"level":0,"value":10.0/7} ,{"level":35,"value":5.0/4} ,{"level":75,"value":5.0/4} ,{"level":115,"value":10.0/7} ,{"level":150,"value":1} ,{"level":250,"value":1} ,{"level":350,"value":2.0/3}]}
							 ]
		self.start_point = [400,300,200,150,100,50,0]
		self.AQI_info_24 = {}
		self.AQI_info_1 = {}
		self.AQI_info_standard = [{"val":0, "level_no": 1, "level": "一级", "classification": "优", "health": "空气质量令人满意，基本无空气污染", "step": "各类人群可正常活动"},
								  {"val": 50, "level_no": 2, "level": "二级", "classification": "良", "health": "空气质量可接受，但某些污染物可能对极少数异常敏感人群健康有较弱影响",
								   "step": "极少数异常敏感人群应减少户外活动"},
								  {"val": 100, "level_no": 3, "level": "三级", "classification": "轻度污染","health": "易感人群症状有轻度加剧，健康人群出现刺激状况",
								   "step": "儿童，老年人及心脏病，呼吸系统疾病患者应减少长时间，高强度的户外训练"},
								  {"val": 150, "level_no": 4, "level": "四级", "classification": "中度污染",
								   "health": "进一步加剧易感人群症状，可能对健康人群心脏，呼吸系统有影响",
								   "step": "儿童，老年人及心脏病，呼吸系统疾病患者避免长时间，高强度的户外训练，一般人群适量减少户外运动"},
								  {"val": 200, "level_no": 5, "level": "五级", "classification": "重度污染",
								   "health": "心脏病和肺病患者症状显著加剧，运动耐受力降低，健康人群普遍出现症状",
								   "step": "儿童，老年人及心脏病，呼吸系统疾病患者应停留在室内，停止户外运动，一般人群减少户外运动"},
								  {"val": 300, "level_no": 6, "level": "六级", "classification": "严重污染",
								   "health": "健康人群运动耐受力降低，有明显强烈症状，提前出现某些疾病",
								   "step": "儿童，老年人和病人应当留在室内，避免体力消耗，一般人群应避免户外运动"}
								  ]
		self.AQI_info_standard.reverse()

	def get_24_iaqi(self, data):
		for key in data.keys():
			key = key
			val = data[key]
			for i in range(len(self.fix_value_24)):
				if self.fix_value_24[i].keys()[0] == key:
					print self.fix_value_24[i]
					level_data = self.fix_value_24[i].values()[0]
					cnt = -1
					level_data.reverse()
					for level in level_data:
						cnt += 1
						if val > level["level"]:
							print level
							print self.start_point[cnt]
							iaqi = round((val - level["level"]) * level["value"] + self.start_point[cnt])
							self.IAQI_24.append(iaqi)
							break
					break

	def get_1_iaqi(self, data):
		for key in data.keys():
			key = key
			val = data[key]
			for i in range(len(self.fix_value_1)):
				if self.fix_value_1[i].keys()[0] == key:
					# print self.fix_value_1[i]
					level_data = self.fix_value_1[i].values()[0]
					cnt = -1
					level_data.reverse()
					for level in level_data:
						cnt += 1
						if val > level["level"]:
							# print level
							# print self.start_point[cnt]
							iaqi = round((val - level["level"]) * level["value"] + self.start_point[cnt])
							self.IAQI_1.append(iaqi)
							break
					break
		self.AQI_1 = max(self.IAQI_1)

	def get_1_aqi(self, data):
		self.get_1_iaqi(data)
		self.AQI_1 = max(self.IAQI_1)
		if self.AQI_1 > 50:
			pollute_str = ["so2", "no2", "pm10", "co2", "o3", "pm2.5"]
			max_val = -1
			max_name = ""
			for idx, val in enumerate(self.IAQI_1):
				if val > max_val:
					max_name = pollute_str[idx]
		else:
			max_name = "无"
		self.Main_Pollute_1 = max_name
		for x in self.AQI_info_standard:
			if self.AQI_1 > x["val"]:
				self.AQI_info_1["level_no"] = x["level_no"]
				self.AQI_info_1["level"] = x["level"]
				self.AQI_info_1["classification"] = x["classification"]
				self.AQI_info_1["health"] = x["health"]
				self.AQI_info_1["step"] = x["step"]
				break

	def get_24_aqi(self, data):
		self.get_24_iaqi(data)
		self.AQI_24 = max(self.IAQI_24)
		if self.AQI_24 > 50:
			pollute_str = ["so2", "no2", "pm10", "co2", "o3", "pm2.5"]
			max_val = -1
			max_name = ""
			for idx, val in enumerate(self.IAQI_24):
				if val > max_val:
					max_name = pollute_str[idx]
		else:
			max_name = "无"
		self.Main_Pollute_24 = max_name
		self.AQI_24 = max(self.IAQI_24)
		for x in self.AQI_info_standard:
			if self.AQI_24 > x["val"]:
				self.AQI_info_24["level_no"] = x["level_no"]
				self.AQI_info_24["level"] = x["level"]
				self.AQI_info_24["classification"] = x["classification"]
				self.AQI_info_24["health"] = x["health"]
				self.AQI_info_24["step"] = x["step"]
				break


if __name__ == '__main__':
	aqi = AqiParameter()
	data = {"so2": 32, "no2": 53, "pm10": 294, "co": 2, "o3": 33, "pm25": 158}
	# aqi.get_24_iaqi(data)
	aqi.get_1_aqi(data)
	print aqi.Main_Pollute_1
	print aqi.AQI_info_1
	# for i in range(len(aqi.fix_value_24)):
	# 	print aqi.fix_value_24[i].keys()[0]
	# 	val = aqi.fix_value_24[i].values()[0]
	# 	print type(val)
	# 	try:
	# 		val.reverse()
	# 	except Exception, e:
	# 		print(str(e))
	# 	for i in val:
	# 		print i


