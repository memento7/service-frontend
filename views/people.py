# people.py

from jikji import render_template, register_view
from models.people import People
import globals


def get_trend_data(name) :
	import requests, json

	keyword = name
	url = 'http://ca.datalab.naver.com/ca/step1/process.naver'

	r = requests.post(
		url = url,
		data = {
			'qcType': 'N',
			'queryGroups': '%s__SZLIG__%s' % (name, keyword),
			'startDate': '20130331',
			'endDate': '20170331',
		},
		headers={
			'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36',
			'Referer': 'http://ca.datalab.naver.com/ca/step1.naver?'
		}
	)

	
	data = json.loads(r.text)
	gdata = data['result'][0]['data']
	result = []
	max_value = 100
	MERGE_CNT = 5

	for index, d in enumerate(gdata) :
		if index % MERGE_CNT == (MERGE_CNT-1) :
			value = 0
			for i in range(-MERGE_CNT + 1, 1) :
				value += int(gdata[index+i]['value'])

			max_value = max(max_value, value)

			result.append({
				'value': value,
				'period': gdata[index-int(MERGE_CNT/2)]['period'],
				'index': int(index / MERGE_CNT),
			})

	for d in result :
		d['value'] *= (75 / max_value)

	return result


@register_view
def index(id) :
	person = People.get(id)
	
	trend_graph = get_trend_data(person.nickname)

	# Process trends
	sorted_trend = sorted(trend_graph, key=lambda d: d['value'], reverse=True)
	top_trend_graph = sorted_trend[0:3] # 전체 그래프중 가장 높은 3개 날짜

	top_trends = {}

	from datetime import datetime
	for event in person.events :
		event_timestamp = datetime.strptime(event.date, '%Y-%m-%d %H:%M:%S').timestamp()

		for index, tt in enumerate(top_trend_graph) :
			tt_timestamp = datetime.strptime(tt['period'], '%Y%m%d').timestamp()

			# Similar date
			if tt_timestamp - 86400 * 15 <= event_timestamp <= tt_timestamp + 86400 * 15 :
				
				if index not in top_trends or top_trends[index]['event'].issue_score['score'] < event.issue_score['score'] : 
					# Update
					top_trends[index] = {
						'event': event,
						'graph_data': tt,
						'color': globals.rand_color()
					}


	return render_template('people_magazine/summary.html',
		person=person,
		trend_graph=trend_graph,
		top_trends=top_trends,
		People=People,
	)


@register_view
def timeline(name) :
	person = People.get(name)

	return render_template('people_magazine/timeline.html',
		person=person,
		timelines=person.get_timelines(),
	)


@register_view
def images(name) :
	return render_template('people_magazine/images.html',
		person=People.get(name)
	)

@register_view
def role_data(name, rolename) :
	person = People.get(name)
	
	return render_template('people_magazine/role_data.html',
		person=person,
		current_role=person.get_role(rolename),
	)



