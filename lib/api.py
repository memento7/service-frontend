from jikji.cprint import cprint
import requests, json
import settings

class RestClient :

	def geturl(cls, api) :
		""" Get full url combining with api and baseurl
		"""
		if api[0] != '/' :
			api = '/' + api

		return cls.BASE_URL + api


	def get_headers(cls, headers=None) :
		""" Return default_headers if param 'headers' is None,
			else return combination of default header and param headers
		"""
		if headers is not None :
			for key, val in cls.HEADERS.items() :
				if key not in headers :
					headers[key] = val
			
			return headers

		else :
			return cls.HEADERS


	def call(cls, method, api, data=None, headers=None, parsejson=True) :
		""" Rest Call to server
		:params
			- method: GET, POST, PUT, or DELETE
			- api: api string appended to baseurl
			- data: url form data (default: None)
			- headers: appending headers in http call
			- parsejson = boolean status of parsing result to json (default: True)
		:return json-parsed object
		"""

		url = RestClient.geturl(cls, api)

		if data is not None :
			data = json.dumps(data)
			

		printing_str = "%s '%s' "% (method.upper(), url)
		cprint.line('%s' % printing_str)

		# Call proper method of requests (maybe GET, POST or ext)
		r = getattr(requests, method.lower())(
			url = url,
			data = data,
			headers = RestClient.get_headers(cls, headers)
		)

		try :
			r.raise_for_status()

		except requests.exceptions.HTTPError as e :
			code = e.response.status_code
			status_msg = requests.status_codes._codes[code][0].replace('_', ' ').upper()

			cprint.error('%s \'%s\' %s %s' % (method.upper(), url, code, status_msg))


		if parsejson and r.text :
			result = r.json()
		else :
			result = r.text
		
		#cprint.okb('\r%s    ' % printing_str)
		return result


class PublishAPI(RestClient) :

	BASE_URL = 'https://api.memento.live/publish'
	HEADERS = {
		'Authorization': settings.BASIC_AUTH_KEY,
		'Content-Type': 'application/json',
	}

	@staticmethod
	def get(api, headers=None) :
		""" GET reqeust to Publish-API-Server
		"""
		return RestClient.call(
			cls = PublishAPI,
			method = 'GET', 
			api = api,
			headers = headers,
		)


	@staticmethod
	def put(api, data=None, headers=None) :
		""" PUT reqeust to Publish-API-Server
		"""
		return RestClient.call(
			cls = PublishAPI,
			method = 'PUT', 
			api = api,
			data = data,
			headers = headers,
		)

	@staticmethod
	def post(api, data=None, headers=None) :
		""" POST reqeust to Publish-API-Server
		"""
		return RestClient.call(
			cls = PublishAPI,
			method = 'POST', 
			api = api,
			data = data,
			headers = headers,
		)

	@staticmethod
	def delete(api, headers=None) :
		""" DELETE reqeust to Publish-API-Server
		"""
		return RestClient.call(
			cls = PublishAPI,
			method = 'DELETE', 
			api = api,
			headers = headers,
		)



	published_events = []
	@staticmethod
	def enqueue_event_published(event_id) :
		""" Set event is published
		"""
		PublishAPI.published_events.append(event_id)


	@staticmethod
	def upload_events_published() :
		cprint.okb('Published Events: ' + str(PublishAPI.published_events))

		if not len(PublishAPI.published_events) :
			return

		PublishAPI.put(
			api = '/events/publish',
			data = PublishAPI.published_events,
		)
		PublishAPI.published_events = []



	published_entities = []
	@staticmethod
	def enqueue_entity_published(entity_id) :
		""" Set entity is published
		"""
		PublishAPI.published_entities.append(entity_id)


	@staticmethod
	def upload_entities_published() :
		cprint.okb('Published Entities: ' + str(PublishAPI.published_entities))

		if not len(PublishAPI.published_entities) :
			return

		PublishAPI.put(
			api = '/entities/publish',
			data = PublishAPI.published_entities,
		)
		PublishAPI.published_entities = []



