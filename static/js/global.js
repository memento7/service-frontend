var memento = (function () {
	/* 
	 * Memento front-end global vars and functions
	 */

	//var AUTH_BASE = 'https://auth.memento.live';
	var AUTH_BASE = 'https://base.memento.live/auth';
	var API_BASE = 'https://uapi.memento.live';

	var loginedUser = {
		'loggined': false,
		'favorites': [],
	};
	var loginCallbacks = [];

	function callAPI(method, api, sucessCallback) {
		$.ajax(API_BASE + api, {
			method: method,
			crossDomain: true,
			crossOrigin: false,
			success: sucessCallback,
			xhrFields: {
				withCredentials: true
			}
		});
	}

	function updateLoginSession() {
		callAPI('GET', '/me', function (result) {
			loginedUser = result;
			loginedUser.loggined = true;

			console.log(result);

			callAPI('GET', '/me/favorites', function (result2) {
				console.log(result2);
				loginedUser.favorites = result2;

				for (var i = 0; i < loginCallbacks.length; i++)
					loginCallbacks[i](loginedUser);
			});
		});
	}

	return {
		'callAPI': callAPI,
		'updateLoginSession': updateLoginSession,

		'getLoginedUser': function() {
			return loginedUser
		},

		'login': function (type) {
			location.href = AUTH_BASE + '/' + type// + '?redirect=' + encodeURI(location.href);
		},

		'registerLoginCallback': function(func) {
			loginCallbacks.push(func);
		},
	};

})();


