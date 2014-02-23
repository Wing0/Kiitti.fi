var module = angular.module('ktAPI', ['ngResource', 'ngCookies']);

module.factory('AuthAPI', function($http, APIUrl, authService, $cookieStore, $log) {
  var user;
  var Methods = {
    load: function() {
      return $http.get(APIUrl + '/auth/load')
        .success(function(data) {
          user = data;
        })
        .error(function(response) {
          $log.error("Could not load user");
        });
    },
    logout: function() {
      return $http.get(APIUrl + '/auth/logout')
        .success(function(data) {
          $cookieStore.remove('tursas');
          delete $http.defaults.headers.common['Authorization'];
          delete user;
        });
    },
    register: function(user) {
      return $http.post(APIUrl + '/auth/register', user);
    }
  };

  Methods.login = function(user) {
    return $http.post(APIUrl + '/auth/login', user)
      .success(function(data) {
        /* set token into cookies */
        try { var authtoken = data.token; }
        catch(TypeError) {
          $log.info("Already logged in.")
        };

        if (authtoken) {
          /* set token into cookies */
          $cookieStore.put('tursas', authtoken);
          $http.defaults.headers.common['Authorization'] = 'Token ' + authtoken;

          // get user data
          Methods.load(function() {
            /* confirm login */
            authService.loginConfirmed();
          }, function() {
            $log.error("Unexpected error in loading user")
          });
        }
      });
  };

  Methods.user = function() {
    return user;
  };

  return Methods;
});

module.factory('QuestionAPI', function($resource, APIUrl) {
  return $resource(APIUrl + '/questions/:messageId', {},
    { 'get': {method: 'GET', isArray: false} });
});

module.factory('AnswerAPI', function($resource, APIUrl) {
  return $resource(APIUrl + '/answers');
});

module.factory('CommentAPI', function($resource, APIUrl) {
  return $resource(APIUrl + '/comments');
});
