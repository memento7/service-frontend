from jikji import render_template, register_view
from jikji.view import PageGroup, Page
from models.people import People
from lib import functions
from lib.api import PublishAPI

from datetime import datetime, timedelta



def get_trend_data(name) :
	import requests, json

	keyword = name
	url = 'http://datalab.naver.com/qcHash.naver'

	today = datetime.now()
	
	data = {
	    'qcType': 'N',
	    'queryGroups': '%s__SZLIG__%s' % (name, keyword),
	#   'startDate': (today - timedelta(days=365*4)).strftime('%Y%m%d'),
	    'startDate': '20160101',
	    'endDate': today.strftime('%Y%m%d'),
	    'timeUnit': 'date',
	}

	r = requests.post(
		url = url,
		data = data,
		headers={
			'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
			'Origin': 'http://datalab.naver.com',
			'Referer': 'http://datalab.naver.com/',
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
			'X-Requested-With': 'XMLHttpRequest',
		}
	)
	
	data = json.loads(r.text)
	hashKey = data['hashKey']
	
	url = 'http://datalab.naver.com/keyword/trendResult.naver?hashKey=' + hashKey
	r = requests.get(url)
	html = r.text
	html = html.split('<div id="graph_data" style="display:none">')[1].split('</div>')[0]
	
	d = json.loads(html)
	gdata = d[0]['data']
	# gdata = data['result'][0]['data']
	
	result = []
	max_value = 100
	MERGE_CNT = 5

	for index, d in enumerate(gdata) :
		if index % MERGE_CNT == (MERGE_CNT-1) :
			value = 0
			for i in range(-MERGE_CNT + 1, 1) :
				value += int(gdata[index+i]['value'])

			max_value = max(max_value, value)
			period = gdata[index-int(MERGE_CNT/2)]['period']

			result.append({
				'value': value,
				'period': datetime.strptime(period, '%Y%m%d'),
				'index': int(index / MERGE_CNT),
			})

	for d in result :
		d['value'] *= (75 / max_value)

	return result




class PeoplePageGroup(PageGroup) :

	def __init__(self, model) :
		self.model = model
		self.id = model.id


	def getpages(self) :
		pages = [
			Page(self.index, params=self),
			Page(self.timeline, params=self),
			Page(self.inmac, params=self),
			Page(self.images, params=self),
			Page(self.quotations, params=self),
		]

		# for role in self.model.roles.values() :
		# 	if role['data']['stats'] :
		# 		pages.append( Page(self.role_data, params=(self, role['name'])) )

		return pages



	@register_view
	def index(self) :
		trend_graph = get_trend_data(self.model.nickname)

		# Process trends
		sorted_trend = sorted(trend_graph, key=lambda d: d['value'], reverse=True)
		top_trend_graph = sorted_trend[0:4] # 전체 그래프중 가장 높은 4개 날짜

		top_trends = {}
		used_events = {}

		events = sorted(self.model.events, key=lambda e: e.issue_data.issue_score)

		for event in events :
			for index, tt in enumerate(top_trend_graph) :
				# Similar date
				if -15 <= (tt['period'] - event.date).days <= 15 :
					if index not in top_trends or top_trends[index]['event'].issue_data.issue_score < event.issue_data.issue_score : 
						# Update
						if event.id in used_events :
							continue

						if index in top_trends :
							used_events[ top_trends[index]['event'].id ] = False

						top_trends[index] = {
							'event': event,
							'graph_data': tt,
						}
						
						used_events[event.id] = True


		return render_template('people_magazine/summary.html',
			page='summary',
			person = self.model,
			trend_graph = trend_graph,
			top_trends = top_trends,
		)


	@register_view
	def timeline(self) :
		return render_template('people_magazine/timeline.html',
			page='timeline',
			person = self.model,
			timelines = self.model.get_timelines(),
		)

	@register_view
	def inmac(self) :
		return render_template('people_magazine/inmac.html',
			page='inmac',
			person = self.model,
		)

	@register_view
	def images(self) :
		return render_template('people_magazine/images.html',
			page='images',
			person = self.model,
		)

	@register_view
	def quotations(self) :
		return render_template('people_magazine/quotations.html',
			page='quotations',
			person = self.model,
		)

	# @register_view
	# def role_data(self, rolename) :		
	# 	return render_template('people_magazine/role_data.html',
	# 		page='role_data',
	# 		person = self.model,
	# 		current_role = self.model.get_role(name=rolename),
	# 	)


	def after_published(self, success_pages, errors, ignored_pages) :
		if len(errors) == 0 :
			PublishAPI.enqueue_entity_published(self.id)


