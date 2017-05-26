// Register callback after logined
memento.registerLoginCallback(sidebar.render);

// Update Login Session
memento.updateLoginSession();


// Sidebar loading
$.get(baseUrls.assets + 'templates/sidebar.html', function (result) {
	sidebar.setTemplate(result);
	sidebar.render();
});

$('header .menu-bar').click(function(event) {
	sidebar.open();
});


/* Popup Closing */
$('.popup > .background').on('click', function (e) {
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