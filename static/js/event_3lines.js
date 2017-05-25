var summeries3lines = (function(eventId) {
	var likeDislikeErrorCallback = function (result) {
		if (result.responseJSON.code == 'DUPLICATE_KEY')
			alert('이미 추천 또는 비추천 하셨습니다');
		else
			alert('오류가 발생했습니다');
	};

	function render(sort) {
		memento.uapi.get('/events/' + eventId +'/summaries_3line' + (sort ? '?sort='+sort : ''), function (result) {
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
	}

	return {
		'render': render,

		'openWritePopup': function() {
			if (!memento.getLoginedUser().loggined) {
				sidebar.open();
				return false;
			}
			$("#three-lines-writing-popup").fadeIn();
			$("#three-lines-writing-popup input[type=text]").val('');
		},

		'upload': function(form) {
			if (!form.line1.value || !form.line2.value || !form.line3.value) {
				alert("내용을 입력 해 주세요");
				return false;
			}
			memento.uapi.post('/events/' + eventId +'/summaries_line',
				[
					form.line1.value,
					form.line2.value,
					form.line3.value
				],
				function (result) {
					reload(1);
				},
				function (result) {
					alert('오류가 발생했습니다');
				}
			);

			$("#three-lines-writing-popup").fadeOut();
		},

		'like': function(summaries3LineId) {
			memento.uapi.post('/events/' + eventId +'/summaries_3line/' + summaries3LineId + '/like',
				null,
				function (result) {
					var dom = $('#summaries3-' + summaries3LineId + ' .like-btn span');
					dom.html( parseInt(dom.html()) + 1 );
				},
				likeDislikeErrorCallback
			);
		},
		'dislike': function(summaries3LineId) {
			memento.uapi.post('/events/' + eventId +'/summaries_3line/' + summaries3LineId + '/dislike',
				null,
				function (result) {
					var dom = $('#summaries3-' + summaries3LineId + ' .dislike-btn span');
					dom.html( parseInt(dom.html()) + 1 );
				},
				likeDislikeErrorCallback
			);
		},
		'reload': function(type) {
			$('.filter-btn').removeClass('active');

			if (type == 0) {
				// 호감순
				$('.filter-btn.type0').addClass('active');
				render();

			}else {
				// 최신순
				$('.filter-btn.type1').addClass('active');
				render('createdTime,desc')
			}
		}
	}

})(eventId);
