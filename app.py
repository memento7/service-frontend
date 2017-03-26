from jikji.view import view
from models.people import People
from models.event import Event
import requests
import settings


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




r = requests.get(settings.API_BASE_URL + '/entities/updated?size=100')
new_people = r.json()

# Generate Pages
#people_names = ['수지', '김태희']

new_people.append( People.get(70001) )
new_people.append( People.get(70002) )

for person in new_people :
	#person = People.get(pn)

	People.register(person['id'], person)

	view('people.index').addpage(person['id'])
	view('people.timeline').addpage(person['id'])
	view('people.images').addpage(person['id'])

	if 'role_datas' in person :
		for role in person['role_datas'] :
			view('people.role_data').addpage(person['id'], role)





r = requests.get(settings.API_BASE_URL + '/events/updated?size=100')
new_events = r.json()


#event_pages = [101]

new_events.append( Event.get( 80001) )

for event in new_events :
	Event.register(event['id'], event)

	for v in ['index', 'images', 'news', 'three_lines', 'emotion_wordcloud', 'keyword_wordcloud'] :
		view('event.' + v).addpage(event['id'])


