var swiper = new Swiper('.swiper-container', {
	pagination: '.swiper-pagination',
	paginationClickable: true
});


// Emotions
(function() {
	var color = d3.scaleOrdinal(d3.schemeCategory10);

	function render(svgId, data) {
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
			.style("fill", function(d) { return color(d.data.title); });

		node.append("text")
			.selectAll("tspan")
			.data(function(d) { return d.data.title.split(/(?=[A-Z][^A-Z])/g); })
			.enter().append("tspan")
			.attr("x", 0)
			.attr("y", function(d, i, nodes) { return 18 + (i - nodes.length / 2 - 0.5) * 13; })
			.text(function(d) { return d });
	}

	var positiveEmotions = [];
	var negativeEmotions = [];

	// TODO: Enhancement

	for (var i=0; i<emotions.length; i++) {
		var posWords = ['사랑', '멋', '놀라', '행복', '공감', '대단', '재밌', '축하', '예쁨', '황홀', '아름']
		for (var j=0; j<posWords.length; j++)
			if (emotions[i].title.indexOf(posWords[j]) != -1) 
				positiveEmotions.push(emotions[i]);

		var negWords = ['부러', '부럽', '나빠', '나쁨', '슬퍼', '무서', '화', '슬픔', '수줍']
		for (var j=0; j<negWords.length; j++)
			if (emotions[i].title.indexOf(negWords[j]) != -1) 
				negativeEmotions.push(emotions[i]);
	}

	render("#emotions-positive", positiveEmotions);
	render("#emotions-negative", negativeEmotions);

})();
