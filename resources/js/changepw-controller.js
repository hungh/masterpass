/** Change password controller */
angular.module('changepw', [])
	.controller('changepwController', ['$scope', '$http', '$window', function($scope, $http, $window){	

	$scope.password = '';
	$scope.newPassword = '';
	$scope.reNewPassword  = '';

	$scope.changePassword = function(){		
		if ($scope.password == ''){
			$window.alert('missing password');
			$scope.pw_validdated_css = 'has-error';
		}else if ($scope.newPassword == ''){
			$scope.newpw_validdated_css = 'has-error';
		} else if ($scope.reNewPassword == '') {
			$scope.renewpw_validdated_css = 'has-error';
		}
	};
}]);