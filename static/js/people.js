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