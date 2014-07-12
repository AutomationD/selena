function formatTime(unixTimestamp) {
    var dt = new Date(unixTimestamp * 1000);

    var hours = dt.getHours();
    var minutes = dt.getMinutes();

    if (hours < 10) 
        hours = '0' + hours;

    if (minutes < 10) 
        minutes = '0' + minutes;

    return hours + ":" + minutes;
}

function formatTemp(temperature) {
    if ( temperature == '--' ) {
        return '-- &deg;C';
    }
    var temp = Math.round( temperature * 10 ) / 10;
    return temp.toFixed(1) + ' &deg;C';
}

var Alice = {

    url_base: "",

    setHost: function(host, port) {
        url_base = 'http://' + host + ":" + port;
    },


    getWeather: function() {
        //$.get( url_base + '/weather/current', null, Callback.onWeather, 'json' );

        $.ajax({
            url: url_base + '/weather/current',
            type: "GET",
            crossDomain: true,
            data: null,
            dataType: "json",
            success: function(data, status) {
                if (status === "success") {
                    $("#temperature").html(formatTemp(data.temp));
                    $("#weather2").html(data.weather.descr);
                } else {
                    // TODO :
                }
            },
            error: function(data, status) {
                $("#temperature").html(formatTemp('--'));
                $("#weather2").html('--');
            }
        });

    },

    getForecast: function() {
        $.get( url_base + '/weather/forecast' )
            .done(
                function( data ) {
                    var obj = jQuery.parseJSON(data);
                    var forecast = '<b>Forecast:<br/></b>';
                    var count = obj.length;
                    for (var i=0; i < count; i++) {
                        forecast += formatTime(obj[i].timestamp) + ': ' + formatTemp(obj[i].temp) + ', ' + obj[i].weather.descr + '<br />';
                    }
                    $("#forecast").html(forecast);
                }
            )
            .fail(
                function() {
                    // log("error")
                }
            )
        ;
    }
};