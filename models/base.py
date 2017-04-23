import requests
import settings

class Model :

	@staticmethod
	def api_get(url) :
		print('GET ' + url)

		return requests.get(
			url=settings.API_BASE_URL + url,
			headers={'Authorization': settings.BASIC_AUTH_KEY}
		).json()
