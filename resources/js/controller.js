var mainApp = angular.module('main', ['ui.bootstrap']);


mainApp.controller('pwsEntryController', ['$scope', '$http', '$window', 'environService', '$modal', 'httpPostGetService',
	 function($scope, $http, $window, environService, $modal, httpPostGetService){			
		$scope.users = [];		
		/** current select pws entry user*/
		$scope.currUser = $scope.users[0];
		/** log-in name to access application*/
		$scope.appLoginName = '';
		$scope.currEnviron = '';
		$scope.newEnviron = '';
		$scope.environs = []; 
		$scope.showAdmin = false;

		var removeSelectedUser = function(removingLogin){
			for(var i = 0; i < $scope.users.length; i++){
				if ($scope.users[i].login == removingLogin) {
					/**if selected*/
					if($scope.currUser){
						$scope.currUser.login = '';
						$scope.currUser.env_name = '';
						$scope.currUser.password = '';	
					}					
					$scope.users.splice(i, 1);
					break;
				}
			}
		};			

		var handleError =  function(msg){
			$scope.workAreaMsg = msg;
		};

		httpPostGetService.httpPostGet('GET', '/user/current', {}, function(appLoginName){			
			$scope.appLoginName  = appLoginName;
			if(appLoginName == 'root'){
				$scope.showAdmin = true;
			}
			
		}, handleError);

		httpPostGetService.httpPostGet('GET', '/env/get', {}, function(data){			
			$scope.environs = data;
		}, function(msg){
			$scope.envErrMsg = msg;
		}, handleError);


		httpPostGetService.httpPostGet('POST', '/pws/pwsowner', {}, function(data){
			if (data.stat){
				$scope.users = data.msg;
			}else {
				$scope.workAreaMsg = data.msg;
			}
		}, handleError);

		$scope.createNewEnv = function(){			
			if ($scope.newEnviron){		
				httpPostGetService.httpPostGet('GET', '/env/add?env=' + $scope.newEnviron, {},  function(data){
					if (data.stat){
						environService.push($scope.newEnviron);			 				
					}
					$scope.envErrMsg = data.msg;	
					$scope.msgType = 'info';
					
				});									
			}else{
				$scope.envErrMsg = 'Please enter the environment name.';
				$scope.msgType = 'warning';
			}			
		};

		$scope.deleteEnv = function(env){
			httpPostGetService.httpPostGet('GET', '/env/delete?env=' + env, {},  function(data){
					var new_users = [];
					if (data.stat){
						environService.pop(env);		
						angular.forEach($scope.users, function(v, i){
							if(v.env_name != env){
								new_users.push(v);
							}							
						});
						$scope.users = new_users;	
					}
					$scope.envErrMsg = data.msg;						
					$scope.msgType = 'info';
				});	
		};

		/** functions */
		$scope.getUserPassword = function(){						
			if(!$scope.currUser || !$scope.currUser.login || !$scope.currUser.env_name ){
				$scope.workAreaMsg = 'Please select an entry from drop down';
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
											if ($scope.isMaskCheck){
												$scope.currUser.password = data.msg;												
												toTextInp('maskPasswordId');
											}else{
												$scope.currUser.password = maskText(data.msg, 'maskPasswordId');
												toPasswordInp('maskPasswordId');												
											}
											
										}else {
											$scope.workAreaMsg = data.msg;
										}
									}								
			          		};
			        }
			    }
			});	
		};

		$scope.addPassword = function(){				
			if(!$scope.currEnviron){
				$scope.workAreaMsg = 'Please select an environment';
				return;	
			}
		
			if (!$scope.username){
				$scope.workAreaMsg = 'Please enter user name';
				return;
			}
			if(!$scope.password){
				$scope.workAreaMsg = 'Please enter password entry';
				return;	
			}
			if($scope.password != $scope.confirmPassword){
				$scope.workAreaMsg = 'Your password don\'t match';
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

		$scope.updateUserPassword = function(){
			if(!$scope.currUser || !$scope.currUser.login) {				
				$scope.workAreaMsg = 'Please select an entry from the drop-down';
				return;
			}			
			if(!$scope.currUser.password){
				$window.alert('Enter a new value for password');
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
			if(!$scope.currUser){
				return;
			}
			httpPostGetService.httpPostGet('POST', '/pws/delete', {user: $scope.currUser.login}, function(data){
				$window.alert('Server:' + data.msg);				
				if(data.stat){			
					removeSelectedUser($scope.currUser.login);					
				}
				
			});			
		};
	
		$scope.$on('addEnvionEvent', function(event, data) {				
        	$scope.environs.push(data);
       	});

       	$scope.$on('delEnvionEvent', function(event, data) {				
        	if($scope.environs){
        		for(var i = 0; i < $scope.environs.length; i++){
        			if($scope.environs[i] == data){
        				$scope.environs.splice(i, 1);
        				break;
        			}
        		}
        	}
       	});

       	$scope.isMaskCheck = false;
       	/** mask/ unmask password*/
       	$scope.maskPassword = function(maskId){       		
       		if ($scope.isMaskCheck === true){
       			$scope.currUser.password = unMaskText($scope.currUser.password, maskId);       			
       		}else{
       			$scope.currUser.password = maskText($scope.currUser.password, maskId);
       		}
       	};

		$scope.memus = ['workAreaId', 'changeEnvId', 'changePwId'];

       	$scope.switchMenu = function(elemId){
			angular.forEach($scope.memus, function(elementId, index){
				if (elementId == elemId) {
					document.getElementById(elementId).style.display = 'block';		
				}else {
					document.getElementById(elementId).style.display = 'none';
				}
			});
			
		};  

		$scope.showNewPassword = function(pwIds){
			for(var i = 0; i < pwIds.length; i++){
				if($scope.isShownPassword){
					toTextInp(pwIds[i]);
				}else{
					toPasswordInp(pwIds[i]);								
				}				
			}			
		};

	}]);

angular.module('main').controller('modalInstanceController', ['$scope', '$http', '$window', '$modalInstance', 'transformReq', 'modalData', function($scope, $http, $window, $modalInstance, transformReq, modalData){
	$scope.updateGetPwsUserPassword = function(masterPassword){		
		if (!masterPassword){
			$scope.modalMsg = 'Please enter password';
			return;
		}		
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
			}else{
				$scope.modalMsg = resp.msg;	
			}
		}).error(function(err_msg){
		  	$scope.modalMsg = err_msg;
		});
	};

	$scope.cancel = function () {
    	$modalInstance.dismiss('cancel');
  	};	
}]);


mainApp.factory('environService', function($rootScope){		
	return {
		push: function(data){			
			$rootScope.$broadcast('addEnvionEvent', data);;
		},
		pop: function(data){
			$rootScope.$broadcast('delEnvionEvent', data);;	
		}		
	};
});

mainApp.factory('transformReq', glb_postTransformFnc);

mainApp.factory('httpPostGetService', ['$http', '$window', 'transformReq', function($http, $window, transformReq){
	return {
		httpPostGet: function(method, urlStr, postData, callback, errorHandler){
				var processError = function(err_msg){
						if(errorHandler){
							errorHandler.call(this, err_msg);
						}else{
							$window.alert('Error:' + err_msg);
						}	
					};
				if(method == 'GET'){
					$http({
				    	method: 'GET',
				    	url: urlStr,
					}).success(function(data){
						callback.call(this, data);
					}).error(function(err_msg){
						processError(err_msg);				
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
					  	processError(err_msg);
					});
				}		
			}
	};
}]);
