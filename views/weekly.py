from jikji import render_template, register_view
from models.weekly import WeeklyMemento
from datetime import datetime, timedelta


@register_view
def recent_week() :
	date = datetime.now()  - timedelta(days=7)
	return weekly(*WeeklyMemento.get_week(date))


@register_view
def weekly(year, month, week) :
	w = WeeklyMemento(year, month, week)

	return render_template('weekly.html',
		year=w.year,
		month=w.month,
		week=w.week,
		start_date=w.start_date,
		end_date=w.end_date,
		events=w.events,
		next_week=w.next_week,
		prev_week=w.prev_week,
	)

