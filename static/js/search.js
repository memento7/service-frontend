function searchPeople(keyword, page) {
	var template = Handlebars.compile($('#template-person-tile').html());
	
	if (!page) {
		page = 0;
		$('#people-result .result').html('');
	}

	memento.uapi.get('/entities/search/'+keyword+'?size=5&page='+page, function (result) {
		for (var i = 0; i < result.length; i++) {
			$('#people-result .result').append(template({
				'person': result[i],
				'baseUrls': baseUrls,
				'showMoreBtn': true
			}));
		}
		
		if (result.length == 0) {
			$('#people-result .more-btn').remove();
			
			if (page == 0)
				$('#people-result .result').append('<div class="no-content">검색 결과가 없습니다</div>');

		}else {
			$('#people-result .more-btn').one('click', function () {
				searchPeople(keyword, page+1);
			});
		}
	});
}

function searchEvent(keyword, page) {
	var template = Handlebars.compile($('#template-event-tile').html());
	
	if (!page) {
		page = 0;
		$('#event-result .result').html('');
	}

	memento.uapi.get('/events/search/'+keyword+'?size=5&page='+page+'&sort=issue_score,desc', function (result) {
		$('#event-result .result .more-btn').remove();

		$('#event-result .result').append(template({
			'events': result,
			'baseUrls': baseUrls,
			'showMoreBtn': true
		}));

		if (result.length == 0) {
			$('#event-result .result .more-btn').remove();
			
			if (page == 0)
				$('#event-result .result').append('<div class="no-content">검색 결과가 없습니다</div>');

		}else {
			$('#event-result .result .more-btn').one('click', function () {
				searchEvent(keyword, page+1);
			});
		}
	});
}

$(window).on('hashchange', function(e) {
	var params = parseHash(location.hash);
	searchEvent(params['q']);
	searchPeople(params['q']);
});

function parseHash(hash) {
	if (hash[0] == '#') hash = hash.substr(1);

	var paramList = hash.split("&");
	var params = {};
	for (var i = 0; i < paramList.length; i++) {
		var param = paramList[i];
		var tmp = param.split("=");
		params[ tmp[0] ] = decodeURI(tmp[1]);
	}
	return params;
}


var searchPage = true;
