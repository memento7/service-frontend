from jikji.cprint import cprint
import requests
import settings

class PublishAPI :

	BASE_URL = 'https://api.memento.live/publish'
	HEADERS = {
		'Authorization': settings.BASIC_AUTH_KEY,
	}

	@staticmethod
	def get(url) :
		cprint.write('GET %s ...' % url)

		result = requests.get(
			url = PublishAPI.BASE_URL + url,
			headers = PublishAPI.HEADERS,
		).json()

		cprint.ok('\rGET %s    ' % url)

		return result




