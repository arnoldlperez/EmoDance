(function() {
	var video = document.getElementById('video'),
		canvas = document.getElementById('canvas'),
		context = canvas.getContext('2d'),
		photo = document.getElementById('photo'),
		vendorUrl = window.URL || window.webkitURL;

	navigator.getMedia = 	navigator.getUserMedia ||
							navigator.webkitGetUserMedia ||
							navigator.mozGetUserMedia ||
							navigator.msGetUserMedia;

	navigator.getMedia({
		video: true,
		audio: false
	}, function(stream) {
		video.srcObject=stream;
		video.play();
	}, function(error) {
		// An error occured
		// error.code
	});

	document.getElementById('capture').addEventListener('click', function() {
		context.drawImage(video, 0, 0, 400, 300);
		// saveAs(context, "test.png");
		// photo.setAttribute('src', canvas.toDataURL('image/png'));
		var selector = Math.floor(Math.random()*4);
		switch (selector) {
			case 0:
				photo.src="./img/emotion/anger.png";
				break;
			case 1:
				photo.src="./img/emotion/joy.png";
				break;
			case 2:
				photo.src="./img/emotion/sad.png";
				break;
			case 3:
				photo.src="./img/emotion/surprise.png";
				break;
			default:
				photo.src="./img/emotion/joy.png";
				break;
		}
	});

})();