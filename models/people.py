class People :

	role_stat_info = {
		'배우': ['외모', '감정 연기', '안정감', '배역 소화도', '액션'],
		'가수': ['가창력', '외모', '댄스', '작곡', '감정 호소'],
	}


	people_data = {
		'수지': {
			'name': "수지",
			'real_name': "배수지",
			'images': [
				{
					'url': "http://movie.phinf.naver.net/20120227_135/1330332776326RN3D6_JPEG/movie_image.jpg?type=m665_443_2",
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
			'role_datas': {
				'배우': {
					'_stats': [9.4, 4.0, 7.9, 4.1, 1.6],
					'영화': [],
					'드라마': [],
				},
				'가수': {
					'_stats': [9.4, 4.0, 7.9, 4.1, 1.6],
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
			'timeline': []
		},

		'김태희': {
			'name': "김태희",
			'images': [
				{
					'url': "http://club.draghome.com/folder/10000057/board/10000/10862/kim3.jpg",
					'heart': 0
				}
			],
			'in_one_word': [
				# {
				# 	'keyword': '김태희 그 자체'
				# },
				{
					'keyword': "김태희가 듣는 수업은\n언제나 학생들로 꽉 차있었다",
					'reference': "당시 서울대 재학생",
					'order': 0
				}
				# {
				# 	'keyword': "누군가 한국을 대표하는 대표 여배우를 꼽으라고 한다면, 1초의 망설임도 없이 김태희를 꼽을것이다",
				# 	'reference': "메멘토 개발자 중 1명",
				# 	'order': 0
				# }
			],
			'role_datas': {
				'배우': {
					'_stats': [9.4, 4.0, 7.9, 4.1, 1.6],
					'영화': [],
					'드라마': [],
				}
			},
			'timeline': [
				{
					'id': 101,
					'date': "2017-01-19",
					'title': "김태희-비 열애끝에 결혼",
					'category': '연예',
					'issue_score': 250,
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
							'url': 'https://i.ytimg.com/vi/sg_Z7kspl6E/maxresdefault.jpg',
						}
					]
				},
				{
					'id': 102,
					'date': "2015-08-15",
					'title': "SBS 드라마 '용팔이' 출연",
					'category': '미디어',
					'issue_score': 150,
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
							'url': 'http://www.fashionn.com/files/board/2015/image/p1a0ridlphkkvlevf7r1rbptpi1.jpg',
						}
					]
				},
				{
					'id': 103,
					'date': "2013-01-01",
					'title': "김태희-비 열애",
					'category': '연예',
					'issue_score': 230,
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
							'url': 'http://cfile1.uf.tistory.com/image/191E223650E2E5F642A8D9',
						}
					]
				},
				{
					'id': 104,
					'date': "2009-10-14",
					'title': "KBS 드라마 '아이리스' 출연",
					'category': '미디어',
					'issue_score': 190,
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
							'url': 'https://encrypted-tbn2.gstatic.com/images?q=tbn:ANd9GcT1Ur3zsQjMWFAMSM7CVeoW0CUXdI7RAEiUaARm_KKLtWr56-wmVA',
						}
					]
				},
			],
		}
	}

	@staticmethod
	def get(name) :
		return People.people_data[name]

