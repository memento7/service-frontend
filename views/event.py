from jikji import render_template, register_view
from jikji.view import PageGroup, Page
from models.event import Event

from lib import functions
from lib.api import PublishAPI
import settings


def image2str(image, type='PNG') :
	from io import BytesIO
	virt_file = BytesIO()
	image.save(virt_file, type)
	
	virt_file.seek(0)
	content = virt_file.read()
	virt_file.close()

	return content


def get_wordcloud(data, key='title', multn=1) :
	from wordcloud import WordCloud
	import math

	text = ''
	for e in data :
		text += (e[key] + ' ') * int(math.log( e['weight']*multn + 1 ))
		#text += (e[key] + ' ') * int(e['weight'] / 3)	

	def custom_color_func(word, font_size, *arg, **kwarg) :
		return functions.rand_color()

	wc = WordCloud(
		background_color = "white",
		font_path = settings.ROOT_PATH + '/data/fonts/NanumSquareOTFBold.otf',
		#font_path = settings.ROOT_PATH + '/static/fonts/NanumBarunGothic.otf',
		color_func = custom_color_func,
		width = 800,
		height = 280,
		max_font_size = 90,
	)
	wc.generate(text)

	image = wc.to_image()
	return image2str(image)



class EventPageGroup(PageGroup) :
	def __init__(self, model) :
		self.model = model
		self.id = model.id


	def getpages(self) :
		pages = [
			Page(self.index, params=self),
			Page(self.images, params=self),
			Page(self.news, params=self),
			Page(self.three_lines, params=self),
			Page(self.keyword_wordcloud, params=self),
		]

		return pages


	@register_view
	def index(self) :
		return render_template('event_magazine/summary.html',
			page='summary',
			event=self.model,
		)


	@register_view
	def images(self) :
		return render_template('event_magazine/images.html',
			page='images',
			event=self.model,
		)


	@register_view
	def news(self) :
		return render_template('event_magazine/news.html',
			page='news',
			event=self.model,
		)

	@register_view
	def three_lines(self) :
		return render_template('event_magazine/3lines.html',
			page='3lines',
			event=self.model,
		)


	@register_view
	def keyword_wordcloud(self) :
		return get_wordcloud(self.model.keywords, key='keyword')



	def after_published(self, success_pages, errors, ignored_pages) :
		if len(errors) == 0 :
			PublishAPI.enqueue_event_published(self.id)


