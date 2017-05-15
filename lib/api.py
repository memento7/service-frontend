from jikji import Jikji
from jikji.cprint import cprint
from jikji.utils import Cache, AppDataUtil

import requests, json, urllib, hashlib, mimetypes, os
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




class ImageAPI :

	BASE_URL = 'https://images.memento.live'
	cache = Cache(Jikji.getinstance())

	@staticmethod
	def get_hash_url(url, content_type) :
		u = urllib.parse.urlparse(url)
		extension = mimetypes.guess_extension(content_type)

		if not extension :
			extension = '.' + u.path.split('.')[-1]

		return "%s/%s%s" % (
			hashlib.md5( u.netloc.encode() ).hexdigest()[0:10],
			hashlib.md5( url.encode() ).hexdigest(),
			extension,
		)


	@staticmethod
	def make_thumbnail(image_path, output_path, basewidth=300) :
		from PIL import Image

		img = Image.open(image_path)

		wpercent = basewidth / float(img.size[0])
		hsize = int(float(img.size[1]) * float(wpercent))

		img = img.resize(
			(basewidth, hsize),
			Image.ANTIALIAS
		)
		img.save(output_path)


	@staticmethod
	def get(url, size_mode='original') :
		filehash = hashlib.sha1(url.encode()).hexdigest()
		uploaded_image_url = ImageAPI.cache.get(
			key='image_hash/%s' % filehash,
			use_json=False,
			quote=False
		)

		if uploaded_image_url :
			# If cache exists, return image url
			return "%s/%s/%s" % (ImageAPI.BASE_URL, size_mode, uploaded_image_url)


		tmp_img_path = ImageAPI.cache.cachedir + '/image_' + filehash

		filename, headers = urllib.request.urlretrieve(url, tmp_img_path)
		content_type = headers['Content-Type']

		object_key = ImageAPI.get_hash_url(
			url=url,
			content_type=content_type
		)

		if not content_type :
			content_type = mimetypes.guess_type(object_key)[0]

		thumbnail_path = tmp_img_path + '_thumbnail.' + object_key.split('.')[-1]

		# Make Thumbnail
		ImageAPI.make_thumbnail(
			image_path=tmp_img_path,
			output_path=thumbnail_path,
			basewidth=300
		)

		# Upload S3
		import boto3
		s3 = boto3.resource('s3')
		
		s3.Bucket('images.memento.live').upload_file(
			Filename=tmp_img_path,
			Key='original/' + object_key,
			ExtraArgs={
				'ContentType': content_type,
				'ACL':'public-read',
			},
		)

		s3.Bucket('images.memento.live').upload_file(
			Filename=thumbnail_path,
			Key='300x/' + object_key,
			ExtraArgs={
				'ContentType': content_type,
				'ACL':'public-read',
			},
		)


		# Set cache that image is uploaded
		ImageAPI.cache.set(
			key='image_hash/%s' % filehash,
			value=object_key,
			use_json=False,
			quote=False,
		)

		os.remove(tmp_img_path)
		os.remove(thumbnail_path)

		return "%s/%s/%s" % (ImageAPI.BASE_URL, size_mode, object_key)

