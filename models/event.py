from models.people import People
from lib import functions

from datetime import datetime
import re

class Event :

	tag_remover = re.compile(r'<[^>]+>')
	_instances = {}
	CATEGORIES = ['연예', '정치', '스포츠', '미디어', '세계', '기타']

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
				images=[], entities=[], event_articles=[],
				keywords=[], emotions=[], summaries=[], summaries3line=[],
				hit=0, created_time=None, updated_time=None, published_time=None, **kwarg) :
		
		self.id = id
		self.title = Event.tag_remover.sub('', title)
		self.category = type
		self.date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')


		self.issue_data = EventIssueData(**issue_data)
		
		self.event_articles = []
		for article in event_articles :
			self.event_articles.append( EventArticle(**article) )

		self.event_articles.sort(key=lambda a: a.rank)


		self.entities = []
		for entity in entities :
			self.entities.append( People(**entity) )


		self.keywords = keywords
		self.emotions = emotions
		self.summaries3line = summaries3line
		self.images = images

		self.created_time = created_time
		self.updated_time = updated_time
		self.published_time = published_time


	def repr_image(self, css_mode=False, thumbnail=False) :
		""" Get representative image of person
		"""
		return functions.first_image(self.images, css_mode, thumbnail)


	def category_id(self) :
		return chr( Event.CATEGORIES.index(self.category) + 97 )


	def magazine_url(self) :
		return functions.geturl('event', self.id)



class EventIssueData :
	""" event.issue_data DTO
	"""
	def __init__(self, issue_score, top_percentile, issue_rank=None,
				article_count=None, sns_count=None, comment_count=None, **kwarg) :

		self.issue_score = issue_score
		self.top_percentile = top_percentile
		self.ranking = issue_rank

		self.article_count = article_count
		self.sns_count = sns_count
		self.comment_count = comment_count

		self.f_article_count = article_count and '{0:,}'.format(article_count) or None
		self.f_sns_count	 = sns_count and '{0:,}'.format(sns_count) or None
		self.f_comment_count = comment_count and '{0:,}'.format(comment_count) or None

	
	def rank(self) :
		if self.top_percentile is None :	return '?'
		elif self.top_percentile <= 2  :	return 's'
		elif self.top_percentile <= 10 :	return 'a'
		elif self.top_percentile <= 50 :	return 'b'
		else :								return 'c'


	def label(self) :
		return {
			's': '세간',
			'a': '이슈',
			'b': '그냥',
			'c': '저냥',
			'?': '오류',
		}[ self.rank() ]


	def full_label(self) :
		return {
			's': '세간의 관심',
			'a': '이슈 오브 이슈',
			'b': '세상의 이야기',
			'c': '그냥저냥 뉴스',
			'?': '오류',
		}[ self.rank() ]


	def mention(self) :
		return {
			's': '이 사건도 모르면 간첩이죠! 정말 뜨거웠던 이야기였어요',
			'a': '꽤 화제가 많이 된 사건이었어요!',
			'b': '나름 재미있는 소식이었어요',
			'c': '이런 소식도 있었네요',
			'?': '오류가 발생했습니다',
		}[ self.rank() ]



class EventArticle :
	""" event.event_article DTO
	"""
	def __init__(self, id, title, source_url, crawl_target,
				 rank, images=[], image=None,
				 comment_count=None, summary=None, **kwarg) :

		self.id = id
		self.title = Event.tag_remover.sub('', title)
		self.source_url = source_url
		self.crawl_target = crawl_target

		self.rank = rank
		self.images = images

		if not images and image :
			self.images = [image]
		
		self.comment_count = comment_count
		self.summary = summary


	def repr_image(self, css=False) :
		""" Get representative image of person
		"""
		return functions.first_image(self.images, css)

