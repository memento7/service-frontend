var swiper = new Swiper('.swiper-container', {
	pagination: '.swiper-pagination',
	paginationClickable: true
});

$(window).load(function () {
	var slideHeight = $('.swiper-slide .container').outerHeight(true);

	$('.swiper-wrapper').css('height', slideHeight + 'px');
});

// Emotions
(function() {
	var color = d3.scaleOrdinal(d3.schemeCategory10);

	function render(svgId, data, key) {
		var svg = d3.select(svgId),
			width = $(svgId).width(),
			height = $(svgId).height();

		if (!data.length) {
			svg.append('text')
				.attr("x", width / 2)
				.attr("y", 80)
				.text('데이터가 없습니다');
			return;
		}
		
		var pack = d3.pack()
			.size([width, height])
			.padding(1.5);


		var root = d3.hierarchy({children: data})
			.sum(function(d) { return d.weight; })

		var node = svg.selectAll(".node")
			.data(pack(root).leaves())
			.enter().append("g")
			.attr("class", "node")
			.attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; });

		node.append("circle")
			.attr("r", function(d) { return d.r; })
			.style("fill", function(d) { return color(d.data[key]); });

		node.append("text")
			.selectAll("tspan")
			.data(function(d) { return d.data[key].split(/(?=[A-Z][^A-Z])/g); })
			.enter().append("tspan")
			.attr("x", 0)
			.attr("y", function(d, i, nodes) { return 18 + (i - nodes.length / 2 - 0.5) * 13; })
			.text(function(d) { return d });
	}

	render("#emotions-svg", emotions, 'emotion');

})();
