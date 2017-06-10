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
	#since = now - timedelta(days=20)


	# Process trendy people
	trendy_people = []
	for entity in PublishAPI.get('/entities/toprank?sinceDate=%s&rankLimit=%d' % (
					(now - timedelta(days=60)).strftime('%Y-%m-%d'),
					rank_limit)) :
		trendy_people.append( People(**entity) )


	# Process watchable events
	watchable_events = []
	for event_data in PublishAPI.get('/events/toprank?fromDate=%s&toDate=%s&rankLimit=%d' % (
					(now - timedelta(days=20)).strftime('%Y-%m-%d'),
					now.strftime('%Y-%m-%d'),
					18)) :
		event = Event(**event_data)
		if event.repr_image() :
			watchable_events.append( event )
	
	watchable_events = watchable_events[0:9]


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
	return render_template('intro/callback.html')


@register_view
def about() :
	return render_template('intro/about.html')


@register_view
def terms() :
	return render_template('intro/terms.html')


@register_view
def privacy() :
	return render_template('intro/privacy.html')


@register_view
def search() :
	return render_template('search.html')