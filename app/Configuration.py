import yaml


class Configuration:
	"""
	Configuration manager
	"""
	def __init__(self):
		# Load configuration file
		with open('../config.yml', 'r') as yamlfile:
			self.config = yaml.full_load(yamlfile)


	# Python magic for class to act as dict
	def __getitem__(self, key):
		return self.config[key]
