angular.module('main', [])
	.controller('loginController', ['$scope', '$http', function($scope, $http){	
		$scope.environs = ["DEV", "UAT", "STAGE", "PROD"];
		$scope.users = [
			{name: 'hung', env: 'DEV'},
			{name: 'emma', env: 'STAGE'},
			{name: 'tinh', env: 'DEV'},
			{name: 'thao', env: 'UAT'},
			{name: 'ngoc', env: 'DEV'},
			{name: 'tuy', env: 'PROD'},
			{name: 'emily', env: 'STAGE'},
			{name: 'tam', env: 'PROD'},
			{name: 'loan', env: 'STAGE'},
			{name: 'phuong', env: 'UAT'},
		];		

		$scope.currUser = $scope.users[0];
		$scope.currEnviron = 'DEV';

		$http({
			    method: 'GET',
			    url: '/user/current',
		}).success(function(login_uid){
			$scope.current_login = login_uid;
		}).error(function(err_msg){
			alert(err_msg);
		});		

		/** functions */
		$scope.getUserPassword = function(){			
			$scope.currUser.password = "sfas";
		};

		$scope.savePassword = function(){
			alert("Saving...:" + $scope.username  + ";with password:" + $scope.password);
		};

		$scope.updateUserPassword = function(){
			alert('');
		}

		$scope.getAdminLink = function(){
			if ($scope.current_login == 'root')
				return "/admin.html";
			return '#';
		}
	}]);