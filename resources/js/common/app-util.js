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

var toPasswordInp = function(docId){
	var inputElem = document.querySelector('#' + docId );
	inputElem.type = 'password';
};

var toTextInp = function(docId){
	var inputElem = document.querySelector('#' + docId );
	inputElem.type = 'text';
};

var maskText = function(text, docId){	
	var str1 = [];	
	toPasswordInp(docId);
	for (var i =0; i < text.length; i++) {  				
		str1.push(String.fromCharCode(  text.charCodeAt(i) + (i + 1)* 2 ) ) ; 		
	}	
	return str1.join("");
};


var unMaskText = function(text, docId){	
	var str1 = [];	
	toTextInp(docId);
	for (var i =0; i < text.length; i++) {  		
		str1.push (String.fromCharCode(  text.charCodeAt(i) - (i + 1) * 2) ) ; 		
	}
	return str1.join("");
};

/**get parameter value from location */
var getParameterByName = function(name, owindow) {name = name.replace(/[\[]/, "\\[").replace(/[\]]/, "\\]");
    var regex = new RegExp("[\\?&]" + name + "=([^&#]*)"),
        results = regex.exec(owindow.location.search);
    return results === null ? "" : decodeURIComponent(results[1].replace(/\+/g, " "));
}
