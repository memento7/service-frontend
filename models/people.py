from models.event import Event
import settings
import requests
import globals

class People :

	_roleinfo = None
	_instances = {}


	@staticmethod
	def get_roleinfo(key=None) :
		""" Get role info on API Server
		"""
		if not People._roleinfo :
			# If roleinfo is not initialzied, init info
			role_arr = requests.get(settings.API_BASE_URL + '/entities/roles').json()
			rv = {}

			for role in role_arr :
				rv[role['key']] = role

			People._roleinfo = rv

		# If key, get info by key
		# Else, return all dictionary
		if key :
			return People._roleinfo[key]
		else :
			return People._roleinfo


	@staticmethod
	def register(data) :
		if type(data) == dict :
			instance = People(**data)
		else :
			instance = data

		People._instances[instance.id] = instance
		return instance


	@staticmethod
	def get(id) :
		return People._instances[id]


	
	def __init__(self, id, nickname, realname, role_json,
				images, events, status=0,
				created_time=None, updated_time=None, published_time=None, **kwarg):

		self.id = id
		self.nickname = nickname
		self.role_json = role_json
		self.status = status
		self.created_time = created_time
		self.updated_time = updated_time
		self.published_time = published_time
		self.images = images



		# tmp
		self.events = events
		for event in self.events :
			event['title'] = Event.tag_remover.sub('', event['title'])

		# self.events = []
		# for event in events :
		# 	self.events.append( Event(**event) )

		self.init_roles()


	def init_roles(self) :
		roles = {}
		stat_counts = 0

		for roleid, value in self.role_json.items() :
			roleinfo = People.get_roleinfo(roleid)

			roles[roleid] = {
				'info': roleinfo,
				'name': roleinfo['name'],
				'data': value['data']
			}

			stats = None
			try :
				stats = roles[roleid]['data']['score']
			except KeyError as ke : pass
			except e : raise e

			if stats :
				roles[roleid]['stats2'] = {
					'labels': [globals.l10n(i) for i in stats.keys()],
					'datas': [globals.l10n(i) for i in stats.values()],
				}
				stat_counts += 1


		self.roles = roles
		self.stat_counts = stat_counts



People.register({
	'id': 70001,
	'nickname': "수지",
	'realname': "배수지",
	'is_mockup': True,
	'status': 4,
	'images': [
		{
			'path': "http://movie.phinf.naver.net/20120227_135/1330332776326RN3D6_JPEG/movie_image.jpg?type=m665_443_2",
			'heart': 0
		}
	],
	'in_one_word': [
		{
			'keyword': "국민 첫사랑",
			'reference': "",
			'order': 0
		}
	],
	'role_json': {
		"ACTOR": {
			'data': {
				'score': {
					'looks': 9.4,
					'empathy': 4.0,
					'perform': 6.8,
					'roleplay': 4.1,
					'stability': 1.6,
				}
			}
		},
		"SINGER": {
			'data': {
				'score': {
					'dance': 7.9,
					'looks': 9.4,
					'emotional': 3.3,
					'composition': 2.1,
					'singability': 3.6,
				}
			}
		}
	},
	'group': {
		'name': 'Miss A',
		'belongs': 'JYP Entertainment',
		'members': [
			{
				'name': '지아',
				'image': 'https://search.pstatic.net/common?type=o&size=120x150&quality=95&direct=true&src=http%3A%2F%2Fsstatic.naver.net%2Fpeople%2F8%2F201612071901428361.jpg'
			},
			{
				'name': '민',
				'image': 'https://search.pstatic.net/common?type=o&size=120x150&quality=95&direct=true&src=http%3A%2F%2Fsstatic.naver.net%2Fpeople%2F6%2F201612071902269531.jpg'
			},
			{
				'name': '수지',
				'image': 'https://search.pstatic.net/common?type=o&size=120x150&quality=95&direct=true&src=http%3A%2F%2Fsstatic.naver.net%2Fpeople%2F4%2F201612071904526981.jpg'
			},
			{
				'name': '페이',
				'image': 'http://img.rsrs.co.kr/artist/images/500/800730/80073014.jpg'
			},
		]
	},
	'events': []
})

People.register({
	'id': 70002,
	'nickname': "김태희",
	'realname': "김태희",
	'is_mockup': True,
	'status': 4,
	'images': [
		{
			'path': "http://club.draghome.com/folder/10000057/board/10000/10862/kim3.jpg",
			'heart': 0
		}
	],
	'in_one_word': [
		{
			'keyword': "김태희가 듣는 수업은\n언제나 학생들로 꽉 차있었다",
			'reference': "당시 서울대 재학생",
			'order': 0
		}
	],
	'role_json': {
		"ACTOR": {
			'data': {
				'score': {
					'looks': 9.4,
					'empathy': 4.0,
					'perform': 7.9,
					'roleplay': 4.1,
					'stability': 1.6,
				}
			}
		}
	},
	'events': [
		{
			'id': 80001,
			'date': "2017-01-19 00:00:00",
			'title': "김태희-비 열애끝에 결혼",
			'type': '연예',
			'issue_score': 300000,
			'emotions': [
				{
					'title': "축하해요",
					'weight': 0.7
				},
				{
					'title': "사랑스러워요",
					'weight': 0.7
				},
				{
					'title': "부러워요",
					'weight': 0.5
				},
				{
					'title': "아름다워요",
					'weight': 0.4
				},
			],
			'images': [
				{
					'path': 'https://i.ytimg.com/vi/sg_Z7kspl6E/maxresdefault.jpg',
				}
			]
		},
		{
			'id': 80002,
			'date': "2015-08-15 00:00:00",
			'title': "SBS 드라마 '용팔이' 출연",
			'type': '미디어',
			'issue_score': 15000,
			'emotions': [
				{
					'title': "멋져요",
					'weight': 0.4
				},
				{
					'title': "아름다워요",
					'weight': 0.4
				},
			],
			'images': [
				{
					'path': 'http://www.fashionn.com/files/board/2015/image/p1a0ridlphkkvlevf7r1rbptpi1.jpg',
				}
			]
		},
		{
			'id': 80003,
			'date': "2013-01-01 00:00:00",
			'title': "김태희-비 열애",
			'type': '연예',
			'issue_score': 230000,
			'emotions': [
				{
					'title': "놀라워요",
					'weight': 0.8
				},
				{
					'title': "축하해요",
					'weight': 0.7
				},
			],
			'images': [
				{
					'path': 'http://cfile1.uf.tistory.com/image/191E223650E2E5F642A8D9',
				}
			]
		},
		{
			'id': 80004,
			'date': "2009-10-14 00:00:00",
			'title': "KBS 드라마 '아이리스' 출연",
			'type': '미디어',
			'issue_score': 19000,
			'emotions': [
				{
					'title': "재미있어요",
					'weight': 0.8
				},
				{
					'title': "아름다워요",
					'weight': 0.5
				},
			],
			'images': [
				{
					'path': 'https://encrypted-tbn2.gstatic.com/images?q=tbn:ANd9GcT1Ur3zsQjMWFAMSM7CVeoW0CUXdI7RAEiUaARm_KKLtWr56-wmVA',
				}
			]
		},
	],
})
