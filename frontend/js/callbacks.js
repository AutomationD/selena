//
// REST callbacks
//

var Callback = {

	onWeather: function(data, status) {
		// log("Song: " + status + ", data: " + data);
		if ( status === "success" ) {
			updateWeather( jQuery.parseJSON(data) );
		}
		else {
			// TODO :
		}
	}

};
