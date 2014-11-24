/** login controller */

var adminApp = angular.module('admin-app', [])
	.controller('adminController', ['$scope', '$window', '$http', 'transformReq', function($scope, $window, $http, transformReq){		

		$http({
		    method: 'GET',
		    url: '/user/get',
		}).success(function(jsonStr){
			$scope.users = jsonStr;
			$scope.selectedUser = $scope.users [0];
			$scope.selectedMenu = $scope.memus [0]
		}).error(function(err_msg){
			alert(err_msg);
		});		

		$scope.memus = ['addUserId', 'removeUserId', 'updateUserId', 'adminStatId'];		

		$scope.switchMenu = function(elemId){
			angular.forEach($scope.memus, function(elementId, index){
				if (elementId == elemId) {
					document.getElementById(elementId).style.display = 'block';		
				}else {
					document.getElementById(elementId).style.display = 'none';
				}
			});
			
		};

		$scope.getAdminStat = function(){
			$http({
			    method: 'GET',
			    url: '/user/active',
			}).success(function(data){
				for(var i = 0; i < data.length; i ++){
					$window.alert('session id=' + data[i].session + ';user=' + data[i].user);
				}				
			}).error(function(err_msg){
				$window.alert(err_msg);
			});			
		};

		$scope.addUser = function(){	
			if(!$scope.newId){
				$window.alert('User ID is required.');
				return;
			}
			if(!$scope.newPassword){
				$window.alert('Password is required.');
				return;
			}				

			var newUser = {id: $scope.newId, first: $scope.newFirst, last: $scope.newLast, password: $scope.newPassword};			
			var httpResponse = $http({
			    method: 'POST',
			    url: '/user/add',
			    transformRequest: transformReq,
			    data: newUser,
			    headers: glb_formHeader
			}).success(function(status){
				$scope.users.push(newUser);
				alert(status);
			}).error(function(err_msg){
				alert(err_msg);
			});			
		}

		$scope.saveUser = function(){			
			if(!$scope.selectedUser || !$scope.selectedUser.id){
				$window.alert('Please enter select a user');
				return;
			}
			var httpResponse = $http({
			    method: 'POST',
			    url: '/user/update',
			    transformRequest: transformReq,
			    data: {id: $scope.selectedUser.id, first: $scope.selectedUser.first, last: $scope.selectedUser.last},
			    headers: glb_formHeader
			}).success(function(status){
				$window.alert(status);				
			}).error(function(err_msg){
				alert(err_msg);
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
					$window.alert(stat);
					angular.forEach($scope.users, function(oneUser, index){
						if (oneUser.id == uid){
							$scope.users.splice(index, 1);
							return;						
						}
					});
				}).error(function(err_msg){
					alert(err_msg);
				});						
			}
		};
		
	}]);


adminApp.factory('transformReq', glb_postTransformFnc);