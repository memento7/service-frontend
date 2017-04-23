import os
from jikji.publisher import LocalPublisher
import _security


# Root Path of Application
ROOT_PATH = os.path.dirname(__file__)


# Absolute directory path includes Template files
TEMPLATE_ROOT = ROOT_PATH + '/template'

# Directory that includes Static files (to copied to output)
STATIC_ROOT = ROOT_PATH + '/static'

# Directory that includes View files
VIEW_ROOT = ROOT_PATH + '/views'

# Publisher instance used after generation
PUBLISHER = LocalPublisher(output_root=ROOT_PATH + '/output')



# Scripts that runned on initializing application
INIT_SCRIPTS = (
	ROOT_PATH + '/app.py',
)


# FILTERS = ROOT_PATH + '/filters.py'
GLOBALS = ROOT_PATH + '/globals.py'


# Process Core cnt
PROCESSES = 5



API_BASE_URL = _security.API_BASE_URL
BASIC_AUTH_KEY = _security.BASIC_AUTH_KEY