from jikji import render_template, register_view
from jikji.view import PageGroup, Page
from models.people import People
from lib import functions
from lib.api import PublishAPI

from datetime import datetime, timedelta



def get_trend_data(name) :
	import requests, json

	keyword = name
	url = 'http://ca.datalab.naver.com/ca/step1/process.naver'

	today = datetime.now()

	r = requests.post(
		url = url,
		data = {
			'qcType': 'N',
			'queryGroups': '%s__SZLIG__%s' % (name, keyword),
			'startDate': (today - timedelta(days=365*4)).strftime('%Y%m%d'), #'20130331',
			'endDate': today.strftime('%Y%m%d'),#'20170331',
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
			Page(self.images, params=self),
		]

		for role in self.model.roles.values() :
			if role['data']['stats'] :
				pages.append( Page(self.role_data, params=(self, role['name'])) )

		return pages



	@register_view
	def index(self) :
		trend_graph = get_trend_data(self.model.nickname)

		# Process trends
		sorted_trend = sorted(trend_graph, key=lambda d: d['value'], reverse=True)
		top_trend_graph = sorted_trend[0:3] # 전체 그래프중 가장 높은 3개 날짜

		top_trends = {}

		for event in self.model.events :
			for index, tt in enumerate(top_trend_graph) :
				# Similar date
				if -15 <= (tt['period'] - event.date).days <= 15 :
					if index not in top_trends or top_trends[index]['event'].issue_data.issue_score < event.issue_data.issue_score : 
						# Update
						top_trends[index] = {
							'event': event,
							'graph_data': tt,
						}


		return render_template('people_magazine/summary.html',
			person = self.model,
			trend_graph = trend_graph,
			top_trends = top_trends,
			People = People,
		)


	@register_view
	def timeline(self) :
		return render_template('people_magazine/timeline.html',
			person = self.model,
			timelines = self.model.get_timelines(),
		)


	@register_view
	def images(self) :
		return render_template('people_magazine/images.html',
			person = self.model
		)


	@register_view
	def role_data(self, rolename) :		
		return render_template('people_magazine/role_data.html',
			person = self.model,
			current_role = self.model.get_role(name=rolename),
		)


	def after_published(self, success_pages, errors, ignored_pages) :
		if len(errors) == 0 :
			PublishAPI.enqueue_entity_published(self.id)


