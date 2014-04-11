var HotOrNotApp = angular.module("HotOrNotApp", []);

HotOrNotApp.controller("sexController", function($scope) {
	$scope.sex = "Men";
});

HotOrNotApp.controller("peepsController", function($scope, $http) {
	$http.get('http://hot-or-not-api.demo4sa.org/get_member/male/').success(function(peep1) {
		$http.get('http://hot-or-not-api.demo4sa.org/get_member/male/').success(function(peep2) {
			$scope.peeps = [ peep1, peep2 ];
		});
	});
});
