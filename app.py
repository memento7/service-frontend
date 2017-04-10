from jikji import getview, addpage, addpagegroup
from models.people import People
from models.event import Event
import requests
import settings


# Config URLs
getview('home.home').url_rule = '/'

getview('people.index').url_rule 	 = '/people/$1/'
getview('people.timeline').url_rule  = '/people/$1/timeline/'
getview('people.images').url_rule 	 = '/people/$1/images/'
getview('people.role_data').url_rule = '/people/$1/$2/'

getview('event.index').url_rule 	 = '/event/$1/'
getview('event.images').url_rule 	 = '/event/$1/images/'
getview('event.news').url_rule 		 = '/event/$1/news/'
getview('event.three_lines').url_rule 	 		 = '/event/$1/3lines/'
getview('event.emotion_wordcloud').url_rule 	 = '/event/$1/emotion-wordcloud.png'
getview('event.keyword_wordcloud').url_rule 	 = '/event/$1/keyword-wordcloud.png'


addpage(view='home.home')


# Get updated entites
new_people = requests.get(settings.API_BASE_URL + '/entities/updated').json()


# Register people to model and view
new_people.append( People.get(70001) ) #가데이터 - 수지
new_people.append( People.get(70002) ) #가데이터 - 김태희

for data in new_people :
	person = People.register(data)

	addpage(view='people.index', params=(person.id, ))
	addpage(view='people.timeline', params=(person.id, ))
	addpage(view='people.images', params=(person.id, ))

	for role in person.role_json.values() :
		if 'stat_records' in role :
			addpage(view='people.role_data', params=(person.id, role['name']))




# Get updated events
new_events = requests.get(settings.API_BASE_URL + '/events/updated?size=50').json()


new_events.append( Event.get(80001) ) #가데이터 - 김태희,비 결혼

# Register event to model and view
for data in new_events :
	event = Event.register(data)

	for v in ['index', 'images', 'news', 'three_lines', 'keyword_wordcloud'] :
		addpage(view='event.'+v, params=(event.id, ))

	if event.emotions :
		addpage(view='event.emotion_wordcloud', params=(event.id, ))
		#view('event.emotion_wordcloud').addpage(event.id)


