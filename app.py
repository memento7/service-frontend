from jikji.view import view
from models.people import People
from models.event import Event
import requests
import settings


# Config URLs
view('home.home').url_rule = '/'
view('home.home').addpage()

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



# Get updated entites
r = requests.get(settings.API_BASE_URL + '/entities/updated')
new_people = r.json()



# Register people to model and view
new_people.append( People.get(70001) ) #가데이터 - 수지
new_people.append( People.get(70002) ) #가데이터 - 김태희

for data in new_people :
	person = People.register(data)

	view('people.index').addpage(person.id)
	view('people.timeline').addpage(person.id)
	view('people.images').addpage(person.id)

	for role in person.role_json.values() :
		if 'stat_records' in role :
			view('people.role_data').addpage(person.id, role['name'])




# Get updated events
r = requests.get(settings.API_BASE_URL + '/events/updated?size=00')
new_events = r.json()

new_events.append( Event.get(80001) ) #가데이터 - 김태희,비 결혼

# Register event to model and view
for event in new_events :
	Event.register(event['id'], event)

	#for v in ['index', 'images', 'news', 'three_lines', 'emotion_wordcloud', 'keyword_wordcloud'] :
	for v in ['index', 'images', 'news', 'three_lines', 'keyword_wordcloud'] :
		view('event.' + v).addpage(event['id'])

	if event['emotions'] :
		view('event.emotion_wordcloud').addpage(event['id'])


