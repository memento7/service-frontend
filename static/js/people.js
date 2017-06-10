var peopleMagazine = (function(entityId) {
	
	return {
		'makeStatChart': function (ctx, labels, data) {
			return new Chart(ctx, {
				type: 'radar',
				data: {
					labels: labels,
					datasets: [
						{
							backgroundColor: "rgba(255,99,132,0.2)",
							borderColor: "rgba(255,99,132,1)",
							pointBackgroundColor: "rgba(255,99,132,1)",
							data: data
						},
					]
				},
				options: {
					responsive: false,
					scale: {
						ticks: {
							stepSize: 2.5,
							max: 10,
							min: 0,
							display: false
						}
					},
					legend: {
						display: false
					}
				}
			});
		},
		'setFavorite': function (ajaxCall) {
			function applyView() {
				$('#people-header .favorite').addClass('enabled');
				$('#people-header .favorite .fa')
					.addClass('fa-star')
					.removeClass('fa-star-o');
			}

			if (ajaxCall) {
				memento.uapi.post('/me/favorites/' + entityId, null, function (result) {
					applyView();
					memento.updateLoginSession();
				});

			}else
				applyView();
			
		},

		'cancelFavorite': function (ajaxCall) {
			function applyView() {
				$('#people-header .favorite').removeClass('enabled');
				$('#people-header .favorite .fa')
					.removeClass('fa-star')
					.addClass('fa-star-o');
			}

			if (ajaxCall) {
				memento.uapi.delete('/me/favorites/' + entityId, function (result) {
					applyView();
					memento.updateLoginSession();
				});

			}else
				applyView();
		}
	}

})(entityId);



$(window).ready(function() {
	$('#people-header .favorite').on('click', function (e) {
		if ($(e.currentTarget).hasClass('enabled'))
			peopleMagazine.cancelFavorite(true);
		else
			peopleMagazine.setFavorite(true);
	});

	memento.registerLoginCallback(function(loginedUser) {
		var favoriteNotSelected = true;

		for (var i = 0; i < loginedUser.favorites.length; i++) {
			if (loginedUser.favorites[i].id == entityId) {
				peopleMagazine.setFavorite(false);
				favoriteNotSelected = false;
				break;
			}
		}

		if (favoriteNotSelected)
			peopleMagazine.cancelFavorite(false);
	});
	
});



