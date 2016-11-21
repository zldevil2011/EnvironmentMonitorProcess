class AqiParameter(object):
	def __init__(self):
		self.so2_24 = 0
		self.so2_1 = 0
		self.no2_24 = 0
		self.no2_1 = 0
		self.pm10_24 = 0
		self.pm10_1 = 0
		self.co_24 = 0
		self.co_1 = 0
		self.o3_24 = 0
		self.o3_1 = 0
		self.pm25_24 = 0
		self.pm25_1 = 0
		self.IAQI = []
		self.AQI = 0
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
		self.start_point = [0,50,100,150,200,300,400]

	def get_iaqi(self):
		if self.so2_24 == 0

