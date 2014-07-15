function getModule() {
	return {
		name: 'facebook',
		title: "Facebook",
		base_url: '',

		content: function() {
			return "<div class='module_content' id='facebook_content'></div>";
		},

		start : function() {
			this.getNewsFeed();
		},

		update: function() {
			this.getNewsFeed();
		},



		getNewsFeed: function() {
			$.get( this.base_url + '/facebook/newsfeed')
				.done(
					function( data ) {
						$("#facebook_content").html( '<h3>' + data + '</h3>');
					}
				)
			;
		}

	}
}
