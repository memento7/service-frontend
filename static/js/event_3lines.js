var summeries3lines = (function(eventId) {
	var likeDislikeErrorCallback = function (result) {
		if (result.responseJSON.code == 'DUPLICATE_KEY')
			alert('이미 추천 또는 비추천 하셨습니다');
		else
			alert('오류가 발생했습니다');
	};

	return {
		'render': function (sort) {
			memento.callAPI('GET', '/events/' + eventId +'/summaries_3line' + (sort ? '?sort='+sort : ''), function (result) {
				Handlebars.registerHelper("inc", function(value, options) {
					return parseInt(value) + 1;
				});

				var template = Handlebars.compile( $('#template-3lines').html() );

				$('#three-lines-full').html(
					template({
						'summaries3lines': result
					})
				);
			});
		},
		'like': function(summaries3LineId) {
			memento.callAPI(
				'POST', '/events/' + eventId +'/summaries_3line/' + summaries3LineId + '/like',
				function (result) {
					var dom = $('#summaries3-' + summaries3LineId + ' .like-btn span');
					dom.html( parseInt(dom.html()) + 1 );
				},
				likeDislikeErrorCallback
			);
		},
		'dislike': function(summaries3LineId) {
			memento.callAPI(
				'POST', '/events/' + eventId +'/summaries_3line/' + summaries3LineId + '/dislike',
				function (result) {
					var dom = $('#summaries3-' + summaries3LineId + ' .dislike-btn span');
					dom.html( parseInt(dom.html()) + 1 );
				},
				likeDislikeErrorCallback
			);
		}
	}

})(eventId);


function reload3lines(type) {
	$('.reload-btn').removeClass('active');

	if (type == 0) {
		// 호감순
		$('.reload-btn.type0').addClass('active');
		summeries3lines.render();

	}else {
		$('.reload-btn.type1').addClass('active');
		// 최신순
		summeries3lines.render('createdTime,desc')
	}
}

summeries3lines.render();