var peopleImages = (function(entityId) {
	
	function init() {
		var grid = new Minigrid({
			container: 'ul.image-container',
			item: 'ul.image-container li',
			gutter: 8
		});

		$(window).on('resize', function () {
			grid.mount();
		});
		$(window).on('load', function() {
			grid.mount();
		})
		grid.mount();

		loadMyLikes();
	}

	function loadMyLikes() {
		memento.uapi.get('/entities/' + entityId + '/images',
			function (result) {
				for (var i = 0; i < result.length; i++) {
					var imageId = result[i].image_id;
					if (result[i].action == 'LIKE') {
						$('#image-' + imageId).find('button').addClass('enabled');
						
						// tmp
						// TODO: GET Count from API Server
						var valueDom = $('#image-' + imageId).find('.value');
						valueDom.html( parseInt(valueDom.html()) + 1 );
					}
				}
			},
			function (error) {
			}
		);
	}

	function like(imageId, target) {
		memento.uapi.post('/images/' + imageId +'/actions/like',
			null,
			function (result) {
				$(target).addClass('enabled');

				var valueDom = $(target).find('.value');
				valueDom.html( parseInt(valueDom.html()) + 1 );
			},
			function (error) {
				alert('오류가 발생했습니다');
			}
		);
	}

	function dislike(imageId, target) {
		memento.uapi.delete('/images/' + imageId +'/actions/like',
			function (result) {
				$(target).removeClass('enabled');
				var valueDom = $(target).find('.value');
				valueDom.html( parseInt(valueDom.html()) - 1 );
			},
			function (error) {
				alert('오류가 발생했습니다');
			}
		);
	}
	
	return {
		'init': init,
		'loadMyLikes': loadMyLikes,
		'act': function (imageId, target) {
			if ($(target).hasClass('enabled'))
				dislike(imageId, target);
			else
				like(imageId, target);
		},
		'like': like,
		'dislike': dislike
	}

})(entityId);
