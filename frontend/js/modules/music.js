function getModule() {
	return {
		name: 'music',
		title: "Music",
		base_url: '',

		content: function() {
			return "<div class='module_content' id='music_content'></div>";
		},

		start : function() {
			this.getNowPlaying();
		},

		update: function() {
			this.getNowPlaying();
		},



		getNowPlaying: function() {
			$.get( this.base_url + '/music/now_playing')
				.done(
					function( data ) {
						$("#music_content").html( data );
					}
				)
			;
		}


	}
}
