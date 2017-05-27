from jikji import Jikji
from jikji import getview, addpage, addpagegroup
from models.people import People
from models.event import Event
from models.weekly import WeeklyMemento
from models import _mockup

from views.people import PeoplePageGroup
from views.event import EventPageGroup
from lib.api import PublishAPI

import requests
import settings
from datetime import datetime, timedelta


""" Config URLs
"""
getview('home.home').url_rule = '/'
getview('home.callback').url_rule = '/callback.html'
getview('home.search').url_rule = '/search/'

getview('people.index').url_rule 	 = '/people/{ id }/'
getview('people.timeline').url_rule  = '/people/{ id }/timeline/'
getview('people.inmac').url_rule  = '/people/{ id }/inmac/'
getview('people.images').url_rule 	 = '/people/{ id }/images/'
getview('people.quotations').url_rule 	 = '/people/{ id }/quotations/'

getview('event.index').url_rule 	 		 = '/event/{ id }/'
getview('event.images').url_rule 			 = '/event/{ id }/images/'
getview('event.news').url_rule 		 		 = '/event/{ id }/news/'
getview('event.three_lines').url_rule 	 	 = '/event/{ id }/3lines/'
getview('event.keyword_wordcloud').url_rule  = '/event/{ id }/keyword-wordcloud.png'

getview('weekly.weekly').url_rule = '/weekly/{$1}.{$2}/{$3}/'
getview('weekly.recent_week').url_rule = '/weekly/'


""" Add pages and pagegroups
"""

addpage(view='home.home')
addpage(view='home.callback')
addpage(view='home.search')


# Mockup data
addpagegroup( PeoplePageGroup( model=People.register(_mockup.person70001) ) ) # 가데이터 - 수지
addpagegroup( PeoplePageGroup( model=People.register(_mockup.person70002) ) ) # 가데이터 - 수지
addpagegroup( EventPageGroup ( model=Event.register(_mockup.event80001) ) ) # 가데이터 - 김태희,비 결혼



# Get updated entites and register pages
page_num = 0
while True :
	result = PublishAPI.get('/entities/updated?page=%d' % page_num)
	if type(result) is not list or len(result) == 0 : break

	for data in result:
		person = People.register(data)
		addpagegroup( PeoplePageGroup( model=person ) )

	if 'pagelimit' in Jikji.getinstance().options :
		break
	page_num += 1



# Get updated events and register pages
page_num = 0
while True :
	result = PublishAPI.get('/events/updated?page=%d' % page_num)
	if type(result) is not list or len(result) == 0 : break

	for data in result:
		event = Event.register(data)
		addpagegroup( EventPageGroup( model=event ) )

	if 'pagelimit' in Jikji.getinstance().options :
		break
	page_num += 1


addpage(view='weekly.recent_week')

# Weekly memento
for d in range(1, 40) :
	today = datetime.now()
	today = datetime(today.year, today.month, today.day)

	year, month, week = WeeklyMemento.get_week( today - timedelta(days=d*7) )
	addpage(view='weekly.weekly', params=(year, month, week))	


