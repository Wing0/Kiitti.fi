var module = angular.module('ktAPI', ['ngResource']);

module.factory('AuthAPI', function(APIUrl, $http) {
  return {
    load: function() {
      return $http.get(APIUrl + '/auth/login');
    },
    login: function(user) {
      return $http.post(APIUrl + '/auth/login', user);
    },
    logout: function() {
      return $http.get(APIUrl + '/auth/logout');
    },
    register: function(user) {
      return $http.post(APIUrl + '/auth/register', user);
    }
  }
});

module.factory('AnswerFactory', function($resource) {
  return $resource('http://0.0.0.0:8000' + '/answers', {},
    { 'get': {method: 'GET', isArray: false} });
});
