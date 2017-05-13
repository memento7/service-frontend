from jikji import getview, addpage, addpagegroup
from models.people import People
from models.event import Event
from models import _mockup
from views.people import PeoplePageGroup
from views.event import EventPageGroup
from views.weekly import get_week
from lib.api import PublishAPI

import requests
import settings
from datetime import datetime, timedelta


""" Config URLs
"""
getview('home.home').url_rule = '/'

getview('people.index').url_rule 	 = '/people/{ id }/'
getview('people.timeline').url_rule  = '/people/{ id }/timeline/'
getview('people.images').url_rule 	 = '/people/{ id }/images/'
#getview('people.role_data').url_rule = '/people/{ $1.id }/{ $2 }/'

getview('event.index').url_rule 	 		 = '/event/{ id }/'
getview('event.images').url_rule 			 = '/event/{ id }/images/'
getview('event.news').url_rule 		 		 = '/event/{ id }/news/'
getview('event.three_lines').url_rule 	 	 = '/event/{ id }/3lines/'
getview('event.keyword_wordcloud').url_rule  = '/event/{ id }/keyword-wordcloud.png'

getview('weekly.weekly').url_rule = '/weekly/{$1}.{$2}/{$3}/'
getview('weekly.this_week').url_rule = '/weekly/'


""" Add pages and pagegroups
"""

addpage(view='home.home')


# Mockup data
addpagegroup( PeoplePageGroup( model=People.register(_mockup.person70001) ) ) # 가데이터 - 수지
addpagegroup( PeoplePageGroup( model=People.register(_mockup.person70002) ) ) # 가데이터 - 수지
addpagegroup( EventPageGroup ( model=Event.register(_mockup.event80001) ) ) # 가데이터 - 김태희,비 결혼



# Get updated entites and register pages
for data in PublishAPI.get('/entities/updated') :
	person = People.register(data)
	addpagegroup( PeoplePageGroup( model=person ) )


# Get updated events and register pages
for data in PublishAPI.get('/events/updated') :
	event = Event.register(data)
	addpagegroup( EventPageGroup( model=event ) )


addpage(view='weekly.this_week')

# Weekly memento
for d in range(1, 20) :
	today = datetime.now()
	today = datetime(today.year, today.month, today.day)

	year, month, week = get_week( today - timedelta(days=d*7) )

	addpage(view='weekly.weekly', params=(year, month, week))	


