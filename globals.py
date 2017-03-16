def rand_color() :
	import random
	return 'rgb(%s, %s, %s)' % (random.randrange(1, 255), random.randrange(1, 255), random.randrange(1, 255))

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
	if issue_score >= 200 :
		rank, label = 'S', '세간의 관심'
	elif issue_score >= 130 :
		rank, label = 'A', '이슈 오브 이슈'
	elif issue_score >= 80 :
		rank, label = 'B', '세상의 이야기'
	else :
		rank, label = 'C', '이런저런 뉴스'

	return {
		'rank': rank,
		'label': label,
	}

def event_category_id(category) :
	categories = ['연예', '정치', '스포츠', '미디어', '세계']

	# 1: 연예, 2: 정치, ... 의 dict 형태로 만듬
	#d = dict( map( lambda: k, v : (v, k), range(1, len(categories)+1), categories ) )
	#return d[category]
	return chr( categories.index(category) + 97 )



def circular_number(number) :
	cn = ['0', '①','②','③','④','⑤','⑥','⑦','⑧','⑨','⑩','⑪','⑫','⑬','⑭','⑮']
	return cn[number]