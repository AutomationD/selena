function getModule() {
	return {
		name: 'weather',
		title: 'Weather',
		base_url: '',

		content: function() {
			return '<div class="module_content" id="weather_content">' +
			'<div id="weather_temperature"></div>\n' +
			'<div id="weather"></div>\n' +
			'<div id="weather_forecast"></div>\n' +
			'</div>';
		},

		start : function() {
			this.getWeather();
			this.getForecast();
		},

		update: function() {
			this.getWeather();
			this.getForecast();
		},


		/*
		"Private" methods
		*/

		formatTemp : function(temperature) {
			return ( temperature == '--' ? '--' : (Math.round( temperature * 10 ) / 10).toFixed(1) ) + ' &deg;C';
		},

		formatTime : function(unixTimestamp) {
			var dt = new Date(unixTimestamp * 1000);

			var hours = dt.getHours();
			var minutes = dt.getMinutes();

			if (hours < 10)
				hours = '0' + hours;

			if (minutes < 10)
				minutes = '0' + minutes;

			return hours + ":" + minutes;
		},

		getWeather: function() {
			var weatherModule = this;
			$.get( this.base_url + '/weather/current')
				.done(
					function( data ) {
						var obj = jQuery.parseJSON(data);
						$("#weather_temperature").html( '<h1>' + weatherModule.formatTemp(obj.temp) + '</h1>' );
						$("#weather").html('<h4>' + obj.weather.descr + '</h4>');
					}
				)
				.fail(
					function() {
						$("#weather_temperature").html( '<h1>' + weatherModule.formatTemp('--') + '</h1>');
						$("#weather").html('<h4>--</h4>');
					}
				)
			;
		},

		getForecast: function() {
			var weatherModule = this;
			$.get( this.base_url + '/weather/forecast' )
				.done(
					function( data ) {
						var obj = jQuery.parseJSON(data);
						var forecast = '<br/><h3>Forecast:</h3>';
						var count = obj.length;
						for (var i=0; i < count; i++) {
							forecast += '<h4>' + weatherModule.formatTime(obj[i].timestamp) + ': ' + weatherModule.formatTemp(obj[i].temp) + ', ' + obj[i].weather.descr + '</h4>';
						}
						$("#weather_forecast").html(forecast);
					}
				)
				.fail(
					function() {
						$("#weather_forecast").html('<h3>Forecast:</h3><br/>');
					}
				)
			;
		}

	}
}
