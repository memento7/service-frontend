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
				# Upload S3
				# TODO
				print('Currently production publish is not supported')
				# for sucesses, errors, ignores, pagegroup in generation_result :
				# 	print( pagegroup )
				# 	if pagegroup :
				# 		print( pagegroup.getpages()[0].view.__dict__ )
				# 	print( sucesses )
				# 	if pagegroup :
				# 		pagegroup.after_published(sucesses, errors, ignores)


			elif 'development' in generator.app.options :
				# Local Publish
				lp = LocalPublisher('/var/www/dev')
				lp.publish(generator, generation_result)



			# Purge Cloudflare Cache
			from lib import functions

			assets_s, assets_f, assets_i, _ = generation_result[-1]
			
			file_groups = []
			for index, pageurl in enumerate(assets_s) :
				if index % 30 == 0 : # Max: 30 files per api call
					file_groups.append([])

				file_groups[-1].append(functions.geturl('assets', pageurl))

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
					json={
						'files': files
					}
				)

				try :
					r.raise_for_status()

				except requests.exceptions.HTTPError as e :
					cprint.error('%s' % e.response.status_code)
					print(e)
				