var mainApp = angular.module('main', []);

mainApp.controller('loginController', ['$scope', '$http', '$window', 'environService', 'transformReq',
	 function($scope, $http, $window, environService, transformReq){			
		$scope.users = [];		
		$scope.currUser = $scope.users[0];
		$scope.currEnviron = 'DEV';
		$scope.newEnviron = '';
		$scope.environs = []; 

		var httpCall = function(method, urlStr, postData, callback, transformReq){
			if(method == 'GET'){
				$http({
			    	method: 'GET',
			    	url: urlStr,
				}).success(function(data){
					callback.call(this, data);
				}).error(function(err_msg){
					$window.alert('Error:' + err_msg);
				});			
			}else if (method == 'POST'){
				$http({
				    method: 'POST',
				    url: urlStr,
				    transformRequest: transformReq,			    
				    data: postData,
				    headers: glb_formHeader				    
				}).success(function(data){
					callback.call(this, data)
				}).error(function(err_msg){
				  	$window.alert('Error:' + err_msg);
				});
			}		
		};

		httpCall('GET', '/env/get', {}, function(data){
			$scope.environs = data;
		});

		httpCall('GET', '/user/current', {}, function(data){
			$scope.current_login = data;
		});

		httpCall('POST', '/pws/pwsowner', {}, function(data){
			if (data.stat){
				$scope.users = data.msg;
			}else {
				$window.alert(data.msg);
			}
		}, transformReq);

		/** functions */
		$scope.getUserPassword = function(){			
			if(!$scope.currUser || !$scope.currUser.login || !$scope.currUser.env_name ){
				$window.alert('Please select an entry from drop down');
				return;
			}
			httpCall('POST', '/pws/get', {user: $scope.currUser.login, env: $scope.currUser.env_name}, function(data){
				if (data.stat){
					$scope.currUser.password = data.msg;
				}else {
					$window.alert(data.msg);
				}
			}, transformReq);	
		};

		$scope.savePassword = function(){
			if (!$scope.username){
				$window.alert('Please enter user name');
				return;
			}
			if(!$scope.currEnviron){
				$window.alert('Please select an environment');
				return;	
			}
			if(!$scope.password){
				$window.alert('Please enter password entry');
				return;	
			}

			httpCall('POST', '/pws/add', {user: $scope.username, env: $scope.currEnviron, password: $scope.password}, function(data){
				if (data.stat){
					$scope.users.push({env_name: $scope.currEnviron, login: $scope.username})
				}
				$window.alert('Server:' + data.msg);
			}, transformReq);				
		};

		$scope.updateUserPassword = function(){
			if(!$scope.currUser || !$scope.currUser.login){
				return;
			}
			httpCall('POST', '/pws/update', {user: $scope.currUser.login, env: $scope.currUser.env_name, password: $scope.currUser.password}, function(data){
				$window.alert('Server:' + data.msg);
			}, transformReq);			
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

mainApp.controller('newEnvionController', ['$scope', '$window', '$http', 'environService', function($scope, $window, $http, environService){

	$scope.createNewEnv = function(){			
		if ($scope.newEnviron != ''){									
			$http({
			    method: 'GET',
			    url: '/env/add?env=' + $scope.newEnviron			    
			}).success(function(data){
				if (data.stat){
					environService.push($scope.newEnviron);			 				
				}
				$window.alert(data.msg);	
				
			}).error(function(err_msg){
				$window.alert('Error' + err_msg);
			});		
			
		}else{
			$window.alert('Please enter the environment name.');
		}			
	};

}]);

mainApp.factory('environService', function($rootScope){		
	return {
		push: function(data){			
			$rootScope.$broadcast('envChange', data);;
		}		
	};
});

mainApp.factory('transformReq', glb_postTransformFnc);
