# event.py

from jikji.view import render_template, view
from models.event import Event
import globals
import settings


def image2str(image, type='PNG') :
	from io import BytesIO
	virt_file = BytesIO()
	image.save(virt_file, type)
	
	virt_file.seek(0)
	content = virt_file.read()
	virt_file.close()

	return content


def get_wordcloud(data) :
	from wordcloud import WordCloud
	import math

	text = ''
	for e in data :
		text += (e['keyword'] + ' ') * int(math.log(e['weight']+1) * 8)
		

	def custom_color_func(word, font_size, *arg, **kwarg) :
		return globals.rand_color()

	wc = WordCloud(
		background_color = "white",
		font_path = settings.ROOT_PATH + '/fonts/NanumSquareOTFBold.otf',
		color_func = custom_color_func,
		width = 800,
		height = 280,
		max_font_size = 90,
	)
	wc.generate(text)

	image = wc.to_image()
	return image2str(image)


@view
def emotion_wordcloud(event_id) :
	return get_wordcloud(Event.get(event_id)['emotions'])

@view
def keyword_wordcloud(event_id) :
	return get_wordcloud(Event.get(event_id)['keywords'])



@view
def index(event_id) :
	return render_template('event_magazine/summary.html', Event.get(event_id))


@view
def images(event_id) :
	return render_template('event_magazine/images.html', Event.get(event_id))


@view
def news(event_id) :
	return render_template('event_magazine/news.html', Event.get(event_id))

@view
def three_lines(event_id) :
	return render_template('event_magazine/3lines.html', Event.get(event_id))



