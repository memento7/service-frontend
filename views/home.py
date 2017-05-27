from jikji import render_template, register_view
from models.people import People
from models.event import Event
from models.weekly import WeeklyMemento

from datetime import datetime, timedelta

@register_view
def home() :
	now = datetime.now()

	return render_template('home.html',
		trendy_people=People._instances,
		watchable_events=Event._instances,
		event_3years_ago=Event.get(80001),
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