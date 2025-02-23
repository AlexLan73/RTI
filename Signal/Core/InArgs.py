import json
class InArgs:
	def __init__(self, path):
		with open(path, 'r') as file:
			self.Params = json.load(file)

	def get(self, path):
		with open(path, 'r') as file:
			self.Params = json.load(file)
