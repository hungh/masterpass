/** Change password controller */
angular.module('changepw', [])
	.controller('changepwController', ['$scope', '$http', '$window', function($scope, $http, $window){	

	$scope.password = '';
	$scope.newPassword = '';
	$scope.reNewPassword  = '';

	var validateForm = function(){
		var hasError = 'has-error';
		var hasSuccess = 'has-success';
		if ($scope.password == ''){			
			$scope.pw_validdated_css = hasError;
			return false;
		}else{
			$scope.pw_validdated_css = hasSuccess;
		}
		if ($scope.newPassword == ''){			
			$scope.newpw_validdated_css = hasError;
			return false;
		}else{
			$scope.newpw_validdated_css = hasSuccess;
		} 

		if ($scope.reNewPassword == '') {			
			$scope.renewpw_validdated_css = hasError;
			return false;
		}else{
			$scope.renewpw_validdated_css = hasSuccess;
		}
		return true;
	}

	$scope.changePassword = function(){		
		if (validateForm()){
			$window.alert('ready to change password');
		}
	};
}]);