from jikji.view import render_template, view
from models.people import People

@view
def home() :
	context = {
		'people': People.people_data
	}
	return render_template('home.html', context)