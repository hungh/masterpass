/** Change password controller */
mainApp.controller('changepwController', ['$scope', '$http', 'transformReq', function($scope, $http, transformReq){	

	$scope.password = '';
	$scope.newPassword = '';
	$scope.reNewPassword  = '';

	var validateForm = function(){
		var hasError = 'has-error';
		var hasSuccess = 'has-success';
		var failedStat = {stat: false, msg: ''};

		if ($scope.password == ''){			
			$scope.pw_validdated_css = hasError;
			failedStat.msg = 'Please enter your current password.';
			return failedStat;
		}else{
			$scope.pw_validdated_css = hasSuccess;
		}
		if ($scope.newPassword == ''){	
			$scope.newpw_validdated_css = hasError;
			failedStat.msg = 'Please enter your new password.';
			return failedStat;
		}else{
			$scope.newpw_validdated_css = hasSuccess;
		} 

		if ($scope.reNewPassword == '') {			
			$scope.renewpw_validdated_css = hasError;
			failedStat.msg = 'Please repeat your new password.';
			return failedStat;
		}else{
			$scope.renewpw_validdated_css = hasSuccess;
		}

		if ($scope.newPassword != $scope.reNewPassword){
			failedStat.msg = 'Your passwords don\'t match.';
			return failedStat;
		}
		return {stat:true, msg:''};
	}

	$scope.changePassword = function(){		
		var statusObj = validateForm();
		if (!statusObj.stat ){
			$scope.changePwError = statusObj.msg;
			return;
		}
		$http({
			    method: 'POST',
			    url: '/user/changepw',
			    transformRequest: transformReq,
			    data: {password: $scope.password, new_password: $scope.newPassword},
			    headers: glb_formHeader
			}).success(function(status){			
				$scope.changePwError = status;
			}).error(function(err_msg){
				$scope.changePwError = err_msg;
			});			
	};
}]);
