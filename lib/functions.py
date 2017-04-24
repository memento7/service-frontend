def rand_color() :
	colorsets = [
		'#F44336', #Red
		'#E91E63', #Pink
		'#9C27B0', #Purple
		'#673AB7', #Deep Purple
		'#3F51B5', #Indigo
		'#2196F3', #Blue
		'#0097A7', #Cyan 700
		'#00796B', #Teal 700
		'#43A047', #Green 600
		'#64DD17', #LightGreen
		'#FDD835', #Yellow 600
		'#EF6C00', #Orange 800
		'#795548', #Brown
		'#607D8B', #Blue Grey
	]
	import random
	return colorsets[ random.randrange(0, len(colorsets)) ]

	#return 'rgb(%s, %s, %s)' % (random.randrange(1, 255), random.randrange(1, 255), random.randrange(1, 255))

def range_svg_pos(ratio, radius, cx, cy) :
	import math
	return "%s, %s" % (
		round(-radius * math.cos(math.pi * ratio), 4) + cx,
		round(-radius * math.sin(math.pi * ratio), 4) + cy,
	)

def iow_size(word) :
	s = 200 / len(word)
	if s > 33 : s = 33
	if s < 17 : s = 17

	return "%dpx" % int(s)


def issue_rank(issue_score) :
	tp = issue_score['top_percentile']

	if tp is None :
		rank, label = '?', '??'
		mention = '오류가 발생했습니다'
	
	elif tp <= 2 :
		rank, label = 'S', '세간의 관심'
		mention = '이 사건도 모르면 간첩이죠! 정말 뜨거웠던 이야기였어요'

	elif tp <= 10 :
		rank, label = 'A', '이슈 오브 이슈'
		mention = '꽤 화제가 많이 된 사건이었어요!'

	elif tp <= 50 :
		rank, label = 'B', '세상의 이야기'
		mention = '꽤 재미있는 소식이었어요'

	else :
		rank, label = 'C', '이런저런 뉴스'
		mention = '이런 소식도 있었네요'

	return {
		'rank': rank,
		'label': label,
		'mention': mention,
	}

def event_category_id(category) :
	categories = ['연예', '정치', '스포츠', '미디어', '세계', '기타']

	# 1: 연예, 2: 정치, ... 의 dict 형태로 만듬
	#d = dict( map( lambda: k, v : (v, k), range(1, len(categories)+1), categories ) )
	#return d[category]
	return chr( categories.index(category) + 97 )



def circular_number(number) :
	cn = ['0', '①','②','③','④','⑤','⑥','⑦','⑧','⑨','⑩','⑪','⑫','⑬','⑭','⑮']

	if 0 <= number < len(cn) :
		return cn[number]
	else :
		return number



def first_image(images, css=False) :
	if not images or len(images) == 0 :
		rv = None
	else :
		rv = images[0]['path']


	if css :
		if rv is None :
			return ''
		else :
			return "background-image: url('%s')" % rv
	else :
		return rv


def l10n(key) :
	d = {
		'roleplay': '배역 소화도',
		'perform': '액션',
		'looks': '외모',
		'stability': '안정감',
		'empathy': '감정연기',

		'emotional': '감정 호소',
		'singability': '가창력',
		'composition': '작곡',
		'dance': '댄스', 

		'drama': '드라마',
		'movie': '영화',
		'album': '앨범',
	}

	if key in d :
		return d[key]
	else :
		return key
