/*
window.WebFontConfig = {
	custom: {
		families: ['Spoqa Han Sans:100,300,400,500,700'],
		urls: ['https://spoqa.github.io/spoqa-han-sans/css/SpoqaHanSans-kr.css']
	},
	timeout: 60000
};
(function(d) {
	var wf = d.createElement('script'), s = d.scripts[0];
	wf.src = 'https://ajax.googleapis.com/ajax/libs/webfont/1.5.18/webfont.js';
	s.parentNode.insertBefore(wf, s);
})(document);
*/

$(window).ready(function () {
	$('aside.sidemenu')
		.sidebar({side: 'right'})
		.show();

	$('header .menu-bar').click(function(event) {
		$('aside.sidemenu').trigger('sidebar:open');
		$('#mask').fadeIn();

		$('#mask').one('click', function() {
			$('aside.sidemenu').trigger('sidebar:close');
			$('#mask').fadeOut();
		});
	});
});