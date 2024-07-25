class Service:
	def __init__(self, service_setting):
		self.provider = service_setting['provider']
		self.settings = service_setting['settings']


	def start(self):
		self.provider.get_data()
