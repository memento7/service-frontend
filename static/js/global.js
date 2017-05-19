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
	var progressCount = 0;

	function decreaseAjaxProgress() {
		progressCount--;
		if (progressCount <= 0)
			$('#global-progress').hide();
	}

	function callAPI(method, api, data, sucessCallback, errorCallback, hideProgressMask) {
		console.log(method, api);

		if (!hideProgressMask) {
			progressCount++;
			$('#global-progress').show();
		}

		var payload = {
			method: method,
			crossDomain: true,
			//crossOrigin: false,
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
			payload.data = data;
			payloadprocessData = false;
			payload.contentType = 'application/json';
			// payload.dataType = 'json';
		}

		$.ajax(API_BASE + api, payload);
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
		}, null, true);
	}

	return {
		'callAPI': callAPI,
		'uapi': {
			'get': function(api, sucessCallback, errorCallback, hideProgressMask) {
				return callAPI('GET', api, null, sucessCallback, errorCallback, hideProgressMask);
			},
			'post': function(api, data, sucessCallback, errorCallback, hideProgressMask) {
				return callAPI('POST', api, data, sucessCallback, errorCallback, hideProgressMask);
			},
			'put': function(api, data, sucessCallback, errorCallback, hideProgressMask) {
				return callAPI('PUT', api, data, sucessCallback, errorCallback, hideProgressMask);
			},
			'delete': function(api, sucessCallback, errorCallback, hideProgressMask) {
				return callAPI('DELETE', api, null, sucessCallback, errorCallback, hideProgressMask);
			}
		},

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


