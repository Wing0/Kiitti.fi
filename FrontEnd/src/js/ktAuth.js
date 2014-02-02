var ktAuth = angular.module('ktAuth', ['http-auth-interceptor']);

ktAuth.factory('AuthFactory', function(APIUrl, $http) {
  return {
    load: function() {
      return $http.post(APIUrl + '/auth/load');
    },
    login: function(user) {
      return $http.post(APIUrl + '/auth/login', user);
    },
    logout: function() {
      return $http.post(APIUrl + '/auth/logout');
    },
    register: function(user) {
      return $http.post(APIUrl + '/auth/register', user);
    }
  }
});

ktAuth.controller('LoginController', function ($scope, $http, authService, AuthFactory) {
  $scope.login = function(user) {
    AuthFactory.login(user)
      .success(function(data, status, headers, config) {
        authService.loginConfirmed();
        console.log("login onnistui!");
      })
      .error(function(data, status, headers, config) {
        console.log("login error");
      });
  }
});
