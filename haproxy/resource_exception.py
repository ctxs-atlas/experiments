

class ResourceException(Exception):
	def __init__(self,  errors, failure_status):
		self.errors = errors
		self.failure_status = failure_status