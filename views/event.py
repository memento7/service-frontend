# event.py

from jikji.view import render_template, view

event_data = {
	101: {
		'id': 101,
		'date': "2017-01-01",
		'title': "김태희-비 열애끝에 결혼",
		'type': '연예',
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

			
			{
				'title': "슬퍼요",
				'weight': 0.3
			},
			{
				'title': "예뻐요",
				'weight': 0.3
			},
			{
				'title': "황홀해요",
				'weight': 0.2
			},
			{
				'title': "멋져요",
				'weight': 0.2
			},
			{
				'title': "화나요",
				'weight': 0.1
			},
			{
				'title': "수줍어요",
				'weight': 0.1
			},
		],
		'images': [
			{
				'url': 'https://i.ytimg.com/vi/sg_Z7kspl6E/maxresdefault.jpg',
			}
		],
		'related_people': [
			{
				'name': "김태희",
				'roles': ['배우'],
				'images': [
					{
						'url': "https://search.pstatic.net/common?type=o&size=120x150&quality=95&direct=true&src=http%3A%2F%2Fsstatic.naver.net%2Fpeople%2F28%2F201406261348278841.jpg",
						'heart': 0
					}
				],
			},
			{
				'name': "비",
				'real_name': "정지훈",
				'roles': ['가수', '배우'],
				'images': [
					{
						'url': "https://search.pstatic.net/common?type=o&size=120x150&quality=95&direct=true&src=http%3A%2F%2Fsstatic.naver.net%2Fpeople%2F71%2F20170123185015611.jpg",
						'heart': 0
					}
				],
			}
		],
		'realted_news': [
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
	}
}


@view
def wordcloud(event_id) :
	global event_data
	data = event_data[event_id]

	from wordcloud import WordCloud
	text = ''
	for e in data['emotions'] :
		text += (e['title'] + ' ') * int(e['weight'] * 10)

	wc = WordCloud(background_color="white", font_path='~/Library/Fonts/NanumSquareOTFExtraBold.otf')
	wc.generate(text)

	image = wc.to_image()

	from io import BytesIO
	byte_io = BytesIO()
	image.save(byte_io, 'PNG')
	
	byte_io.seek(0)
	content = byte_io.read()
	byte_io.close()

	return content


@view
def index(event_id) :
	global event_data
	data = event_data[event_id]


	return render_template('event_magazine/summary.html', data)

@view
def news(event_id) :
	global event_data
	data = event_data[event_id]

	return render_template('event_magazine/news.html', data)

