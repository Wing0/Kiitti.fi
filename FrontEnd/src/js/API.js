var module = angular.module('ktAPI', ['ngResource', 'ngCookies']);

module.factory('AuthAPI', function($http, APIUrl, authService, $cookieStore) {
  var user;
  return {
    load: function() {
      return $http.get(APIUrl + '/auth/load')
        .success(function(data) {
          user = data;
        });
    },
    login: function(user) {
      return $http.post(APIUrl + '/auth/login', user)
        .success(function(data) {
          /* confirm login */
          authService.loginConfirmed();

          /* set token into cookies */
          $cookieStore.put('tursas', data.token);
          $http.defaults.headers.common['Authorization'] = 'Token ' + data.token;

          user = data;
        });
    },
    logout: function() {
      return $http.get(APIUrl + '/auth/logout')
        .success(function(data) {
          delete user;
        });
    },
    register: function(user) {
      return $http.post(APIUrl + '/auth/register', user);
    },
    user: function() {
      return user;
    }
  }
});

module.factory('AnswerAPI', function($resource, APIUrl) {
  return $resource(APIUrl + '/answers', {},
    { 'get': {method: 'GET', isArray: false} });
});

module.factory('QuestionAPI', function($resource, APIUrl) {
  return $resource(APIUrl + '/questions/:messageId', {},
    { 'get': {method: 'GET', isArray: false} });
});
