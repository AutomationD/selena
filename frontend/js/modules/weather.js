function getModule() {
	return {
		name: 'weather',
		title: "Weather",
		base_url: '',

		content: function() {
			return "<div class='module_content' id='weather_content'>" +
			"<div id='temperature'></div><br />" +
			"<div id='weather'></div>" +
			"</div>";
		},

		start : function() {
			this.getWeather();
		},


		formatTemp : function(temperature) {
			if ( temperature == '--' ) {
				return '-- &deg;C';
			}
			var temp = Math.round( temperature * 10 ) / 10;
			return temp.toFixed(1) + ' &deg;C';
		},

		getWeather: function() {

			var weatherModule = this;
			$.get( this.base_url + '/weather/current')
				.done(
					function( data ) {
						var obj = jQuery.parseJSON(data);
						$("#temperature").html( weatherModule.formatTemp(obj.temp) );
						$("#weather").html(obj.weather.descr);
					}
				)
			;
		}


	}
}
