var mainApp = angular.module('main', []);

mainApp.controller('loginController', ['$scope', '$http', '$window', 'environService', function($scope, $http, $window, environService){			
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
		$scope.newEnviron = '';
		$scope.environs = []; // TODO: retrieve from database

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
		};

		$scope.getAdminLink = function(){
			if ($scope.current_login == 'root')
				return "/admin.html";
			return '#';
		};
		
		$scope.$on('envChange', function(event, data) {				
        	$scope.environs.push(data);
       	});

		$scope.memus = ['workAreaId', 'changeEnvId'];

       	$scope.switchMenu = function(elemId){
			angular.forEach($scope.memus, function(elementId, index){
				if (elementId == elemId) {
					document.getElementById(elementId).style.display = 'block';		
				}else {
					document.getElementById(elementId).style.display = 'none';
				}
			});
			
		};
    
		
	}]);

mainApp.controller('newEnvionController', ['$scope', '$window', 'environService', function($scope, $window, environService){

	$scope.createNewEnv = function(){			
		if ($scope.newEnviron != ''){						
			environService.push($scope.newEnviron);			 
			$window.alert($scope.newEnviron + ' is created. Please navigate back to Main menu to add user entry.');
		}else{
			$window.alert('Please enter the environment name.');
		}	
		//TODO: SAVE ENV INTO DB		
	};

}]);

mainApp.factory('environService', function($rootScope){		
	return {
		push: function(data){			
			$rootScope.$broadcast('envChange', data);;
		}		
	};
});
