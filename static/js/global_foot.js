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


/* Grid Images */
function resizeGirdImageTiles() {
	var windowWidth = $(window).width();

	if (windowWidth < 300)
		$('.grid-image-tile').css('width', windowWidth - 10);
	else if (windowWidth < 575)
		$('.grid-image-tile').css('width', windowWidth / 2 - 15);
	else if (windowWidth <= 660)
		$('.grid-image-tile').css('width', '180px');
	else
		$('.grid-image-tile').css('width', '210px');

}
resizeGirdImageTiles();
$(window).on('resize', resizeGirdImageTiles);


function openMoreAction(button) {
	var ul = $(button).parent().find('ul');
	ul.show();

	setTimeout(function() {
		$(window).one('click', function(e) {
			ul.hide();
		});
	}, 10);
}


/* Search */
function searchSubmit(form) {
	if (form.q.value) {
		if (searchPage)
			location.hash = '#q=' + encodeURI(form.q.value);
		else
			location.href = baseUrls.main + 'search/#q=' + encodeURI(form.q.value);
	}
	return false;
}