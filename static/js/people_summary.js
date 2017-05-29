var peopleSummary = (function(entityId) {

	function closeStatPopup(roleId) {
		$('.stat-' + roleId + ' .stat-evaluate-popup').fadeOut(200);
	}

	function loadStatEvaluation(roleId, successFunc) {
		memento.uapi.get('/entities/' + entityId + '/stats',
			function (result) {
				for (var i = 0; i < result.length; i++) {
					if (result[i].role == roleId) {
						successFunc(result[i].stats);
						break;
					}
				}
			},
			function (result) {
				alert('오류가 발생했습니다');
			}
		);
	}

	return {
		'init': function() {
			$('.stat-evaluate-popup .star-grade-big').on('click', function (event) {
				var poses = [12, 27, 41, 56, 70, 85, 98, 113, 127, 140];
				var correction = 3/2;

				for (var i = 0; i < poses.length; i++) {

					if (event.offsetX < poses[i] * correction) {
						for (var j = 0; j <= 10; j++)
							$(event.currentTarget).removeClass("grade" + j);

						$(event.currentTarget).addClass("grade" + (i + 1));
						$(event.currentTarget).parent().find('input[type=hidden]').val( i+1 );
						break;
					}
				}
			});
		},
		'openStatPopup': function (roleId) {
			if (!memento.getLoginedUser().loggined) {
				sidebar.open();
				return false;
			}
			// TODO: load evaluating info from API Server
			
			$('.stat-' + roleId + ' .stat-evaluate-popup').fadeIn();

			$('.stat-' + roleId + ' .stat-evaluate-popup input[type=hidden]').each(function (index, field) { field.value = "0"; });
			for (var j = 1; j <= 10; j++)
				$('.stat-' + roleId + ' .stat-evaluate-popup .star-grade-big').removeClass("grade" + j);
			$('.stat-' + roleId + ' .stat-evaluate-popup .star-grade-big').addClass("grade0");

			loadStatEvaluation(roleId, function(stats) {
				
				for (var key in stats) {
					var dom = $('.stat-' + roleId + ' .stat-evaluate-popup .star-grade-big.stat-'+key);
					dom.removeClass("grade0");
					dom.addClass("grade" + stats[key]);
					dom.parent().find('input[type=hidden]').val( stats[key] );
				}
			});
		},

		'closeStatPopup': closeStatPopup,

		'loadStatEvaluation': loadStatEvaluation,

		'uploadStatEvaluation': function (roleId, form) {
			var data = [];
			$(form).find('input[type=hidden]').each(function (index, field) {
				data.push( parseInt(field.value) );
			});

			for (var i = 0; i < data.length; i++) {
				if (!data[i]) {
					alert("모든 항목을 평가 해 주세요!");
					return false;
				}
			}

			memento.uapi.put('/entities/' + entityId + '/roles/' + roleId + '/stats',
				data,
				function (result) {
					alert('평가되었습니다!');
					closeStatPopup(roleId);
				},
				function (result) {
					alert('오류가 발생했습니다');
				}
			);
		}
	}

})(entityId);



