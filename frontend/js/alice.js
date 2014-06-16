
var Alice = {

	url_base : "",

	setHost : function(host, port) {
		url_base = 'http://' + host + ":" + port;
	},


	getWeather : function() {
		//$.get( url_base + '/weather/current', null, Callback.onWeather, 'json' );

        $.ajax({
            url: url_base + '/weather/current',
            type: "GET",
            crossDomain: true,
            data: null,
            dataType: "json",
            success: Callback.onWeather
        });
	}
};
