function getModule() {
	return {
		name: 'currrency',
		title: "Currency",
		base_url: '',

		content: function() {
			return "<div class='module_content' id='currency_content'></div>";
		},

		start : function() {
			this.getRates();
		},

		update: function() {
			this.getRates();
		},



		getRates: function() {
			$.get( this.base_url + '/currency/rates')
				.done(
					function( data ) {
						var obj = jQuery.parseJSON(data);
                        var content = '';
                        for (var i = 0; i < obj.length; i++) {
                            content += '<h3>' + obj[i].from + '/' + obj[i].to + ': ' + (Math.round( obj[i].rate * 100) / 100 ).toFixed(2);
                        }
						$("#currency_content").html( content );
					}
				)
			;
		}

	}
}
