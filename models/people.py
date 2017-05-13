from lib import functions
from lib.api import PublishAPI

import requests

class People :

	_roleinfo = None
	_instances = {}


	@staticmethod
	def get_roleinfo(key=None) :
		""" Get role info on API Server
		"""
		if not People._roleinfo :
			# If roleinfo is not initialzied, init info
			role_arr = PublishAPI.get('/entities/roles')
			rv = {}

			for role in role_arr :
				rv[role['key']] = role

			People._roleinfo = rv

		# If key, get info by key
		# Else, return all dictionary
		if key :
			return People._roleinfo[key]
		else :
			return People._roleinfo


	@staticmethod
	def register(data) :
		if type(data) == dict :
			instance = People(**data)
		else :
			instance = data

		People._instances[instance.id] = instance
		return instance


	@staticmethod
	def get(id) :
		return People._instances[id]


	
	def __init__(self, id, nickname, realname, role_json={},
				images=[], profile_image=None, events=[], in_one_word=[], status=0,
				created_time=None, updated_time=None, published_time=None, **kwarg):

		from models.event import Event

		self.id = id
		self.nickname = nickname
		self.realname = realname
		self.role_json = role_json

		self.in_one_word = in_one_word
		self.status = status
		self.images = images
		self.profile_image_url = profile_image
		
		self.created_time = created_time
		self.updated_time = updated_time
		self.published_time = published_time

		self.events = []
		for event in events :
			self.events.append( Event(**event) )

		self.init_roles()


	def init_roles(self) :
		""" Init role datas from role_json
		"""
		roles = {}
		stat_counts = 0

		for roleid, value in self.role_json.items() :
			roleinfo = People.get_roleinfo(roleid)

			if not 'data' in value :
				value['data'] = {}

			roles[roleid] = {
				'info': roleinfo,
				'name': roleinfo['name'],
				'data': value['data'],
			}
			role = roles[roleid]

			role['related_entities'] = value.get('related_entities', {})
			stats = role['data'].get('stats', None)


			if stats :
				role['stats2'] = {
					'labels': [functions.l10n(i) for i in stats.keys()],
					'datas': [functions.l10n(i) for i in stats.values()],
				}
				stat_counts += 1

			role['data']['stats'] = stats


		self.roles = roles
		self.stat_counts = stat_counts


	def get_role(self, id=None, name=None) :
		""" Get specific role by id or name
		"""
		if id :
			return self.roles[id]

		elif name :
			for role in self.roles.values() :
				if role['name'] == name :
					return role
			return None

		else :
			return self.roles


	def get_roles(self) :
		""" Get list of role's name visible
		"""
		return [ d['name'] for d in self.roles.values() if d['info']['status'] == 1 ]


	def repr_image(self, css=False) :
		""" Get representative image of person
		"""
		return functions.first_image(self.images, css)


	def profile_image(self, css=False) :
		""" Get profile image of person
		"""
		if getattr(self, 'profile_image_url') :
			return functions.first_image([{'url': self.profile_image_url}], css)

		else :
			return self.repr_image(css)


	def get_timelines(self) :
		""" Get timelines
			Temporarily processed in front-end
		"""
		date_sorting_lambda = lambda d: d.date
		events = sorted(self.events, key=lambda d: d.issue_data.issue_score, reverse=True)
		
		return [
			sorted(events[0:7], key=date_sorting_lambda, reverse=True),
			sorted(events[0:20], key=date_sorting_lambda, reverse=True),
			sorted(events[0:40], key=date_sorting_lambda, reverse=True),
			sorted(events, key=date_sorting_lambda, reverse=True),
		]


	def magazine_url(self) :
		return functions.geturl('people', self.id)



