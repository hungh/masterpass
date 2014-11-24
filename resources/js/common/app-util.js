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

var maskText = function(text){	
	var str1 = [];	
	for (var i =0; i < text.length; i++) {  				
		str1.push(String.fromCharCode(  text.charCodeAt(i) + i ) ) ; 		
	}	
	return str1.join("");
};


var unMaskText = function(text){	
	var str1 = [];	
	for (var i =0; i < text.length; i++) {  		
		str1.push (String.fromCharCode(  text.charCodeAt(i) - i ) ) ; 		
	}
	return str1.join("");
};
