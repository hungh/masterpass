/** login controller */

angular.module('admin-app', [])
.service('transformReq', glb_postTransformFnc)
.controller('adminController', ['$scope', '$window', '$http', 'transformReq', function($scope, $window, $http, transformReq){		

		$http({
		    method: 'GET',
		    url: '/user/get',
		}).success(function(jsonStr){
			$scope.users = jsonStr;
			$scope.selectedUser = $scope.users [0];
			$scope.selectedMenu = $scope.memus [0]
		}).error(function(err_msg){
			$window.location.href = "/";
		});		

		$scope.memus = ['addUserId', 'removeUserId', 'updateUserId', 'adminStatId'];		
		$scope.allSessions = [];

		$scope.switchMenu = function(elemId){
			angular.forEach($scope.memus, function(elementId, index){
				if (elementId == elemId) {
					document.getElementById(elementId).style.display = 'block';		
				}else {
					document.getElementById(elementId).style.display = 'none';
				}
			});
			
		};

		
		$scope.getSessions = function(){
			$http({
			    method: 'GET',
			    url: '/user/active',
			}).success(function(data){
				$scope.totalLogins = data.length;			
				$scope.allSessions = data;
			});
		};

		$scope.getSessions();

		$scope.addUser = function(){	
			if(!$scope.newId){
				$scope.addUserMsg = 'User ID is required.';
				$scope.msgType = 'warning';
				return;
			}
			if(!$scope.newPassword){
				$scope.addUserMsg = 'Password is required.';
				$scope.msgType = 'warning';
				return;
			}				

			var newUser = {id: $scope.newId, first: $scope.newFirst, last: $scope.newLast, password: $scope.newPassword, email: $scope.email};			
			var httpResponse = $http({
			    method: 'POST',
			    url: '/user/add',
			    transformRequest: transformReq,
			    data: newUser,
			    headers: glb_formHeader
			}).success(function(status){
				$scope.users.push(newUser);				
				$scope.addUserMsg = status;
				$scope.msgType = 'success';
			}).error(function(err_msg){
				$scope.msgType = 'warning';
				$scope.addUserMsg = err_msg;
				$scope.msgType = 'danger';
			});			
		}

		$scope.saveUser = function(){			
			if(!$scope.selectedUser || !$scope.selectedUser.id){
				$scope.addUserMsg ='Please enter select a user';
				$scope.msgType = 'danger';
				return;
			}
			var httpResponse = $http({
			    method: 'POST',
			    url: '/user/update',
			    transformRequest: transformReq,
			    data: {id: $scope.selectedUser.id, first: $scope.selectedUser.first, last: $scope.selectedUser.last, email: $scope.selectedUser.email},
			    headers: glb_formHeader
			}).success(function(status){				
				$scope.updateUserMsg = status;				
				$scope.msgType = 'success';
			}).error(function(err_msg){				
				$scope.updateUserMsg = err_msg;
				$scope.msgType = 'danger';
			});			
		};

		$scope.deleteUser = function(uid){							
			if (uid == 'root'){
				$window.alert('root user cannot be deleted.');
				return;
			}
			var ans = $window.confirm('Are you sure you want to delete :' + uid);
			if (ans == true){
				var httpResponse = $http({
				    method: 'GET',
				    url: '/user/delete?id=' + uid,
				}).success(function(stat){
					$scope.removeUserInfoMsg = stat;
					angular.forEach($scope.users, function(oneUser, index){
						if (oneUser.id == uid){
							$scope.users.splice(index, 1);
							return;						
						}
					});
				}).error(function(err_msg){
					$scope.addUserMsg = err_msg;
					$scope.msgType = 'danger';
				});						
			}
		};
		
	}]);
