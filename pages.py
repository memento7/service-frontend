from jikji.view import view


view('people.index').addpage('수지')
view('people.timeline').addpage('수지')

view('people.index').addpage('김태희')
view('people.timeline').addpage('김태희')


event_views = ['index', 'images', 'news', 'three_lines',
			   'comments', 'emotion_wordcloud', 'keyword_wordcloud']

event_pages = [101]
for p in event_pages :
	for v in event_views :
		view('event.' + v).addpage(p)
