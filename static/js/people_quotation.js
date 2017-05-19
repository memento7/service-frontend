var quotations = (function(entityId) {
	/* Resize Quotations
	*/

	var RESIZER_DEFAULT_DEST_HEIGHT = 75;
	var RESIZER_DEFAULT_MINIMUM_TOP = 0;


	function resize(destHeight, minimumTop) {
		if (destHeight == undefined) destHeight = RESIZER_DEFAULT_DEST_HEIGHT;
		if (minimumTop == undefined) minimumTop = RESIZER_DEFAULT_MINIMUM_TOP;

		var quotationTiles = $('.quotation-tile');
		for (var i = 0; i < quotationTiles.length; i++) {
			var quotationTile = $(quotationTiles[i]);

			var quotationText = quotationTile.find('.text');
			var h2 = quotationTile.find('.text h2');

			while (true) {
				if (quotationText.height() + minimumTop > destHeight)
					h2.css("font-size", parseInt(h2.css("font-size")) -1 + 'px');

				else {
					var newTop = (100 - quotationText.height()) / 2;
					newTop = Math.max(newTop, minimumTop);
					quotationText.css("padding-top", newTop + 'px');
					break;
				}
			}
		}
	}

	function render(sort) {
		memento.uapi.get('/entities/' + entityId +'/quotations' + (sort ? '?sort='+sort : ''), function (result) {
			var template = Handlebars.compile( $('#template-quotations').html() );

			$('#quotations-full').html(
				template({
					'quotations': result
				})
			);

			resize();
		});
	}

	function reload(type) {
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

	return {
		'resize': resize,
		'render': render,
		'reload': reload,
		'like': function(quotationId) {
			memento.uapi.post('/entities/' + entityId +'/quotations/' + quotationId + '/like',
				null,
				function (result) {
					var dom = $('#quotation-' + quotationId + ' .like-btn span');
					dom.html( parseInt(dom.html()) + 1 );
				},
				function (result) {
					if (result.responseJSON.code == 'DUPLICATE_KEY')
						alert('이미 추천하셨습니다');
					else
						alert('오류가 발생했습니다');
				}
			);
		},
		'write': function (quotation) {
			memento.uapi.post('/entities/' + entityId +'/quotations',
				quotation,
				function (result) {
					reload(1);
				},
				function (result) {
					alert('오류가 발생했습니다');
				}
			);
		}
	}

})(entityId);