from jikji import render_template, register_view
from models.people import People

@register_view
def home() :
	return render_template('home.html',
		people= People._instances
	)