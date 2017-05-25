var inmac = (function(entityId) {
	
	var VISJS_OPTIONS = {
		nodes: {
			borderWidth: 2,
			size: 30,
			color: {
				border: '#cdd2d4',
				background: '#ffffff'
			},
			font: {color:'#333'},
			fixed: true
		},
		edges: {
			color: '#b0bfc7',
			scaling: {
				max: 5
			}
		},
		layout: {
			hierarchical: false
		},
		interaction: {
			dragView: false,
			zoomView: false,
			dragView: false,
			selectable: false,
		}
	};

	var network = null;
	var relations = {};
	var relation_list = [];

	var eventTileTemplate;
	var inmacRelationTemplate;


	function draw() {
		var CENTER_POS = { x: 0, y: 0 };

		var nodes = [];
		var edges = [];
		
		// Main
		nodes.push({
			'id': 1,
			'shape': 'circularImage',
			'label': entityData.nickname,
			'image': entityData.profile_image,
			'size': 30,
			'x': CENTER_POS.x,
			'y': CENTER_POS.y
		});

		for (var i = 0; i < relation_list.length; i++) {
			var entity = relation_list[i]['entity'];
			var theta = i / relation_list.length * 2 * Math.PI;

			nodes.push({
				'id': i+2,
				'shape': 'circularImage',
				'label': entity.nickname,
				'image': entity.images[0]['url'],
				'size': 26,
				'x': 120 * Math.cos(theta) + CENTER_POS.x,
				'y': 120 * Math.sin(theta) + CENTER_POS.y
			});
			edges.push({'from': 1, 'to': i+2, 'value': relation_list[i]['weight']});
		}

		// create a network
		var container = document.getElementById('inmac-network');
		network = new vis.Network(container, {nodes: nodes, edges: edges}, VISJS_OPTIONS);

		network.on("click", function (params) {
			var node = this.getNodeAt(params.pointer.DOM);
			if (node && node != 1)
				showRelations(node);
		});
	}

	function showRelations(entityId) {
		if (!eventTileTemplate) eventTileTemplate = Handlebars.compile($('#template-event-tile').html());
		if (!inmacRelationTemplate) inmacRelationTemplate = Handlebars.compile($('#template-inmac-relation').html());
		
		// temp
		$.get('/temp_relations1_2.json', function(result) {
			$('#inmac-relation').html(
				inmacRelationTemplate({
					'person1': entityData,
					'person2': relations[entityId].entity
				})
			).show();

			var eventsHTML = "";
			for (var i in result) {
				var event = result[i];						
				eventsHTML += eventTileTemplate({
					'event': event,
					'baseUrls': baseUrls
				});
			}
			$('#inmac-relation .events').html(eventsHTML);

		});
	}

	return {
		'setRelations': function(data) {
			relation_list = data;
			
			for (var i = 0; i < data.length; i++)
				relations[data[i].entity.id] = data[i];
		},
		'draw': draw,
		'showRelations': showRelations
	}

})(entityId);
