from lib.api import PublishAPI
from jikji import Jikji

app = Jikji.getinstance()

if 'production' in app.options :
	PublishAPI.upload_events_published()
	PublishAPI.upload_entities_published()