//var AUTH_BASE = 'https://auth.memento.live';
var AUTH_BASE = 'https://base.memento.live/auth';
var API_BASE = 'https://uapi.memento.live';

var sidebarTemplate;
var loginedUser;

function renderSidemenu() {
	var template = Handlebars.compile(sidebarTemplate);
	
	$('#global-sidebar').html(template({
		'user': loginedUser,
	}));

	$('aside.sidebar')
		.sidebar({side: 'right'})
		.show();
}

function updateLoginSession() {
	$.ajax(API_BASE + '/me', {
		method: 'GET',
		crossDomain: true,
		success: function(result) {
			loginedUser = result;
			renderSidemenu();
		},
		error: function(e) {

		},
		xhrFields: {
			withCredentials: true
		}
	});
}

function openSidemenu() {
	$('aside.sidebar').trigger('sidebar:open');
	$('#mask').fadeIn();

	$('#mask').one('click', function() {
		$('aside.sidebar').trigger('sidebar:close');
		$('#mask').fadeOut();
	});
}

function login(type) {
	location.href = AUTH_BASE + '/' + type// + '?redirect=' + encodeURI(location.href);
}


$(window).ready(function () {
	$.get('/templates/sidebar.html', function (result) {
		sidebarTemplate = result;

		$('header .menu-bar').click(function(event) {
			openSidemenu();
		});

		renderSidemenu();
		updateLoginSession();
	});
});

