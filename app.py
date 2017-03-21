from jikji.view import view
from models.people import People

# Config URLs
view('people.index').url_rule 	 = '/people/$1/'
view('people.timeline').url_rule = '/people/$1/timeline/'
view('people.images').url_rule = '/people/$1/images/'
view('people.role_data').url_rule = '/people/$1/$2/'

view('event.index').url_rule 	 = '/event/$1/'
view('event.images').url_rule 	 = '/event/$1/images/'
view('event.news').url_rule 	 = '/event/$1/news/'
view('event.three_lines').url_rule 	 		 = '/event/$1/3lines/'
view('event.emotion_wordcloud').url_rule 	 = '/event/$1/emotion-wordcloud.png'
view('event.keyword_wordcloud').url_rule 	 = '/event/$1/keyword-wordcloud.png'



# Generate Pages
people_names = ['수지', '김태희']
for pn in people_names :
	person = People.get(pn)

	view('people.index').addpage(pn)
	view('people.timeline').addpage(pn)
	view('people.images').addpage(pn)

	for role in person['role_datas'] :
		view('people.role_data').addpage(pn, role)



event_pages = [101]
for p in event_pages :
	for v in ['index', 'images', 'news', 'three_lines', 'emotion_wordcloud', 'keyword_wordcloud'] :
		view('event.' + v).addpage(p)


