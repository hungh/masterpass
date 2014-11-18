/** login controller */

var loginApp = angular.module('login-app', [])
	.controller('loginController', ['$scope', '$http', '$window', 'transformReq', function($scope, $http, $window, transformReq){		

		$scope.login_submit = function(){

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
					$window.alert('Error:' + jsonData.msg);
				}				

			}).error(function(err_msg){
				$window.alert('Error: '+  err_msg);
			});	
		}

		$scope.getAutoComplete = function(bol){
			if (bol === true){
				return "on";
			}
			return "off";			
		}		
	}]);

loginApp.factory('transformReq', glb_postTransformFnc);