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