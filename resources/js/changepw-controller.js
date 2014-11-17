/** Change password controller */
angular.module('changepw', [])
	.controller('changepwController', ['$scope', '$http', '$window', function($scope, $http, $window){	

	$scope.password = '';
	$scope.newPassword = '';
	$scope.reNewPassword  = '';


	$scope.changePassword = function(){		
		var hasError = 'has-error';
		var hasSuccess = 'has-success';
		if ($scope.password == ''){
			$window.alert('missing password');
			$scope.pw_validdated_css = hasError;
		}else{
			$scope.pw_validdated_css = hasSuccess;
		}
		if ($scope.newPassword == ''){
			$scope.newpw_validdated_css = hasError;
		}else{
			$scope.newpw_validdated_css = hasSuccess;
		} 

		if ($scope.reNewPassword == '') {
			$scope.renewpw_validdated_css = hasError;
		}else{
			$scope.renewpw_validdated_css = hasSuccess;
		}
	};
}]);