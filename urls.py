from jikji.view import view


view('people.index').url_rule 	 = '/people/$1/'
view('people.timeline').url_rule = '/people/$1/timeline/'
view('people.role_data').url_rule = '/people/$1/$2'

view('event.index').url_rule 	 = '/event/$1/'
view('event.images').url_rule 	 = '/event/$1/images/'
view('event.news').url_rule 	 = '/event/$1/news/'
view('event.three_lines').url_rule 	 		 = '/event/$1/3lines/'
view('event.comments').url_rule 	 		 = '/event/$1/comments/'
view('event.emotion_wordcloud').url_rule 	 = '/event/$1/emotion-wordcloud.png'
view('event.keyword_wordcloud').url_rule 	 = '/event/$1/keyword-wordcloud.png'
