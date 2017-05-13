from jikji import Jikji
from jikji.publisher import Publisher, LocalPublisher, S3Publisher

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
