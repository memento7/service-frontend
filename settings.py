import os
from jikji.publisher import LocalPublisher, S3Publisher
from lib import security 


# Root Path of Application
ROOT_PATH = os.path.dirname(__file__)


# Absolute directory path includes Template files
TEMPLATE_ROOT = ROOT_PATH + '/template'

# Directory that includes Static files (to copied to output)
STATIC_ROOT = ROOT_PATH + '/static'

# Directory that includes View files
VIEW_ROOT = ROOT_PATH + '/views'

# Publisher instance used after generation
#PUBLISHER = LocalPublisher(output_root=ROOT_PATH + '/output')
PUBLISHER = S3Publisher('beta.memento.live')



# Scripts that runned on initializing application
INIT_SCRIPTS = (
	ROOT_PATH + '/app.py',
)


# FILTERS = ROOT_PATH + '/filters.py'
GLOBALS = ROOT_PATH + '/lib/functions.py'


# Process Core cnt
PROCESSES = 5


BASIC_AUTH_KEY = security.BASIC_AUTH_KEY