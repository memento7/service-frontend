# people.py

from jikji.view import render_template, view
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
			'startDate': '20120101',
			'endDate': '20170331',
		}
	)
	
	data = json.loads(r.text)
	gdata = data['result'][0]['data']
	result = []
	max_value = 100

	for index, d in enumerate(gdata) :
		if index % 2 == 1 :
			value = int(d['value']) + int(gdata[index-1]['value'])
			max_value = max(max_value, value)

			result.append({
				'value': value,
				'period': d['period'],
				'index': int(index / 2),
			})

	for d in result :
		d['value'] *= (75 / max_value)

	return result


@view
def index(name) :
	context = People.get(name)
	context['trend_graph'] = get_trend_data(name)
	context['People'] = People

	# process trends
	sorted_trend = sorted(context['trend_graph'], key=lambda d: d['value'], reverse=True)
	top_trend_graph = sorted_trend[0:2]

	context['top_trends'] = []

	from datetime import datetime
	for event in context['timeline'] :
		ts = datetime.strptime(event['date'], '%Y-%m-%d').timestamp()

		for tt in top_trend_graph :
			ts2 = datetime.strptime(tt['period'], '%Y%m%d').timestamp()

			# similar date
			if ts2 - 86400 * 12 <= ts <= ts2 + 86400 * 12 :
				context['top_trends'].append( event )
				event['graph_data'] = tt
				event['color'] = globals.rand_color()


	context['top_trends'].sort(key=lambda d: d['date'])

	return render_template('people_magazine/summary.html', context)


@view
def timeline(name) :
	return render_template('people_magazine/timeline.html', People.get(name))


@view
def images(name) :
	return render_template('people_magazine/images.html', People.get(name))

@view
def role_data(name, role_type) :
	data = People.get(name)

	data['role_type'] = role_type
	data['role_data'] = data['role_datas'][role_type]
	data['role_stat_info'] = People.role_stat_info[ role_type ]
	
	return render_template('people_magazine/role_data.html', data)



