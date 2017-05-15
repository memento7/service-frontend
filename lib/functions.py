import json
import settings
from jikji import Jikji
from lib.api import ImageAPI


def geturl(module_name='', uri='/') :
	""" Get module url with app option
	"""
	uri = str(uri)

	if uri[0] == '/' : uri = uri[1:]
	if module_name : subdomain = module_name + '.'
	else : 			 subdomain = ''

	if module_name == 'assets' : module_name = None

	app = Jikji.getinstance()

	if 'production' in app.options :
		return 'https://%smemento.live/%s' % (subdomain, uri)

	elif 'development' in app.options :
		subdomain = subdomain.replace('.', '_')
		return 'https://%sdev.memento.live/%s' % (subdomain, uri)

	elif 'local' in app.options :
		base = 'http://%slocal.memento.live:7000' % subdomain

		if module_name :
			return '%s/%s/%s' % (base, module_name, uri)
		else :
			return '%s/%s' % (base, uri)

	else :
		if module_name :
			return '/%s/%s' % (module_name, uri)
		else :
			return '/%s' % (uri)




def json_encode(obj) :
	""" JSON Encode
	"""
	return json.dumps(obj)

def json_decode(obj) :
	""" JSON Decode
	"""
	return json.loads(obj)


def rand_color() :
	""" Get random colors predefined
	"""
	colorsets = [
		'#F44336', #Red
		'#E91E63', #Pink
		'#9C27B0', #Purple
		'#673AB7', #Deep Purple
		'#3F51B5', #Indigo
		'#2196F3', #Blue
		'#0097A7', #Cyan 700
		'#00796B', #Teal 700
		'#43A047', #Green 600
		'#64DD17', #LightGreen
		'#FDD835', #Yellow 600
		'#EF6C00', #Orange 800
		'#795548', #Brown
		'#607D8B', #Blue Grey
	]
	import random
	return colorsets[ random.randrange(0, len(colorsets)) ]


def range_svg_pos(ratio, radius, cx, cy) :
	""" Get position in SVG (used in event-magazine/summary)

		:param ratio: real number (0~1)
		:param radius: radius of circle
		:param cx: x-axis center coordinate
		:param cy: y-axis center coordinate
	"""
	import math
	return "%s, %s" % (
		round(-radius * math.cos(math.pi * ratio), 4) + cx,
		round(-radius * math.sin(math.pi * ratio), 4) + cy,
	)


def iow_size(word) :
	""" Get In-One-Word size

		<TO BE REFACTORED>
	"""
	s = 200 / len(word)
	if s > 33 : s = 33
	if s < 17 : s = 17

	return "%dpx" % int(s)



def circular_number(number) :
	""" Get circular number
	"""
	cn = ['0', '①','②','③','④','⑤','⑥','⑦','⑧','⑨','⑩','⑪','⑫','⑬','⑭','⑮']

	if 0 <= number < len(cn) :	return cn[number]
	else :						return number



def image_url(image, css_mode=False) :
	""" Get image's path with exception handling

	:param images: image object
	:param css: if True, return css-style code
					(ex. background-image: url('my-image.png'))
	"""

	if image is None :		rv = None
	elif type(image) == str :	rv = image
	elif 'path' in image : 	rv = image['path']
	elif 'url' in image : 	rv = image['url']
	else :					rv = None

	if rv is not None :
		rv = ImageAPI.get(rv)
		

	if css_mode :
		if rv is None : return ''
		else : 			return "background-image: url('%s')" % rv
	else :
		return rv


def first_image(images, css_mode=False) :
	""" Get first image's path on list of images with exception handling
	"""

	if not images or len(images) == 0 :
		return image_url(None, css_mode)
	else :
		return image_url(images[0], css_mode)



def fill_zero(string, length=2) :
	""" Put 0 in a space as long as the length
		* Mainly used for displaying time
	"""
	string = str(string)
	
	for i in range(0, length-len(string)) :
		string = '0' + string

	return string



l10n_data = None
def l10n(key) :
	""" Localization
	"""
	global l10n_data
	if not l10n_data :
		# Init l10n data from XML
		import xml.etree.ElementTree as ET
		tree = ET.parse(settings.ROOT_PATH + '/data/l10n.xml')
		root = tree.getroot()

		l10n_data = {}
		for child in root :
			l10n_data[child.get('name')] = child.find('value').text


	if key in l10n_data : 	return l10n_data[key]
	else : 					return key
