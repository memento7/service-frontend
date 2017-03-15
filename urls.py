from jikji.view import view


view('people.index').url_rule 	 = '/people/$1/'
view('people.timeline').url_rule = '/people/$1/timeline/'

view('event.index').url_rule 	 = '/event/$1/'
view('event.news').url_rule 	 = '/event/$1/news/'
view('event.wordcloud').url_rule 	 = '/event/$1/wordcloud.png'
