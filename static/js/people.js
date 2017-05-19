function makeStatChart(ctx, labels, data) {
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
}

function setFavorite(ajaxCall) {
	function applyView() {
		$('#people-header .favorite').addClass('enabled');
		$('#people-header .favorite .fa')
			.addClass('fa-star')
			.removeClass('fa-star-o');
	}

	if (ajaxCall) {
		memento.uapi.post('/me/favorites/' + entityId, null, function (result) {
			applyView();
		});

	}else
		applyView();
	
}

function cancelFavorite(ajaxCall) {
	function applyView() {
		$('#people-header .favorite').removeClass('enabled');
		$('#people-header .favorite .fa')
			.removeClass('fa-star')
			.addClass('fa-star-o');
	}

	if (ajaxCall) {
		memento.uapi.delete('/me/favorites/' + entityId, function (result) {
			applyView();
		});

	}else
		applyView();
}


$(window).ready(function() {
	$('#people-header .favorite').on('click', function (e) {
		if ($(e.currentTarget).hasClass('enabled'))
			cancelFavorite(true);
		else
			setFavorite(true);
	});

	memento.registerLoginCallback(function(loginedUser) {
		for (var i = 0; i < loginedUser.favorites.length; i++) {
			if (loginedUser.favorites[i].id == entityId) {
				setFavorite(false);
				break;
			}
		}
	});
	
});



