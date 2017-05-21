(function () {
	/* 
	 * Sidebar handling
	 */
	 
	var sidebarTemplate;
	var sidebarOpened = false;

	function renderSidemenu(loginedUser) {
		if (!sidebarTemplate) return;
		var template = Handlebars.compile(sidebarTemplate);
		
		$('#global-sidebar').html(template({
			'user': loginedUser
		}));

		$('aside.sidebar')
			.sidebar({side: 'right'})
			.show();


		// Register listeners
		$('aside.sidebar li.weekly-memento').on('click', function() {
			location.href = baseUrls.weekly;
		});
		$('aside.sidebar li.random-person').on('click', function() {
			memento.uapi.get('/entities/random', function(result) {
				location.href = baseUrls.people + result;
			});
		});
		$('aside.sidebar li.random-event').on('click', function() {
			memento.uapi.get('/events/random', function(result) {
				location.href = baseUrls.event + result;
			});
		});

		if (sidebarOpened) // If already opened, re-open sidebar
			openSidemenu();
	}

	function openSidemenu() {
		$('aside.sidebar').trigger('sidebar:open');
		$('#mask').fadeIn();
		sidebarOpened = true;

		$('#mask').one('click', function() {
			$('aside.sidebar').trigger('sidebar:close');
			$('#mask').fadeOut();
			sidebarOpened = false;
		});
	}
	
	$.get(baseUrls.assets + 'templates/sidebar.html', function (result) {
		sidebarTemplate = result;

		$('header .menu-bar').click(function(event) {
			openSidemenu();
		});

		renderSidemenu(null);
	});


	// Register callback after logined
	memento.registerLoginCallback(renderSidemenu);



	/* Popup Closing */
	$('.popup .background').on('click', function (e) {
		var popup = $(e.currentTarget).parent();

		if (popup.find('button.cancel').length)
			return;
		else
			popup.fadeOut();
	});
	$('.popup button.cancel').on('click', function (e) {
		e.preventDefault();
		$(e.currentTarget).parents('.popup').fadeOut(200);
	});

})();


memento.updateLoginSession();

