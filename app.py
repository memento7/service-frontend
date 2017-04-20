from jikji import getview, addpage, addpagegroup
from models.people import People
from models.event import Event
from views.people import PeoplePageGroup
from views.event import EventPageGroup

import requests
import settings


# Config URLs
getview('home.home').url_rule = '/'

getview('people.index').url_rule 	 = '/people/{ id }/'
getview('people.timeline').url_rule  = '/people/{ id }/timeline/'
getview('people.images').url_rule 	 = '/people/{ id }/images/'
getview('people.role_data').url_rule = '/people/{ $1.id }/{ $2 }/'

getview('event.index').url_rule 	 		 = '/event/{ id }/'
getview('event.images').url_rule 			 = '/event/{ id }/images/'
getview('event.news').url_rule 		 		 = '/event/{ id }/news/'
getview('event.three_lines').url_rule 	 	 = '/event/{ id }/3lines/'
getview('event.emotion_wordcloud').url_rule  = '/event/{ id }/emotion-wordcloud.png'
getview('event.keyword_wordcloud').url_rule  = '/event/{ id }/keyword-wordcloud.png'


addpage(view='home.home')


# Get updated entites
new_people = requests.get(settings.API_BASE_URL + '/entities/updated').json()

# Register people to model and view
new_people.append( People.get(70001) ) #가데이터 - 수지
new_people.append( People.get(70002) ) #가데이터 - 김태희

for data in new_people :
	person = People.register(data)
	addpagegroup( PeoplePageGroup(model=person) )



# Get updated events
new_events = requests.get(settings.API_BASE_URL + '/events/updated?size=5').json()
new_events.append( Event.get(80001) ) #가데이터 - 김태희,비 결혼

# Register event to model and view
for data in new_events :
	event = Event.register(data)
	addpagegroup( EventPageGroup(model=event) )


