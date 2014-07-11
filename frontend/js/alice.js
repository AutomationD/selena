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
                // log("Song: " + status + ", data: " + data);
                if (status === "success") {
                    $("#temperature").html(data.temp);
                    $("#weather2").html(data.weather.descr);
                } else {
                    // TODO :
                }
            }
        });

    }
};