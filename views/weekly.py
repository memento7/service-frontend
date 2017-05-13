from jikji import render_template, register_view
from models.event import Event
from lib.api import PublishAPI
from datetime import datetime, timedelta
import math

def get_week_bound(date) :
	weekday = date.isoweekday() % 7 # 0(Sun) ~ 6(Sat)
	return date + timedelta(days=-weekday), date + timedelta(days=6-weekday)


def get_week(date) :
	day1 = datetime(date.year, date.month, 1)
	start_date, end_date = get_week_bound(date)
	diff = start_date - day1

	if end_date > datetime.now() :
		return None

	if end_date.month == date.month :
		return date.year, date.month, int(math.ceil(diff.days / 7)) + 1

	else :
		ndate = datetime(end_date.year, end_date.month, end_date.day)
		return ndate.year, ndate.month, 1


@register_view
def this_week() :
	date = datetime.now()  - timedelta(days=7)
	return weekly(*get_week(date))


@register_view
def weekly(year, month, week) :
	date = datetime(year, month, 1 + (week-1) * 7)
	start_date, end_date = get_week_bound(date)

	data = PublishAPI.get('/events/toprank?fromDate=%s&toDate=%s'
		% (start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))
	)
	
	weekly_events = []
	for event in data :
		weekly_events.append( Event(**event) )

	weekly_events.sort(key=lambda d: d.date, reverse=True)

	return render_template('weekly.html',
		year=year,
		month=month,
		week=week,
		start_date=start_date,
		end_date=end_date,
		events=weekly_events,
		next_week=get_week(date + timedelta(days=7)),
		prev_week=get_week(date + timedelta(days=-7)),
	)

