var mainApp = angular.module('main', ['ui.bootstrap']);


mainApp.controller('pwsEntryController', ['$scope', '$http', '$window', 'environService', '$modal', 'httpPostGetService',
	 function($scope, $http, $window, environService, $modal, httpPostGetService){			
		$scope.users = [];		
		$scope.currUser = $scope.users[0];
		$scope.currEnviron = 'DEV';
		$scope.newEnviron = '';
		$scope.environs = []; 
		
		httpPostGetService.httpPostGet('GET', '/env/get', {}, function(data){
			$scope.environs = data;
		});

		httpPostGetService.httpPostGet('GET', '/user/current', {}, function(data){
			$scope.current_login = data;
		});

		httpPostGetService.httpPostGet('POST', '/pws/pwsowner', {}, function(data){
			if (data.stat){
				$scope.users = data.msg;
			}else {
				$window.alert(data.msg);
			}
		});

		/** functions */
		$scope.getUserPassword = function(){						
			if(!$scope.currUser || !$scope.currUser.login || !$scope.currUser.env_name ){
				$window.alert('Please select an entry from drop down');
				return;
			}

			$modal.open({
				templateUrl: 'appPasswordPop.html',
			    controller: 'modalInstanceController',			  
			    resolve: {
			        modalData: function () {			         
			          return {
			          			login: $scope.currUser.login,
			          			env: $scope.currUser.env_name,
			          			url: '/pws/get',
			          			callback: 
				          			function(data){
										if (data.stat){
											$scope.currUser.password = data.msg;
										}else {
											$window.alert(data.msg);
										}
									}								
			          		};
			        }
			    }
			});	
		};

		$scope.addPassword = function(){
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

			$modal.open({
				templateUrl: 'appPasswordPop.html',
			    controller: 'modalInstanceController',			  
			    resolve: {
			        modalData: function () {			         
			          return {
			          			login: $scope.username,
			          			env: $scope.currEnviron,	
			          			password: $scope.password,		          			
			          			url: '/pws/add',
			          			callback: 
				          			function(data){
										if (data.stat){
											$scope.users.push({env_name: $scope.currEnviron, login: $scope.username})
										}
										$window.alert('Server:' + data.msg);
									}															
			          		};
			        }
			    }
			});						
		};

		var delOrUpdateValidate = function(){
			if(!$scope.currUser || !$scope.currUser.login){
				return false;
			}
			return true;
		}

		$scope.updateUserPassword = function(){
			if(!delOrUpdateValidate()){
				return;
			}			
			$modal.open({
				templateUrl: 'appPasswordPop.html',
			    controller: 'modalInstanceController',			  
			    resolve: {
			        modalData: function () {			         
			          return {
			          			env: $scope.currUser.env_name,
			          			login: $scope.currUser.login,
			          		 	password: $scope.currUser.password, 			          		 	
			          		 	url: '/pws/update',
			          		 	callback: function(data) {
			          		 		$window.alert('Server:' + data.msg);
			          		 	}
			          		 };
			        }
			    }
			});
			
		};

		$scope.deletePwsEntry = function(){
			if(!delOrUpdateValidate()){
				return;
			}
			httpPostGetService.httpPostGet('POST', '/pws/delete', {user: $scope.currUser.login}, function(data){
				$window.alert('Server:' + data.msg);				
				if(data.stat){				
					for(var i = 0; i < $scope.users.length; i++){
						if ($scope.users[i].login == $scope.currUser.login){
							$scope.currUser.login = '';
							$scope.currUser.env_name = '';
							$scope.currUser.password = '';
							$scope.users.splice(i, 1);
						}
					}				
				}
				
			});			
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

angular.module('main').controller('modalInstanceController', ['$scope', '$http', '$window', '$modalInstance', 'transformReq', 'modalData', function($scope, $http, $window, $modalInstance, transformReq, modalData){
	$scope.updateGetPwsUserPassword = function(masterPassword){				
		$http({
		    method: 'POST',
		    url: modalData.url,
		    transformRequest: transformReq,			    
		    data: 	{
		    			user: modalData.login,
		    			env: modalData.env, 
						password: modalData.password,
						masterPassword: masterPassword
					},
		    headers: glb_formHeader				    
		}).success(function(resp){
			if(resp.stat){
				if(modalData.callback){
					modalData.callback.call(this, resp);
				}									
				$modalInstance.dismiss('cancel');
			}
		}).error(function(err_msg){
		  	$window.alert('Error:' + err_msg);
		});
	};

	$scope.cancel = function () {
    	$modalInstance.dismiss('cancel');
  	};	
}]);


mainApp.controller('newEnvionController', ['$scope', '$window', '$http', 'environService', 'httpPostGetService', 
			function($scope, $window, $http, environService, httpPostGetService){

	$scope.createNewEnv = function(){			
		if ($scope.newEnviron){		
			httpPostGetService.httpPostGet('GET', '/env/add?env=' + $scope.newEnviron, {},  function(data){
				if (data.stat){
					environService.push($scope.newEnviron);			 				
				}
				$window.alert(data.msg);	
				
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

mainApp.factory('httpPostGetService', ['$http', '$window', 'transformReq', function($http, $window, transformReq){
	return {
		httpPostGet: function(method, urlStr, postData, callback){
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
			}
	};
}]);
