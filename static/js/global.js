var memento = (function () {
	/* 
	 * Memento front-end global vars and functions
	 */

	var AUTH_BASE = 'https://manage.memento.live/auth';
	var API_BASE = 'https://manage.memento.live/uapi';

	var loginedUser = {
		'loggined': false,
		'id': -1,
		'favorites': [],
	};
	var loginCallbacks = [];
	var progressCount = 0;


	// Local Storage Process
	if (localStorage) {
		var session = localStorage.getItem('session');

		if (session) 
			loginedUser = JSON.parse(session);
	}

	loginCallbacks.push(function(logginedUser) {
		if (localStorage)
			localStorage.setItem('session', JSON.stringify(loginedUser));
	});

	function decreaseAjaxProgress() {
		progressCount--;
		if (progressCount <= 0)
			$('#global-progress').hide();
	}

	function callAPI(method, api, data, sucessCallback, errorCallback, hideProgressMask) {
		//console.log(method, api);

		if (!hideProgressMask) {
			progressCount++;
			$('#global-progress').show();
		}

		var payload = {
			method: method,
			crossDomain: true,
			// crossOrigin: false,
			success: function (result) {
				if (sucessCallback)
					sucessCallback(result);

				if (!hideProgressMask)
					decreaseAjaxProgress();
			},
			error: function(result) {
				if (errorCallback)
					errorCallback(result);

				if (!hideProgressMask)
					decreaseAjaxProgress();
			},
			xhrFields: {
				withCredentials: true
			}
		};

		if (data) {
			payload.data = JSON.stringify(data);
			//payload.processData = false;
			payload.contentType = 'application/json';
			payload.dataType = 'json';
		}

		$.ajax(API_BASE + api, payload);
		return true;
	}

	function updateLoginSession() {
		callAPI('GET', '/me', null, function (result) {
			loginedUser = result;
			loginedUser.loggined = true;
	
			callAPI('GET', '/me/favorites', null, function (result2) {
				loginedUser.favorites = result2;

				for (var i = 0; i < loginCallbacks.length; i++)
					loginCallbacks[i](loginedUser);
			}, null, true);

		}, function(error) {
			// not loggined
			console.log(error);

			loginedUser = {
				'loggined': false,
				'id': -1,
				'favorites': [],
			};

			for (var i = 0; i < loginCallbacks.length; i++)
				loginCallbacks[i](loginedUser);

		}, true);
	}

	return {
		'callAPI': callAPI,
		'uapi': {
			'get': function(api, sucessCallback, errorCallback, hideProgressMask) {
				return callAPI('GET', api, null, sucessCallback, errorCallback, hideProgressMask);
			},
			'post': function(api, data, sucessCallback, errorCallback, hideProgressMask) {
				if (!loginedUser.loggined) {
					sidebar.open();
					return false;
				}
				return callAPI('POST', api, data, sucessCallback, errorCallback, hideProgressMask);
			},
			'put': function(api, data, sucessCallback, errorCallback, hideProgressMask) {
				if (!loginedUser.loggined) {
					sidebar.open();
					return false;
				}
				return callAPI('PUT', api, data, sucessCallback, errorCallback, hideProgressMask);
			},
			'delete': function(api, sucessCallback, errorCallback, hideProgressMask) {
				if (!loginedUser.loggined) {
					sidebar.open();
					return false;
				}
				return callAPI('DELETE', api, null, sucessCallback, errorCallback, hideProgressMask);
			}
		},

		'updateLoginSession': updateLoginSession,

		'getLoginedUser': function() {
			return loginedUser
		},

		'login': function (type) {
			window.open(AUTH_BASE + '/' + type, 'loginPopup', "height=500,width=600,top=100,left=100");

			$(window).one('message', function (e) {
				if (e.originalEvent.data == 'loggined') {
					updateLoginSession();
				}
			});
		},

		'logout': function() {
			window.open('https://base.memento.live/logout', 'logoutPopup', "height=200,width=300");

			$(window).one('message', function (e) {
				updateLoginSession();
			});
		},

		'registerLoginCallback': function(func) {
			loginCallbacks.push(func);
		},
	};

})();

var sidebar = (function () {
	/* 
	 * Sidebar handling
	 */
	 
	var sidebarTemplate;
	var sidebarRendered = false;
	var sidebarOpened = false;

	function render() {
		if (!sidebarTemplate) return;
		var template = Handlebars.compile(sidebarTemplate);
		
		$('#global-sidebar').html(template({
			'user': memento.getLoginedUser(),
			'baseUrls': baseUrls
		}));

		$('aside.sidebar')
			.sidebar({side: 'right'})
			.show();


		// Register listeners
		$('aside.sidebar li.weekly-memento').on('click', function() {
			location.href = baseUrls.weekly;
		});
		$('aside.sidebar li.random-person').on('click', function() {
			memento.uapi.get('/entities/random', function(result) {
				location.href = baseUrls.people + result;
			});
		});
		$('aside.sidebar li.random-event').on('click', function() {
			memento.uapi.get('/events/random', function(result) {
				location.href = baseUrls.event + result;
			});
		});

		sidebarRendered = true;

		if (sidebarOpened) // If already opened, re-open sidebar
			open();
	}

	function open() {
		if (!sidebarRendered) return;

		$('aside.sidebar').trigger('sidebar:open');
		$('#mask').fadeIn();
		sidebarOpened = true;

		$('#mask').one('click', function() {
			$('aside.sidebar').trigger('sidebar:close');
			$('#mask').fadeOut();
			sidebarOpened = false;
		});
	}

	return {
		'setTemplate': function(template) {
			sidebarTemplate = template;
		},
		'render': render,
		'open': open
	};

})();

function image_url(value, css_mode, options) {
	if (value === undefined || value == null) rv = null;
	else if (typeof value == 'string')		  rv = value;
	else if ('path' in value) 				  rv = value['path'];
	else if ('url' in value) 				  rv = value['url'];
	else if ('source_link' in value) 		  rv = value['source_link'];
	else									  rv = null;

	if (css_mode) {
		if (rv == null) return '';
		else  			return "background-image: url('" + rv + "')";
	}else
		return rv;
}

(function() {
	/**
	 * Handlebar helpers
	 */
	Handlebars.registerHelper('if_eq', function(a, b, opts) {
		if (a == b)
			return opts.fn(this);
		else
			return opts.inverse(this);
	});

	Handlebars.registerHelper('if_neq', function(a, b, opts) {
		if (a != b)
			return opts.fn(this);
		else
			return opts.inverse(this);
	});

	Handlebars.registerHelper('replace', function(value, match, replace_string, options) {
		return value.replace(match, replace_string);
	});

	Handlebars.registerHelper('rank', function(value, options) {
		//if (value === undefined)	return '?';
		if (value.top_percentile === undefined) {
			if (value.issue_score >= 1072)				return 's';
			else if (value.issue_score >= 304)		return 'a';
			else if (value.issue_score >= 18)		return 'b';
			else 									return 'c';
		}
		else if (value.top_percentile <= 2 )		return 's';
		else if (value.top_percentile <= 10)		return 'a';
		else if (value.top_percentile <= 50)		return 'b';
		else 						return 'c';
	});


	Handlebars.registerHelper('image_url', image_url);


	Handlebars.registerHelper('profile_image', function(person, css_mode, options) {
		for (var i = 0; i < person.images.length; i++) {
			var image = person.images[i];
			if (image['type'] == 'profile')  {
				return image_url(image, css_mode);
			}
		}
		return image_url(person.images[0], css_mode);
	});

	var ROLE_DICT = {
		'ACTOR': '배우',
		'SINGER': '가수',
		'POLITICIAN': '정치인',
		'SPORTS': '스포츠선수',
		'MODEL': '모델',
		'COMEDIAN': '코미디언',
		'ENTREPRENEUR': '기업인',
		'PUBLIC_FIGURE': '공인'
	};
	Handlebars.registerHelper('roles', function(value, options) {
		var rv = [];
		for (var key in value)
			if (ROLE_DICT[key])
				rv.push(ROLE_DICT[key]);
			
		return rv.join(',');
	});

	Handlebars.registerHelper('random_color', function(options) {
		var colors = ['#F44336','#E91E63','#9C27B0','#673AB7','#3F51B5','#2196F3','#0097A7',
		'#00796B','#43A047','#64DD17','#FDD835','#EF6C00','#795548','#607D8B'];

		return colors[Math.floor( Math.random() * colors.length )];
	});


	Handlebars.registerHelper ('truncate', function (str, len, options) {
		if (str.length > len && str.length > 0) {
			var new_str = str + " ";
			new_str = str.substr (0, len);
			new_str = str.substr (0, new_str.lastIndexOf(" "));
			new_str = (new_str.length > 0) ? new_str : str.substr (0, len);

			return new Handlebars.SafeString ( new_str +'...' ); 
		}
		return str;
	});

})();

