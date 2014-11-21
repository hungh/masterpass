var mainApp = angular.module('main', ['ui.bootstrap']);


mainApp.controller('pwsEntryController', ['$scope', '$http', '$window', 'environService', 'transformReq', '$modal',
	 function($scope, $http, $window, environService, transformReq, $modal){			
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

			httpCall('POST', '/pws/add', {user: $scope.username, env: $scope.currEnviron, 
										  password: $scope.password,  masterPassword: $scope.masterPassword}, function(data){
				if (data.stat){
					$scope.users.push({env_name: $scope.currEnviron, login: $scope.username})
				}
				$window.alert('Server:' + data.msg);
			}, transformReq);				
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
			var modalInstance = $modal.open({
				templateUrl: 'appPasswordPop.html',
			    controller: 'modalInstanceController',			  
			    resolve: {
			        modalData: function () {			         
			          return {
			          			env: $scope.currUser.env_name, login: $scope.currUser.login,
			          		 	password: $scope.currUser.password, masterPassword: $scope.masterPassword
			          		 };
			        }
			    }
			});

			modalInstance.result.then(function (selectedItem) {
		      $window.alert('Model result-then=' + selectedItem);
		    }, function () {
		       /** exit modal: do nothiing*/
		    });
		};

		$scope.deletePwsEntry = function(){
			if(!delOrUpdateValidate()){
				return;
			}
			httpCall('POST', '/pws/delete', {user: $scope.currUser.login}, function(data){
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

angular.module('main').controller('modalInstanceController', ['$scope', '$http', '$window', '$modalInstance', 'transformReq', 'modalData', function($scope, $http, $window, $modalInstance, transformReq, modalData){
	$scope.updatePwsUserPassword = function(masterPassword){		
		$http({
		    method: 'POST',
		    url: '/pws/update',
		    transformRequest: transformReq,			    
		    data: {user: modalData.login, env: modalData.env, 
											password: modalData.password, masterPassword: masterPassword},
		    headers: glb_formHeader				    
		}).success(function(data){
			if(data.stat){
				$window.alert('Server:' + data.msg);
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


mainApp.controller('newEnvionController', ['$scope', '$window', '$http', 'environService', function($scope, $window, $http, environService){

	$scope.createNewEnv = function(){			
		if ($scope.newEnviron){									
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
