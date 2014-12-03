/** login controller */
var loginApp = angular.module('login-app', ['ui.bootstrap']);
loginApp.controller('loginController', ['$scope', '$http', '$window', 'transformReq', function($scope, $http, $window, transformReq){		
		
		$scope.login_submit = function(){
			$scope.loginError = "";
			var httpResponse = $http({
			    method: 'POST',
			    url: '/login',
			    transformRequest: transformReq,
			    data: {login: $scope.login, password: $scope.password},
			    headers: glb_formHeader

			}).success(function(jsonData){												
				if (jsonData.stat === true){
					document.location.href= jsonData.msg;	
				}else{
					$scope.loginError = jsonData.msg;
				}				

			}).error(function(err_msg){
				$scope.loginError = err_msg;
			});	
		}

		$scope.getAutoComplete = function(bol){
			if (bol === true){
				return "on";
			}
			return "off";			
		}		
	}]);

loginApp.controller('forgotPasswordController', ['$scope', '$http', '$window', '$modal', function($scope, $http, $window, $modal){
	$scope.resetPasswordPopup = function(){
		$modal.open({
			templateUrl: 'forgotPassword.html',
		    controller: 'modalInstanceFPWController'			  
		});	
	};	
}]);

angular.module('login-app').controller('modalInstanceFPWController', ['$scope', '$http','$window', '$modalInstance', function($scope, $http, $window, $modalInstance){
	$scope.resetPassword = function(userid){
		$http({
			    method: 'GET',
			    url: '/account/reset?uid='+ userid			
			}).success(function(msg){
				$window.alert(msg);
			})
			.error(function(msg){
				$window.alert(msg);
			});

		$modalInstance.dismiss('cancel');
	};

	$scope.cancel = function () {
    	$modalInstance.dismiss('cancel');
  	};

}]);
loginApp.factory('transformReq', glb_postTransformFnc);