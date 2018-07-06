// simple drag script by marco @ tehwebmaster.blogspot.com

IE = document.all?true:false

function drag_start(x) {
	drag_object = x;
	drag_object.focus();
}

document.onmousedown = function (e) {
	if (!e) var e = window.event;
	if (typeof drag_object != 'undefined') {
		if (IE) {
			xoffset = e.x-drag_object.offsetLeft;
			yoffset = e.y-drag_object.offsetTop;
		}
		else {
			xoffset = e.layerX;
			yoffset = e.layerY;
		}
		return false;
	}
}

document.onselectstart = function () {
	if (typeof drag_object != 'undefined') {
		return false;
	}
}

document.onmousemove = function (e) {
	if (!e) var e = window.event;
	if (typeof drag_object != 'undefined') {
		drag_object.style.left =  e.clientX - xoffset + 'px';
		drag_object.style.top = e.clientY - yoffset + 'px';
	}
}

document.onmouseup = function () {
	delete drag_object;
}