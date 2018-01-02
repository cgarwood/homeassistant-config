var idleTime = 0;

$(document).ready(function() {
	idleTime = 0;
	setInverval(idleIncrement, 1000)
});

function idleIncrement() {
	this.idleTime++;
	console.log(window.location);
	if (this.idleTime > 300) {
		this.idleTime = 0;
		window.location = '/Screensaver?skin=gemini';
	}
}