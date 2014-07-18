function getModule() {
	return {
		name: 'twitter',
		title: "Twitter",
		base_url: '',

		content: function() {
			return "<div class='module_content' id='twitter_content'></div>";
		},

		start : function() {
			this.getNewsFeed();
		},

		update: function() {
			this.getNewsFeed();
		},



		getNewsFeed: function() {
			$.get( this.base_url + '/twitter/newsfeed')
				.done(
					function( data ) {
						$("#twitter_content").html( '<h3>' + data + '</h3>');
					}
				)
			;
		}

	}
}
