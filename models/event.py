import re

class Event :

	tag_remover = re.compile(r'<[^>]+>')
	_instances = {}


	@staticmethod
	def register(data) :
		if type(data) == dict :
			instance = Event(**data)
		else :
			instance = data

		Event._instances[instance.id] = instance
		return instance

		

	@staticmethod
	def get(id) :
		return Event._instances[id]

	
	def __init__(self, id, title, type, date, issue_data,
				images=[], entities=[],
				keywords=[], emotions=[], summaries=[], summaries3line=[],
				hit=0, created_time=None, updated_time=None, published_time=None, **kwarg) :
		
		self.id = id
		self.title = Event.tag_remover.sub('', title)
		self.type = type
		self.date = date

		self.keywords = keywords
		self.emotions = emotions
		self.summaries3line = summaries3line
		self.images = images
		self.entities = entities

		self.issue_data = issue_data

		# self.issue_score = {
		# 	'score': issue_data.get('issue_score', None),
		# 	'top_percentile': issue_data.get('top_percentile', None),
		# 	'ranking': issue_data.get('issue_rank', None),
		# 	'source': {
		# 		'article_count': issue_data.get('article_count', None),
		# 		'sns_count': issue_data.get('sns_count', None),
		# 		'comment_count': issue_data.get('comment_count', None),
		# 	}
		# }

		self.created_time = created_time
		self.updated_time = updated_time
		self.published_time = published_time



