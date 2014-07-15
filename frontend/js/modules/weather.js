function getModule() {
	return {
		name: 'weather',
		title: "Weather",
		base_url: '',

		content: function() {
			return "<div class='module_content' id='weather_content'>" +
			"<div id='weather_temperature'></div><br />" +
			"<div id='weather'></div>" +
			"</div>";
		},

		start : function() {
			this.getWeather();
		},

		update: function() {
			this.getWeather();
		},



		formatTemp : function(temperature) {
			if ( temperature == '--' ) {
				return '<h1>-- &deg;C</h1>';
			}
			var temp = Math.round( temperature * 10 ) / 10;
			return '<h1>' + temp.toFixed(1) + ' &deg;C</h1>';
		},

		getWeather: function() {

			var weatherModule = this;
			$.get( this.base_url + '/weather/current')
				.done(
					function( data ) {
						var obj = jQuery.parseJSON(data);
						$("#weather_temperature").html( weatherModule.formatTemp(obj.temp) );
						$("#weather").html('<h4>' + obj.weather.descr + '</h4>');
					}
				)
			;
		}


	}
}
