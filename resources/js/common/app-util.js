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
