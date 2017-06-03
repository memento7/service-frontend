from jikji import render_template, register_view
from models.people import People
from models.event import Event
from models.weekly import WeeklyMemento
from lib.api import PublishAPI

from datetime import datetime, timedelta

@register_view
def home() :

	rank_limit = 12
	now = datetime.now()
	since = now - timedelta(days=2000)


	# Process trendy people
	trendy_people = []
	for entity in PublishAPI.get('/entities/toprank?sinceDate=%s&rankLimit=%d' % (
					since.strftime('%Y-%m-%d'),
					rank_limit)) :
		trendy_people.append( People(**entity) )


	# Process watchable events
	watchable_events = []
	for event in PublishAPI.get('/events/toprank?fromDate=%s&toDate=%s&rankLimit=%d' % (
					since.strftime('%Y-%m-%d'),
					now.strftime('%Y-%m-%d'),
					rank_limit)) :
		watchable_events.append( Event(**event) )

	# Proceess 3years ago
	ago_3year_date = datetime(now.year-3, now.month, now.day)
	tmp = PublishAPI.get('/events/toprank?fromDate=%s&toDate=%s' % (
					ago_3year_date.strftime('%Y-%m-%d'),
					ago_3year_date.strftime('%Y-%m-%d')))
	if len(tmp) :
		event_3years_ago = Event(**tmp[0])
	else :
		event_3years_ago = None


	return render_template('home.html',
		trendy_people=trendy_people,
		watchable_events=watchable_events,

		event_3years_ago_date=ago_3year_date,
		event_3years_ago=event_3years_ago,
		weekly_mementos=[
			WeeklyMemento(date = now - timedelta(days=7)),
			WeeklyMemento(date = now - timedelta(days=14)),
			WeeklyMemento(date = now - timedelta(days=21)),
		]
	)


@register_view
def callback() :
	return render_template('callback.html')


@register_view
def search() :
	return render_template('search.html')