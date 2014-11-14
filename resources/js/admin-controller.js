/** admin controller (add, update and delete) a user */

/** login controller */

angular.module('admin-app', [])
	.controller('adminController', ['$scope', '$window', '$http', function($scope, $window, $http ){		
		$scope.users = [
			{id: 'hung2', first: 'Hung', last: 'Huynh'},
			{id: 'hung3', first: 'Tren', last: 'Huynh'},
			{id: 'hun42', first: 'Long', last: 'Nguyen'},
			{id: 'hung5', first: 'Sna', last: 'Collin'},
			{id: 'hung34', first: 'Tong', last: 'William'},
			{id: 'hung12', first: 'Theredoor', last: 'Phan'}			
		];

		$scope.memus = ['addUserId', 'removeUserId', 'updateUserId'];		

		$scope.selectedUser = $scope.users [0];
		$scope.selectedMenu = $scope.memus [0]

		$scope.switchMenu = function(elemId){
			angular.forEach($scope.memus, function(elementId, index){
				if (elementId == elemId) {
					document.getElementById(elementId).style.display = 'block';		
				}else {
					document.getElementById(elementId).style.display = 'none';
				}
			});
			
		};

		$scope.addUser = function(){
			//TODO: update to server if success then update users array
			$scope.users.push({id: $scope.newId, first: $scope.newFirst, last: $scope.newLast});
			alert('Done');
		}

		$scope.saveUser = function(uid, first, last){
			$window.alert("The following user with ID:" + uid + "\nFirst name:" + first + "\nLast name:" + last + 'will be updated to server');
			var isNew = true;
			angular.forEach($scope.users, function(oneUser, index){
				
				if(oneUser.id == uid){					
					$scope.users [index].first = first;
					$scope.users [index].last  = last;
					isNew = false;
					return;
				}
			});
			// new user, add to the user array
			if(isNew){
				$scope.users.push({id: uid, first: first, last: last});
			}			
		};

		$scope.deleteUser = function(uid){		
			//$scope.users
			var ans = $window.confirm('Are you sure you want to delete :' + uid);
			if (ans == true){
				// TODO: send delete command to server
				// reload users
				// for now we just splice the user array
				angular.forEach($scope.users, function(oneUser, index){
					if (oneUser.id == uid){
						$scope.users.splice(index, 1);
						return;						
					}
				});
			}
		};

	}]);