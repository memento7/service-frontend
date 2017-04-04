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

	
	def __init__(self, id, title, type, date, 
				issue_score, top_percentile, issue_rank=None,
				images=[], entities=[],
				keywords=[], emotions=[], summaries=[], three_line_summaries=[],
				article_count=None, sns_count=None, comment_count=None,
				hit=0, created_time=None, updated_time=None, published_time=None, **kwarg) :
		
		self.id = id
		self.title = Event.tag_remover.sub('', title)
		self.type = type
		self.date = date

		self.keywords = keywords
		self.emotions = emotions
		self.three_line_summaries = three_line_summaries
		self.images = images
		self.entities = entities

		self.issue_score = {
			'score': issue_score,
			'ranking': issue_rank,
			'top_percentile': top_percentile,
			'source': {
				'article_count': article_count,
				'sns_count': sns_count,
				'comment_count': comment_count,
			}
		}

		self.created_time = created_time
		self.updated_time = updated_time
		self.published_time = published_time



Event.register({
	'id': 80001,
	'date': "2017-01-01 00:00:00",
	'title': "김태희-비 열애끝에 결혼",
	'type': '연예',
	'issue_score': 300000,
	'issue_score_rank': 8,
	'top_percentile': 1.3131,
	'article_count': 1231,
	'comment_count': 41231,
	'emotions': [
		{ 'keyword': "축하해요", 'weight': 70 },
		{ 'keyword': "사랑스러워요", 'weight': 70 },
		{ 'keyword': "부러워요", 'weight': 50 },
		{ 'keyword': "아름다워요", 'weight': 40 },
		{ 'keyword': "슬퍼요", 'weight': 30 },
		{ 'keyword': "예뻐요", 'weight': 30 },
		{ 'keyword': "황홀해요", 'weight': 20 },
		{ 'keyword': "멋져요", 'weight': 20 },
		{ 'keyword': "화나요", 'weight': 10 },
		{ 'keyword': "수줍어요", 'weight': 10 },
	],
	'keywords': [
		{ 'keyword': "결혼식", 'weight': 80 },
		{ 'keyword': "편지", 'weight': 80 },
		{ 'keyword': "5년", 'weight': 705 },
		{ 'keyword': "신혼여행", 'weight': 60 },
		{ 'keyword': "인스타그램", 'weight': 60 },
		{ 'keyword': "최고의 선물", 'weight': 405 },
		{ 'keyword': "가회동 성당", 'weight': 405 },
		{ 'keyword': "화보", 'weight': 30 },
		{ 'keyword': "싸이", 'weight': 30 },
		{ 'keyword': "연애", 'weight': 30 },
		{ 'keyword': "경건한", 'weight': 10 },
		{ 'keyword': "인터뷰", 'weight': 10 },
	],
	'images': [
		{
			'path': 'https://i.ytimg.com/vi/sg_Z7kspl6E/maxresdefault.jpg',
		}
	],
	'three_line_summaries': [
		{
			'id': 1,
			'content': [
				'배우 김태희와 가수 비가 연애 5년만에 결혼했다.',
				'비는 자신의 인스타그램에 손편지로 이를 알렸다.',
				'결혼식은 소박하게 성당에서 진행되었다.'
			],
			'author': '요약GO',
			'like': 130,
			'hate': 3,
			'date': '2017-01-03 13:03:42'
		},
		{
			'id': 2,
			'content': [
				'김태희 ㅈㄴ 예쁘다',
				'김태희 ㅈ~ㄴ 예쁘다',
				'비 도둑놈 새기'
			],
			'author': 'Prev',
			'like': 91,
			'hate': 46,
			'date': '2017-01-10 10:45:13'
		}
	],

	'entities': [
		{
			'id': 70002,
			'nickname': "김태희",
			'roles': ['배우'],
			'images': [
				{
					'path': "https://search.pstatic.net/common?type=o&size=120x150&quality=95&direct=true&src=http%3A%2F%2Fsstatic.naver.net%2Fpeople%2F28%2F201406261348278841.jpg",
					'heart': 0
				}
			],
		},
		{
			'id': 70003,
			'nickname': "비",
			'realname': "정지훈",
			'roles': ['가수', '배우'],
			'images': [
				{
					'path': "https://search.pstatic.net/common?type=o&size=120x150&quality=95&direct=true&src=http%3A%2F%2Fsstatic.naver.net%2Fpeople%2F71%2F20170123185015611.jpg",
					'heart': 0
				}
			],
		}
	],
	'event_articles': [
		{
			'title': '비, 김태희와 결혼하더니 더 진해진 남자의 향기',
			'description': '가수 비가 근황을 공개했다. 비는 2월 26일 자신의 인스타그램에 남자의 향기를 물씬 풍기는 사진 한 장을 게재했다.',
			'source': '뉴스엔',
			'image': 'https://search.pstatic.net/common/?src=http%3A%2F%2Fimgnews.naver.net%2Fimage%2Forigin%2F5033%2F2017%2F02%2F26%2F1451305.jpg&type=ofullfill80_80_q75_re2',
			'link': 'http://www.newsen.com/news_view.php?uid=201702260807041210'
		},
		{
			'title': '비♥김태희, 오늘(23일) 화보촬영차 이탈리아 출국 “조용히 움직일것”',
			'description': '오후 뉴스엔에 "화보 촬영차 출국하는 건 맞지만 조용히 움직일 예정이다"고 말했다.',
			'source': '뉴스엔',
			'image': 'https://search.pstatic.net/common/?src=http%3A%2F%2Fimgnews.naver.net%2Fimage%2Forigin%2F5033%2F2017%2F02%2F23%2F1450354.jpg&type=ofullfill80_80_q75_re2',
			'link': 'http://www.newsen.com/news_view.php?uid=201702230915310410'

		},
		{
			'title': '김태희·비 부부 뒤늦은 신혼살림 준비',
			'description': '부부가 와 가구를 골라 샀다"며 "집은 청담인데 직영인 우리 매장에서 제품을 골랐다"고 전했다. ',
			'source': '중앙일보',
			'image': 'https://search.pstatic.net/common/?src=http%3A%2F%2Fimgnews.naver.net%2Fimage%2Forigin%2F025%2F2017%2F02%2F23%2F2688296.jpg&type=ofullfill80_80_q75_re2',
			'link': 'http://news.naver.com/main/read.nhn?mode=LSD&mid=sec&sid1=106&oid=025&aid=0002688296'
		},
	]
})
