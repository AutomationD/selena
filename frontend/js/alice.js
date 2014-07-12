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
                    $("#temperature").html(data.temp + " C");
                    $("#weather2").html(data.weather.descr);
                } else {
                    // TODO :
                }
            },
            error: function(data, status) {
                $("#temperature").html('-- C');
                $("#weather2").html('--');
            }
        });

    }
};