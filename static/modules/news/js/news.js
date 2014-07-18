function getModule() {
	return {
		name: 'news',
		title: "News",
		base_url: '',

		content: function() {
			return "<div class='module_content' id='news_content'></div>";
		},

		start : function() {
			this.getLatest();
		},

		update: function() {
			this.getLatest();
		},



		getLatest: function() {
			$.get( this.base_url + '/news/latest')
				.done(
					function( data ) {
						$("#news_content").html( '<h3>' + data + '</h3>');
					}
				)
			;
		}

	}
}
