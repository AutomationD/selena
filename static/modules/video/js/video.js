function getModule() {
    return {
        name: 'Video',
        title: "Video",
        base_url: '',

        content: function() {
            return "<div id='result'>test</div>";

            $.getScript("/modules/video/js/janus.js", function(data, textStatus, jqxhr) {
                console.log(data); // Data returned
                console.log(textStatus); // Success
                console.log(jqxhr.status); // 200
                console.log("Load was performed.");
            });

            $.getScript("/modules/video/js/streamingtest.js", function(data, textStatus, jqxhr) {
                console.log(data); // Data returned
                console.log(textStatus); // Success
                console.log(jqxhr.status); // 200
                console.log("Load was performed.");
            });

            $("#result").load("/modules/video/html/testing_load.html", function() {
                alert("Load was performed.");
            });


            // return "<div class='module_content' id='video_content'></div>";
        },

        start: function() {
            this.getVideo();
        },

        update: function() {
            this.getVideo();
        },



        getVideo: function() {
            $.get(this.base_url + '/video/video')
                .done(
                    function(data) {
                        $("#video_content").html('<h3>' + data + '</h3>');
                    }
            );
        }

    }
}