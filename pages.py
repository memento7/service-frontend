from jikji.view import view
from models.people import People


people_names = ['수지', '김태희']
for pn in people_names :
	person = People.get(pn)

	view('people.index').addpage(pn)
	view('people.timeline').addpage(pn)

	for role in person['role_datas'] :
		view('people.role_data').addpage(pn, role)



event_views = ['index', 'images', 'news', 'three_lines', 'comments', 'emotion_wordcloud', 'keyword_wordcloud']

event_pages = [101]
for p in event_pages :
	for v in event_views :
		view('event.' + v).addpage(p)


