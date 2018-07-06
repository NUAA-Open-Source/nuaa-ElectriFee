// vkey v1.0 by marco @ tehwebmaster.blogspot.com

function vkey_load(x) {
	document.getElementById('vkey').style.display = 'block';
}

function vkey_unload() {
	document.getElementById('vkey').style.display = 'none';
}

function vkey_add(x) {
	if (typeof vkey_focus != 'undefined') {
		vkey_focus.value = vkey_focus.value + x.innerHTML;
		vkey_focus.focus();
	}
}

function vkey_cap() {
	var links = document.getElementsByTagName('a');
	for (i = 0; i < links.length; i++) {
		if (links[i].className == 'vkey_key') {
			if (links[i].innerHTML == links[i].innerHTML.toLowerCase()) links[i].innerHTML = links[i].innerHTML.toUpperCase();
			else links[i].innerHTML = links[i].innerHTML.toLowerCase();
		}
	}
	vkey_focus.focus();
}


function vkey_bsp() {
	if (typeof vkey_focus != 'undefined') {
		vkey_focus.value = vkey_focus.value.substring(0, vkey_focus.value.length-1);
		vkey_focus.focus();
	}
}

function vkey_cls() {
	if (typeof vkey_focus != 'undefined') {
		vkey_focus.value = '';
		vkey_focus.focus();
	}
}

window.onload = function() {
	var inputs = document.getElementsByTagName('input');
	for (i = 0; i < inputs.length; i++) {
		if (inputs[i].type == 'text' || inputs[i].type == 'password') {
			inputs[i].onfocus = function() {
				vkey_focus = this;
			}
		}
	}
}