from jikji import render_template, register_view
from models.people import People
from models.event import Event


@register_view
def home() :
	return render_template('home.html',
		people=People._instances,
		events=Event._instances,
	)

@register_view
def search() :
	return render_template('search.html')