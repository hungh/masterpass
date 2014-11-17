/** login controller */

angular.module('login-app', [])
	.controller('loginController', ['$scope', '$http', function($scope, $http){		
		$scope.login_submit = function(){
			var httpResponse = $http({
			    method: 'POST',
			    url: '/login',
			    transformRequest: function(obj) {
			        var str = [];
			        for(var p in obj)
			        	str.push(encodeURIComponent(p) + "=" + encodeURIComponent(obj[p]));
			        return str.join("&");
			    },
			    data: {login: $scope.login, password: $scope.password},
			    headers: {'Content-Type': 'application/x-www-form-urlencoded'}
			}).success(function(redirect){
				document.location.href= redirect;
			}).error(function(err_msg){
				alert(err_msg);
			});	
		}

		$scope.getAutoComplete = function(bol){
			if (bol === true){
				return "on";
			}
			return "off";			
		}		
	}]);