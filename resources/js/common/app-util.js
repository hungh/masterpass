/** common js */
var glb_postTransformFnc =  function(){
	return function transformRequest(obj){
		var str = [];
        for(var p in obj)
        	str.push(encodeURIComponent(p) + "=" + encodeURIComponent(obj[p]));
        return str.join("&");		
	};
};

var glb_formHeader = {'Content-Type': 'application/x-www-form-urlencoded'};

var maskText = function(text, docId){	
	var str1 = [];	
	var inputElem = document.querySelector('#' + docId );
	inputElem.type = 'password';
	for (var i =0; i < text.length; i++) {  				
		str1.push(String.fromCharCode(  text.charCodeAt(i) + (i + 1)* 2 ) ) ; 		
	}	
	return str1.join("");
};


var unMaskText = function(text, docId){	
	var str1 = [];	
	var inputElem = document.querySelector('#' + docId );
	inputElem.type = 'text';
	for (var i =0; i < text.length; i++) {  		
		str1.push (String.fromCharCode(  text.charCodeAt(i) - (i + 1) * 2) ) ; 		
	}
	return str1.join("");
};
