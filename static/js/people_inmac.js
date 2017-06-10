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
		// interaction: {
		// 	dragView: false,
		// 	zoomView: false,
		// 	dragView: false,
		// 	selectable: false,
		// }
		interaction: {
			zoomView: false,
		}
	};

	var DEFAULT_IMAGE = 'https://assets-dev.memento.live/images/avatar.png';

	var network = null;
	var relatedEntities = [];
	var socialRelations = {};

	var eventTileTemplate;
	var inmacRelationTemplate;


	function draw() {
		var CENTER_POS = { x: 0, y: 0 };

		var nodes = [];
		var edges = [];
		
		// Main
		nodes.push({
			'id': 0,
			'shape': 'circularImage',
			'label': entityData.nickname,
			'image': entityData.profile_image ? entityData.profile_image : DEFAULT_IMAGE,
			'size': 30,
			'x': CENTER_POS.x,
			'y': CENTER_POS.y
		});

		for (var i = 1; i < relatedEntities.length; i++) {
			var curEntity = relatedEntities[i];

			if (curEntity.id == entityId) continue;

			var theta = i / relatedEntities.length * 2 * Math.PI;
			var imageUrl = (curEntity.images.length) ? curEntity.images[0]['url'] : DEFAULT_IMAGE;

			nodes.push({
				'id': i,
				'shape': 'circularImage',
				'label': curEntity.nickname,
				'image': imageUrl,
				'size': 26,
				'x': 120 * Math.cos(theta) + CENTER_POS.x,
				'y': 120 * Math.sin(theta) + CENTER_POS.y
			});
			edges.push({'from': 0, 'to': i, 'value': 1}); // TODO: weight calc
			//edges.push({'from': 1, 'to': i+2, 'value': relatedEntities[i]['weight']});
		}

		// create a network
		var container = document.getElementById('inmac-network');
		network = new vis.Network(container, {nodes: nodes, edges: edges}, VISJS_OPTIONS);

		network.on("click", function (params) {
			var nodeId = this.getNodeAt(params.pointer.DOM);
			if (nodeId && nodeId != entityId)
				showRelations( relatedEntities[nodeId].id, nodeId );
		});
	}

	function showRelations(withEntityId, nodeId) {
		if (!eventTileTemplate) eventTileTemplate = Handlebars.compile($('#template-event-tile').html());
		if (!inmacRelationTemplate) inmacRelationTemplate = Handlebars.compile($('#template-inmac-relation').html());
		
		memento.uapi.get('/entities/' + entityId +'/events?withEntityId=' + withEntityId, function (result) {

			$('#inmac-relation').html(
				inmacRelationTemplate({
					'person1': entityData,
					'person2': relatedEntities[nodeId],
					'outbound': socialRelations[entityId][withEntityId],
					'inbound': socialRelations[withEntityId][entityId],
					'baseUrls': baseUrls
				})
			).show();

			$('#inmac-relation .events').html(
				eventTileTemplate({
					'events': result,
					'baseUrls': baseUrls
				})
			);
		});
	}

	return {
		'setRelations': function(data) {
			relatedEntities = data.entities;

			socialRelations = {};
			for (var i = 0; i < data.relations.length; i++) {
				var r = data.relations[i];
				var sid = r.source_entity_id;
				var tid = r.target_entity_id;

				if (!socialRelations[sid])
					socialRelations[sid] = {};

				if (!socialRelations[tid])
					socialRelations[tid] = {};

				socialRelations[sid][tid] = {
					'type': r.relation_type,
					'metadata': r.metadata
				}
			}
		},
		'draw': draw,
		'showRelations': showRelations
	}

})(entityId);
