from jikji.view import render_template, view
from models.people import People

@view
def home() :

	return render_template('home.html',
		people= People._instances
	)