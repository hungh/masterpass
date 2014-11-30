angular.module('reset-app', [])
.service('transformReq', glb_postTransformFnc)
.controller('resetController', ['$scope', '$http', '$window', 'transformReq', function($scope, $http, $window, transformReq){
	$scope.changePassword = function() {
		var sid = getParameterByName('sid', $window);
		if (sid != ''){
			$http({
				method: 'POST',
				url: '/account/update',
				transformRequest: transformReq,			    
			    data: {sid: sid, password: $scope.password, newPassword: $scope.newPassword},
			    headers: glb_formHeader	
			}).success(function(msg){
				$window.alert(msg);
			}).
			error(function(msg){
				$window.alert(msg);
			});
		}
	};
}]);
