from models.event import Event
import settings
import requests
import globals

class People :

	role_info = None

	people_data = {
		70001: {
			'id': 70001,
			'nickname': "수지",
			'realname': "배수지",
			'is_mockup': True,
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
			'role_json': {"ACTOR": {}, "SINGER": {}},

			'role_datas': {
				'배우': {
					'record_stats': [9.4, 4.0, 7.9, 4.1, 1.6],
					'영화': [],
					'드라마': [],
				},
				'가수': {
					'record_stats': [9.4, 4.0, 7.9, 4.1, 1.6],
					'앨범': [],
					'공연': [],
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
		},

		70002: {
			'id': 70002,
			'nickname': "김태희",
			'realname': "김태희",
			'is_mockup': True,
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
			'role_json': {"ACTOR": {}},
			'role_datas': {
				'배우': {
					'record_stats': [9.4, 4.0, 7.9, 4.1, 1.6],
					'영화': [],
					'드라마': [],
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
		}
	}

	@staticmethod
	def get_role_info(key=None) :
		if not People.role_info :
			r = requests.get(settings.API_BASE_URL + '/entities/roles')
			role_arr = r.json()
			rv = {}

			for role in role_arr :
				rv[role['key']] = role

			People.role_info = rv

		if key :
			return People.role_info[key]
		else :
			return People.role_info


	@staticmethod
	def register(id, data) :
		for event in data['events'] :
			event['title'] = Event.tag_remover.sub('', event['title'])

		stat_record_counts = 0
		rj = data['role_json']
		for role, value in rj.items() :
			rj[role]['info'] = People.get_role_info(role)
			rj[role]['name'] = rj[role]['info']['name']

			sr = None
			try :
				sr = rj[role]['data']['score']
			except KeyError as ke :
				pass
			except e :
				raise e

			if sr :
				rj[role]['stat_records'] = {
					'labels': [globals.l10n(i) for i in sr.keys()],
					'datas': [globals.l10n(i) for i in sr.values()],
				}
				stat_record_counts += 1


		data['stat_record_counts'] = stat_record_counts
		People.people_data[id] = data
		return data


	@staticmethod
	def get(id) :
		data = People.people_data[id]
		return data


	"""
	def __init__(self,
			id,
			nickname,
			realname,
			rolejson,
			status,
			created_time,
			updated_time,
			published_time,
			images,
			events,
			**kwarg):
		pass
	"""


