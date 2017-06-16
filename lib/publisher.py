from jikji import Jikji
from jikji.publisher import Publisher, LocalPublisher, S3Publisher
from jikji.cprint import cprint
from lib import security

import requests

class MementoPublisher(Publisher) :

		def __init__(self) :
			""" Constructor of Publisher
			"""
			pass
		

		def publish(self, generator, generation_result=None) :
			""" Publish implmentation function
			:param generator: Generator object
			:param generation_result: Result list of generation
			"""

			if 'production' in generator.app.options :
				from views.people import PeoplePageGroup
				from views.event import EventPageGroup

				for sucesses, errors, ignores, pagegroup in generation_result :
					if not pagegroup :
						self.upload_to_production(generator, 'assets', sucesses)
						
					elif type(pagegroup) == PeoplePageGroup :
						self.upload_to_production(generator, 'people', sucesses)

					elif type(pagegroup) == EventPageGroup :
						self.upload_to_production(generator, 'event', sucesses)

					else :
						for page in sucesses :
							if page.find('/weekly') == 0 :
								self.upload_to_production(generator, 'weekly', page)

							else : 
								self.upload_to_production(generator, '@', page)


				# Purge Cloudflare Cache
				from lib import functions

				assets_s, assets_f, assets_i, _ = generation_result[-1]

				purging_urls = []
				for pageurl in assets_s :
					purging_urls.append( functions.geturl('assets', pageurl) )

				self.purge_cloudflare_cache(purging_urls)


			elif 'development' in generator.app.options :
				# Local Publish
				lp = LocalPublisher('/var/www/dev')
				lp.publish(generator, generation_result)

				# Purge Cloudflare Cache
				from lib import functions

				assets_s, assets_f, assets_i, _ = generation_result[-1]

				purging_urls = []
				for pageurl in assets_s :
					purging_urls.append( functions.geturl('assets', pageurl) )

				self.purge_cloudflare_cache(purging_urls)


			# Super method
			Publisher.publish(self, generator, generation_result)



		def upload_to_production(self, generator, subdomain, pages) :
			""" Upload to production server (S3)
			"""
			if type(pages) != list :
				pages = [pages]


			if subdomain == '@' :
				if 'beta' in generator.app.options :
					bucket_name = 'beta.memento.live'
				else :
					bucket_name = 'memento.live'

			else :
				bucket_name = '%s.memento.live' % subdomain

			import boto3, mimetypes
			from jikji.generator import urltopath
			from lib import functions
			s3 = boto3.resource('s3')

			all_urls = []
			for pageurl in pages :
				file = generator.get_tmp_filepath(pageurl)

				if subdomain == '@' :
					pass

				else :
					if pageurl.find(subdomain) == 1 :
						pageurl = pageurl[len(subdomain) + 1 : ]

				object_key = urltopath(pageurl)
				try :
					content_type = mimetypes.guess_type(file)[0]
				except Exception :
					pass

				if not content_type :
					content_type = 'binary/octet-stream'

				cprint.okb('UPLOAD ' + bucket_name + '  ' + object_key)
				s3.Object(bucket_name, object_key).put(
					Body = open(file, 'rb'),
					ACL = 'public-read',
					ContentType = content_type,
				)

				#all_urls.append( functions.geturl(subdomain, pageurl) )
			
			#self.purge_cloudflare_cache(all_urls)



		def purge_cloudflare_cache(self, urls) :
			""" Purge cloudflare cache via cloudflare API
			"""
			file_groups = []
			for index, url in enumerate(urls) :
				if index % 30 == 0 : # Max: 30 files per api call
					file_groups.append([])

				file_groups[-1].append(url)

			for files in file_groups :
				print('Purge caches :')
				print(files)

				r = requests.delete(
					url='https://api.cloudflare.com/client/v4/zones/0d40f90e25cf5c29078f1dd09fcb8baa/purge_cache',
					headers={
						'X-Auth-Key': security.CLOUDFLARE_AUTH['key'],
						'X-Auth-Email': security.CLOUDFLARE_AUTH['email'],
						'Content-Type': 'application/json',
					},
					json={'files': files}
				)
				try :
					r.raise_for_status()

				except requests.exceptions.HTTPError as e :
					cprint.error('%s' % e.response.status_code)
					print(e)

			