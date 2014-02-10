var module = angular.module('ktAPI', ['ngResource']);

module.factory('AuthAPI', function($http, APIUrl) {
  return {
    load: function() {
      return $http.get(APIUrl + '/auth/load');
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

module.factory('AnswerFactory', function($resource, APIUrl) {
  return $resource(APIUrl + '/answers', {},
    { 'get': {method: 'GET', isArray: false} });
});

module.factory('QuestionFactory', function($resource, APIUrl) {
  return $resource(APIUrl + '/questions', {},
    { 'get': {method: 'GET', isArray: false} });
});
