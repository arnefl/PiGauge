import yaml


class Configuration:
	"""
	Configuration manager
	"""
	def __init__(self):
		# Load configuration file
		self.config_file = '../config.yml'
		with open(self.config_file, 'r') as yamlfile:
			self.config = yaml.full_load(yamlfile)


	# Python magic for class to act as dict
	def __getitem__(self, key):
		return self.config[key]

	def __setitem__(self, key, value):
		# Update current state
		self.config[key] = value

	def save(self):
		# Update configuration file
		with open(self.config_file, 'w') as yamlfile:
			yaml.dump(self.config, yamlfile)
