var ktAuth = angular.module('ktAuth', ['http-auth-interceptor', 'ktAPI']);

ktAuth.controller('LoginController', function($rootScope, $scope, $http, authService, AuthAPI, $location) {

  /* test if already logged in */
  AuthAPI.load()
  .success(function(data, status, headers, config) {
    $location.path('/');
    $rootScope.user = data.user;
  })
  .error(function(data, status, headers, config) {
    $location.path('/login');
  });

  $scope.login = function(user) {
    AuthAPI.login(user)
      .success(function(data, status, headers, config) {
        authService.loginConfirmed();
        $location.path('/');
        console.log("login onnistui!");
        $rootScope.user = user;
      })
      .error(function(data, status, headers, config) {
        console.log("login error");
      });
  }

  $scope.logout = function() {
    AuthAPI.logout()
      .success(function(data, status, headers, config) {
        console.log("uloskirjautuminen onnistui");
        $rootScope.user = "";
      })
      .error(function(data, status) {
        //console.log("data", data);
        //console.log("status", status);
      });
  }
});
