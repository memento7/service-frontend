from jikji.view import makeviews, view

makeviews((
	('people.index', '/people/$1/', 'people_magazine/summary.html'),
	('people.timeline', '/people/$1/timeline/', 'people_magazine/timeline.html')
))


view('people.index').addpage('수지')
view('people.timeline').addpage('수지')

view('people.index').addpage('김태희')
view('people.timeline').addpage('김태희')
